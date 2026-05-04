"""2-step Chain-of-Thought ingest engine.

Ingest pipeline:
- Step 1: Read source + schema.md + purpose.md → structured analysis
- Step 2: Generate wiki pages with exact paths and frontmatter

Critical rules:
- Source summary page MUST be at wiki/sources/{slug}.md
- All pages MUST include `sources` field in frontmatter
- All pages MUST use [[wikilinks]] for cross-references
- Pages MUST be written to wiki/entities/, wiki/concepts/, etc.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

from .cache import IngestCache
from .project_mutex import ProjectLock
from .sanitize import sanitize_page_content


# ── Path safety ───────────────────────────────────────────────────────

@dataclass
class ParsedBlock:
    path: str
    content: str


def is_safe_ingest_path(p: str) -> bool:
    """Reject wiki write paths that escape the wiki/ tree.

    The path field comes straight from LLM-generated text, so an attacker
    can plant prompt injection like "---FILE: ../../../etc/passwd---".
    Without this check the writer would happily overwrite system files.

    Allowed:     wiki/concepts/foo.md, wiki/entities/bar.md
    Rejected:
      - paths not starting with wiki/
      - absolute paths (/etc/passwd, C:/Windows/...)
      - any .. segment
      - NUL or control characters
      - empty / whitespace-only paths
    """
    if not isinstance(p, str) or not p.strip():
        return False
    if re.search(r'[\x00-\x1f]', p):
        return False
    # Reject absolute paths (POSIX) and Windows drive letters / UNC
    if p.startswith("/") or p.startswith("\\"):
        return False
    if re.match(r'^[a-zA-Z]:', p):
        return False
    # Normalize backslashes so a Windows-style payload doesn't sneak past
    normalized = p.replace("\\", "/")
    # No .. segments anywhere
    if ".." in normalized.split("/"):
        return False
    # Must live under wiki/
    if not normalized.startswith("wiki/"):
        return False
    return True


# ── Step 1: Analysis prompt ─────────────────

ANALYSIS_PROMPT = """You are analyzing a source document for a wiki knowledge base.

## Wiki Context

### Schema
{schema}

### Purpose
{purpose}

## Source Document

Filename: {filename}

{source}

---

Analyze this source and produce a JSON object with these fields:
- "title": main title/subject of the document
- "authors": list of authors (if mentioned)
- "year": publication year (if mentioned)
- "url": URL (if mentioned)
- "venue": publication venue (if mentioned)
- "entities": list of important named entities (people, organizations, tools, datasets)
- "concepts": list of key concepts with brief definitions
- "arguments": list of main arguments or claims
- "connections": list of connections between concepts (each: {{"from", "to", "relation"}})
- "tags": list of relevant tags/keywords
- "confidence": 0.0-1.0 confidence in analysis quality
- "summary": 2-3 sentence summary

Respond ONLY with valid JSON, no markdown fencing."""


# ── Step 2: Page generation prompt ──────────

PAGE_GENERATION_PROMPT = """You are a wiki page generator. Based on the analysis below, generate wiki pages for a local knowledge base.

## Wiki Context

### Schema
{schema}

### Purpose
{purpose}

### Current Index
{current_index}

## Source Analysis

{analysis}

Source filename: {filename}

---

Generate wiki pages using this EXACT format for each page:

---FILE: wiki/path.md---
<page content in markdown>
---END FILE---

## CRITICAL RULES (must follow exactly):

1. **Source summary page**: MUST be at `wiki/sources/{source_slug}.md`
   - This is the most important page - it summarizes the source document
   - MUST include `sources: ["{filename}"]` in frontmatter

2. **Entity pages**: For each key entity (person, org, tool), create a page at `wiki/entities/<slug>.md`
   - MUST include `sources: ["{filename}"]` in frontmatter

3. **Concept pages**: For each key concept, create a page at `wiki/concepts/<slug>.md`
   - MUST include `sources: ["{filename}"]` in frontmatter

4. **Frontmatter format** (MUST use exactly):
```
---
type: source | entity | concept
title: Human-readable title
tags: []
related: []
sources: ["{filename}"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Source pages also include:
```
authors: []
year: YYYY
url: ""
venue: ""
```

5. **Cross-references**: Use `[[page-slug]]` syntax to link between pages

6. **Content**: Each page should have:
   - Title (H1)
   - Overview section
   - Key details
   - Related pages section with [[wikilinks]]

7. **Naming**: Use kebab-case slugs (e.g., `gpt-4.md`, `chain-of-thought.md`)
   - Entity slugs MUST match official names (e.g., `claude-2.0`, `gpt-3.5`, `llama-3-instruct-8b`) - do NOT convert dots/hyphens
   - NEVER add prefix like `concept/`, `entity/`, or `source/` to wikilinks - just use the bare slug directly
   - Example correct: `[[decomposition-attacks]]` NOT `[[concept/decomposition-attacks]]`

Generate ALL pages now. Do NOT skip the source summary page."""


class IngestEngine:
    """2-step Chain-of-Thought ingest: analyze then generate wiki pages.

    2-step ingest behavior:
    - Read schema.md and purpose.md as context
    - Force exact file paths for generated pages
    - Use standard frontmatter format
    """

    def __init__(self, wiki_manager, llm_client):
        self.wiki = wiki_manager
        self.llm = llm_client
        self.cache = IngestCache(wiki_manager.project_path)

    def _read_source(self, source_path: str) -> str:
        """Read source file, handling MinerU nested structure."""
        p = Path(source_path)
        if p.is_dir():
            # MinerU output: look for nested markdown
            candidates = list(p.rglob("*.md"))
            if candidates:
                # Prefer file matching parent dir name, else first found
                parent_name = p.name
                for c in candidates:
                    if c.stem == parent_name:
                        return c.read_text(encoding="utf-8")
                return candidates[0].read_text(encoding="utf-8")
            raise FileNotFoundError(f"No markdown files found in {source_path}")
        if p.is_file():
            return p.read_text(encoding="utf-8")
        raise FileNotFoundError(f"Source not found: {source_path}")

    def _find_images(self, source_path: str) -> list[Path]:
        """Find associated images (for MinerU outputs)."""
        p = Path(source_path)
        base = p if p.is_dir() else p.parent
        return sorted(base.rglob("*.png")) + sorted(base.rglob("*.jpg"))

    def _parse_file_blocks(self, text: str) -> tuple[list[ParsedBlock], list[str]]:
        """Parse ---FILE: path--- ... ---END FILE--- blocks (fence-aware).

        Handles all known LLM output hazards:
          H1 CRLF              — normalize to LF before parsing
          H2 stream truncation — surface as warning instead of silent drop
          H3 whitespace/case  — opener/closer line scanner is tolerant
          H5 ---END FILE---    — inside fenced code block treated as body text
          H6 empty path       — surface as warning

        Returns:
            blocks: list of ParsedBlock
            warnings: list of human-readable issue descriptions
        """
        return parse_file_blocks(text)


def parse_file_blocks(text: str) -> tuple[list[ParsedBlock], list[str]]:
    """Module-level FILE-block parser (fence-aware). See IngestEngine._parse_file_blocks."""
    # H1 fix: normalize CRLF
    normalized = text.replace("\r\n", "\n")
    lines = normalized.split("\n")

    blocks: list[ParsedBlock] = []
    warnings: list[str] = []

    # Fence delimiters: triple+ backticks or tildes, CommonMark compliant.
    # Indent ≤ 3 spaces still counts as fence; 4+ spaces is indented code block.
    FENCE_LINE = re.compile(r'^\s{0,3}(```+|~~~+)')

    i = 0
    while i < len(lines):
        opener_match = re.match(r'^---\s*FILE:\s*(.+?)\s*---\s*$', lines[i], re.IGNORECASE)
        if not opener_match:
            i += 1
            continue

        path = opener_match.group(1).strip()
        i += 1

        # Collect content until closer
        content_lines: list[str] = []
        fence_marker: str | None = None
        fence_len = 0
        closed = False

        while i < len(lines):
            line = lines[i]

            # H5 fix: update fence state BEFORE checking closer.
            # Only close the fence when same char repeated ≥ length.
            fence_match = FENCE_LINE.match(line)
            if fence_match:
                run = fence_match.group(1)
                char = run[0]
                length = len(run)
                if fence_marker is None:
                    fence_marker = char
                    fence_len = length
                elif char == fence_marker and length >= fence_len:
                    fence_marker = None
                    fence_len = 0
                content_lines.append(line)
                i += 1
                continue

            # A line matching the closer ONLY counts when outside any fence
            closer_match = re.match(r'^---\s*END\s+FILE\s*---\s*$', lines[i], re.IGNORECASE)
            if fence_marker is None and closer_match:
                closed = True
                i += 1
                break

            content_lines.append(line)
            i += 1

        if not closed:
            # H2 fix: surface truncation instead of silent drop
            path_label = path or "(unnamed)"
            msg = (f"FILE block \"{path_label}\" was not closed before "
                   "end of stream — likely truncation (model hit max_tokens, "
                   "timeout, or connection dropped). Block dropped.")
            warnings.append(msg)
            continue

        if not path:
            # H6 fix: surface empty-path blocks
            msg = "FILE block with empty path skipped (LLM omitted the path after `---FILE:`)."
            warnings.append(msg)
            continue

        blocks.append(ParsedBlock(path=path, content="\n".join(content_lines).strip()))

    return blocks, warnings

    def _step1_analyze(self, source_content: str, filename: str) -> dict:
        """Step 1: LLM analyzes source into structured JSON.

        Ingest behavior:
        - Read schema.md and purpose.md as context
        - Pass source content with filename
        """
        # Read schema and purpose as context
        schema = self.wiki.read_schema()
        purpose = self.wiki.read_purpose()

        prompt = ANALYSIS_PROMPT.format(
            schema=schema[:3000] if schema else "(no schema defined)",
            purpose=purpose[:2000] if purpose else "(no purpose defined)",
            source=source_content[:15000],  # truncate for context
            filename=filename,
        )
        response = self.llm.generate(prompt, system="You are an expert knowledge analyst.")
        # Extract JSON from response
        response = response.strip()
        if response.startswith("```"):
            response = re.sub(r"^```(?:json)?\s*\n?", "", response)
            response = re.sub(r"\n?```\s*$", "", response)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to find JSON object by brace counting (handles truncation)
            raw = _extract_json_by_braces(response)
            if raw:
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    raw = re.sub(r",\s*([}\]])", r"\1", raw)  # remove trailing commas
                    try:
                        return json.loads(raw)
                    except json.JSONDecodeError:
                        print(f"⚠ LLM response (first 500 chars): {raw[:500]}")
                        raise RuntimeError(f"Failed to parse analysis JSON even after cleanup. Response: {raw[:500]}")
            print(f"⚠ LLM response (first 500 chars): {response[:500]}")
            raise RuntimeError(f"Failed to parse analysis JSON. Response: {response[:500]}")

    def _step2_generate_pages(self, analysis: dict, filename: str) -> list[tuple[str, str]]:
        """Step 2: LLM generates wiki pages from analysis.

        Ingest behavior:
        - Read schema.md, purpose.md, and current index.md as context
        - Force exact file paths (wiki/sources/..., wiki/entities/..., wiki/concepts/...)
        - Use standard frontmatter format
        """
        # Read schema, purpose, and current index
        schema = self.wiki.read_schema()
        purpose = self.wiki.read_purpose()
        current_index = self.wiki.read_index()

        # Create source slug for the mandatory source summary page
        source_slug = self.wiki.slugify(Path(filename).stem)

        prompt = PAGE_GENERATION_PROMPT.format(
            schema=schema[:3000] if schema else "(no schema defined)",
            purpose=purpose[:2000] if purpose else "(no purpose defined)",
            current_index=current_index[:2000] if current_index else "(empty index)",
            analysis=json.dumps(analysis, indent=2, ensure_ascii=False),
            filename=filename,
            source_slug=source_slug,
        )
        response = self.llm.generate(
            prompt,
            system="You are a wiki page generator. Always use ---FILE: ...--- format.",
            max_tokens=30000,
        )
        blocks, warnings = self._parse_file_blocks(response)
        if not blocks:
            raise RuntimeError(f"No FILE blocks found in generation response: {response[:500]}")
        return blocks, warnings

    def _copy_images(self, source_path: str) -> list[str]:
        """Copy associated images to wiki assets and generate vision descriptions."""
        images = self._find_images(source_path)
        copied = []
        descriptions = {}

        try:
            from wiki_cli.core.vision import VisionClient
            source_text = self._read_source(source_path)[:1000] if Path(source_path).exists() else ""
            vision = VisionClient()
            for img in images:
                desc = vision.describe_image(str(img), context=source_text)
                if desc:
                    descriptions[img.name] = desc
        except Exception:
            pass

        desc_dir = Path(self.wiki.project_path) / ".llm-wiki" / "assets" / "image-descriptions"
        if descriptions:
            desc_dir.mkdir(parents=True, exist_ok=True)
            desc_file = desc_dir / f"{Path(source_path).stem}-descriptions.json"
            desc_file.write_text(json.dumps(descriptions, indent=2, ensure_ascii=False), encoding="utf-8")

        for img in images:
            dest_dir = Path(self.wiki.project_path) / ".llm-wiki" / "assets" / "images"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / img.name
            if not dest.exists():
                dest.write_bytes(img.read_bytes())
            copied.append(str(dest))
        return copied

    def ingest(self, source_path: str, collection: str | None = None) -> dict:
        """Ingest a source file into the wiki.

        Ingest behavior:
        1. Read source + schema.md + purpose.md
        2. LLM analyzes source -> structured JSON
        3. LLM generates wiki pages using FILE blocks
        4. Parse blocks, write pages, update index/log/overview

        Critical rules:
        - Source summary page MUST be at wiki/sources/{slug}.md
        - All pages MUST include `sources` field in frontmatter
        - Pages MUST be written to wiki/entities/, wiki/concepts/, etc.
        """
        with ProjectLock(self.wiki.project_path):
            return self._ingest_impl(source_path, collection)

    def _ingest_impl(self, source_path: str, collection: str | None) -> dict:
        """Ingest implementation (called inside ProjectLock)."""
        filename = os.path.basename(source_path)

        # Read source
        source_content = self._read_source(source_path)

        # Check cache
        cached = self.cache.check(filename, source_content)
        if cached is not None:
            return {
                "status": "cached",
                "filename": filename,
                "output_paths": cached,
                "analysis": None,
            }

        # Step 1: Analyze (with schema.md and purpose.md as context)
        analysis = self._step1_analyze(source_content, filename)

        # Step 2: Generate pages (with schema.md, purpose.md, and index.md as context)
        page_blocks, gen_warnings = self._step2_generate_pages(analysis, filename)

        # Write pages (with path safety check)
        output_paths = []
        blocked_paths = []
        wiki_root = Path(self.wiki.project_path) / "wiki"
        for block in page_blocks:
            # Path safety: reject any path trying to escape wiki/
            if not is_safe_ingest_path(block.path):
                blocked_paths.append(block.path)
                continue
            # Strip 'wiki/' prefix if LLM included it (avoid wiki/wiki/ nesting)
            clean_path = block.path
            if clean_path.startswith("wiki/"):
                clean_path = clean_path[5:]
            full_path = wiki_root / clean_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(sanitize_page_content(block.content), encoding="utf-8")
            output_paths.append(clean_path)

        # Copy images if any
        self._copy_images(source_path)

        # Update index, overview, and log
        self.wiki.update_index()
        self.wiki.update_overview()

        # Update ingest log
        self._append_log(filename, analysis, output_paths)

        # Auto-flag review items for low-confidence or ambiguous extractions
        review_items = []
        try:
            from wiki_cli.core.review import ReviewSystem
            review = ReviewSystem(str(self.wiki.project_path))
            source_slug = Path(source_path).stem
            review_items = review.flag_ingest_items(analysis, source_slug)
        except Exception:
            pass

        # Save cache
        self.cache.save(filename, source_content, output_paths)

        # Combine parser warnings (H2/H6) and blocked paths
        all_warnings = gen_warnings[:]
        for p in blocked_paths:
            all_warnings.append(f"Blocked unsafe path: {p}")

        return {
            "status": "ingested",
            "filename": filename,
            "output_paths": output_paths,
            "analysis": analysis,
            "review_items": len(review_items),
            "warnings": all_warnings,
            "blocked_paths": blocked_paths,
        }

    def _append_log(self, filename: str, analysis: dict, output_paths: list[str]):
        """Append to ingest log."""
        log_path = Path(self.wiki.project_path) / ".llm-wiki" / "ingest-log.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "filename": filename,
            "title": analysis.get("title", ""),
            "tags": analysis.get("tags", []),
            "pages": output_paths,
            "confidence": analysis.get("confidence", 0),
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── Helper ──────────────────────────────────────────────────────────────────

def _extract_json_by_braces(text: str) -> str | None:
    """Extract a JSON object by brace counting (handles truncated responses).

    Finds the first '{' and matches braces until we have a balanced closing '}'.
    If the text is truncated mid-content, this returns the largest balanced prefix.
    Returns None if no opening brace is found.
    """
    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    end = start
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    if depth == 0:
        return text[start:end]
    return None
