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
from .detect_language import detect_language
from .output_language import build_language_directive
from .page_merge import MergePageOptions, merge_page_content
from .sources_merge import merge_array_fields_into_content, UNION_FIELDS


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


def content_matches_target_language(content: str, target: str) -> bool:
    """Check if the page body matches the target output language.

    Per-file language guard: strips frontmatter + code/math blocks, runs
    detectLanguage on the remainder, and returns whether the content is in
    a language family compatible with the target.

    This catches cases where the LLM follows the format spec but writes
    a page in the wrong language.

    Reference: nashsu/llm_wiki contentMatchesTargetLanguage() ingest.ts:738-760

    Rules:
    - CJK family: Chinese / Japanese / Korean are mutually compatible
    - Non-CJK: reject Arabic, Hindi, Thai, Hebrew (clear cross-family errors)
    - Short content (<20 chars stripped): skip check
    - /entities/ and /sources/ pages: skip check (cite cross-language
      proper nouns legitimately)
    - /concepts/ pages: always check
    """
    import re

    # Strip frontmatter
    fm_end = content.find("\n---", 4)
    body = content[fm_end + 5:] if fm_end > 0 else content

    # Strip code + math blocks
    body = re.sub(r"```[\s\S]*?```", "", body)
    body = re.sub(r"\$\$[\s\S]*?\$\$", "", body)
    body = re.sub(r"\$[^$\n]*\$", "", body)

    sample = body[:1500]
    if len(sample.strip()) < 20:
        return True  # too short to judge

    detected = detect_language(sample)

    # Compatible families: CJK targets accept CJK variants
    cjk = {"Chinese", "Japanese", "Korean"}
    target_is_cjk = target in cjk
    detected_is_cjk = detected in cjk
    if target_is_cjk:
        return detected_is_cjk

    # Non-CJK target: reject clear cross-family mismatches
    return not detected_is_cjk and detected not in (
        "Arabic", "Hindi", "Thai", "Hebrew"
    )


def parse_llm_json(raw: str, purpose: str) -> dict:
    """Parse JSON from LLM output, stripping markdown fences if present.

    The LLM may return fenced or bare JSON. This function handles both,
    and falls back to returning an empty dict with an error field if
    parsing completely fails (rather than crashing the pipeline).

    Args:
        raw: Raw text returned from LLM.generate()
        purpose: Human-readable label for error messages (e.g. "analysis", "page generation")

    Returns:
        Parsed dict. On failure returns {"error": "...", "_raw": raw}
    """
    import json as _json

    text = raw.strip()

    # Strip markdown fences
    if text.startswith("```"):
        lines = text.splitlines()
        # Find the first line with ``` and the last
        first_fence = None
        last_fence = None
        for i, line in enumerate(lines):
            if line.startswith("```") and first_fence is None:
                first_fence = i
            elif line.startswith("```"):
                last_fence = i
        if first_fence is not None and last_fence is not None and last_fence > first_fence:
            text = "\n".join(lines[first_fence + 1 : last_fence])
        elif first_fence is not None:
            # Only opening fence found; strip it
            text = "\n".join(lines[first_fence + 1 :])
        else:
            text = "\n".join(lines)

    text = text.strip()

    # Try direct JSON parse first (most common case)
    try:
        return _json.loads(text)
    except _json.JSONDecodeError:
        pass

    # Try to extract first JSON object/array from the text
    # This handles cases where LLM adds commentary before/after JSON
    for start_idx in range(len(text)):
        if text[start_idx] in ("{", "["):
            break
    else:
        return {
            "error": f"Could not find JSON {purpose} in LLM output",
            "_raw": raw,
        }

    # Try parsing from each '{' or '[' position (brute-force for embedded JSON)
    for i in range(start_idx, len(text)):
        if text[i] not in ("{", "["):
            continue
        try:
            result = _json.loads(text[i:])
            return result
        except _json.JSONDecodeError:
            continue

    return {
        "error": f"Failed to parse JSON {purpose} from LLM output",
        "_raw": raw,
    }


# ── Step 1: Analysis prompt ─────────────────

ANALYSIS_PROMPT = """You are analyzing a source document for a wiki knowledge base.

## Wiki Context

### Schema
{schema}

### Purpose
{purpose}

{language_directive}

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

{language_directive}

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

## Original Source Content (for reference)

{truncated_source}

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

    def __init__(self, wiki_manager, llm_client, merge: bool = True):
        self.wiki = wiki_manager
        self.llm = llm_client
        self.cache = IngestCache(wiki_manager.project_path)
        self.merge = merge

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

    def _step1_analyze(self, source_content: str, filename: str) -> dict:
        """Step 1: LLM analyzes source into structured JSON.

        Ingest behavior:
        - Read schema.md and purpose.md as context
        - Pass source content with filename
        - Truncate to 50,000 chars (aligned with nashsu/llm_wiki)
        - Inject language directive so LLM writes in target language
        """
        # Read schema and purpose as context
        schema = self.wiki.read_schema()
        purpose = self.wiki.read_purpose()

        # Truncate to 50,000 chars (same threshold as nashsu/llm_wiki)
        truncated_source = (
            source_content[:50000] + "\n\n[... content truncated ...]"
            if len(source_content) > 50000
            else source_content
        )

        # Build language directive from source content sample
        lang_directive = build_language_directive(truncated_source)

        prompt = ANALYSIS_PROMPT.format(
            schema=schema[:3000] if schema else "(no schema defined)",
            purpose=purpose[:2000] if purpose else "(no purpose defined)",
            language_directive=lang_directive,
            source=truncated_source,
            filename=filename,
        )
        raw = self.llm.generate(prompt)
        return parse_llm_json(raw, "analysis")

    def _step2_generate_pages(
        self, analysis: dict, filename: str, source_content: str, lang_directive: str = ""
    ) -> list[tuple[str, str]]:
        """Step 2: LLM generates wiki pages from analysis.

        Passes original source content (truncated) so the LLM can reference
        actual passages, not just the analysis summary (nashsu/llm_wiki behavior).
        """
        schema = self.wiki.read_schema()
        purpose = self.wiki.read_purpose()
        index = self.wiki.read_index()
        source_slug = self.wiki.slugify(Path(filename).stem)
        # Truncate source content to 50,000 chars (same threshold as nashsu)
        truncated_source = (
            source_content[:50000] + "\n\n[... content truncated ...]"
            if len(source_content) > 50000
            else source_content
        )
        # Build language directive from source content (cheap, same logic as Step1)
        lang_dir = build_language_directive(truncated_source)

        prompt = PAGE_GENERATION_PROMPT.format(
            language_directive=lang_dir,
            schema=schema[:4000] if schema else "(no schema defined)",
            purpose=purpose[:2000] if purpose else "(no purpose defined)",
            current_index=index[:3000] if index else "(no index yet)",
            analysis=json.dumps(analysis, ensure_ascii=False, indent=2),
            filename=filename,
            source_slug=source_slug,
            truncated_source=truncated_source,
        )
        raw = self.llm.generate(prompt)
        blocks, warnings = self._parse_file_blocks(raw)
        return blocks, warnings

    def _copy_images(self, source_path: str) -> list[str]:
        """Copy associated images to wiki media dir."""
        images = self._find_images(source_path)
        if not images:
            return []
        media_dir = Path(self.wiki.project_path) / "wiki" / "media"
        media_dir.mkdir(parents=True, exist_ok=True)
        copied = []
        for img in images:
            dest = media_dir / img.name
            import shutil
            shutil.copy2(img, dest)
            copied.append(str(dest))
        return copied

    def ingest(self, source_path: str, collection: str | None = None, merge: bool = True) -> dict:
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
        filename = os.path.basename(source_path)
        # Read source (fast, no lock needed)
        source_content = self._read_source(source_path)

        # Check cache (fast, no lock needed)
        cached = self.cache.check(filename, source_content)
        if cached is not None:
            return {
                "status": "cached",
                "filename": filename,
                "output_paths": cached,
                "analysis": None,
            }

        # Step 1 & 2: LLM analysis and page generation — run OUTSIDE the lock
        # to allow concurrent processing of multiple files.
        # Only the final write + index update needs serialization.
        analysis = self._step1_analyze(source_content, filename)
        page_blocks, gen_warnings = self._step2_generate_pages(
            analysis, filename, source_content
        )

        # Now take the lock only for writing and index updates
        with ProjectLock(self.wiki.project_path):
            return self._write_and_finalize(
                source_path, filename, source_content, analysis, page_blocks, gen_warnings
            )

    def _write_and_finalize(
        self, source_path, filename, source_content, analysis, page_blocks, gen_warnings
    ) -> dict:
        """Write pages, update index/log, save cache. Called inside ProjectLock."""
        output_paths: list[str] = []
        blocked_paths: list[str] = []
        hard_failures: list[str] = []
        language_mismatches: list[str] = []
        wiki_root = Path(self.wiki.project_path) / "wiki"

        # Detect target language from source content sample (for language guard)
        target_lang = detect_language(source_content[:2000])

        for block in page_blocks:
            # Path safety: reject any path trying to escape wiki/
            if not is_safe_ingest_path(block.path):
                blocked_paths.append(block.path)
                continue
            # Strip 'wiki/' prefix if LLM included it (avoid wiki/wiki/ nesting)
            clean_path = block.path
            if clean_path.startswith("wiki/"):
                clean_path = clean_path[5:]

            # Language guard: skip /concepts/ pages whose body doesn't match target language.
            # /entities/ and /sources/ are exempt (cite cross-language proper nouns legitimately).
            # nashsu/llm_wiki applies this check in writeFileBlocks.
            is_entity_or_source = (
                clean_path.startswith("entities/")
                or clean_path.startswith("sources/")
            )
            is_log = clean_path.endswith("/log.md") or clean_path == "log.md"
            if (
                not is_log
                and not is_entity_or_source
                and not content_matches_target_language(block.content, target_lang)
            ):
                msg = f'Dropped "{clean_path}" — body language ({detect_language(block.content[:500])}) does not match target {target_lang}'
                language_mismatches.append(msg)
                continue

            # Write the page to disk — with page-merge so re-ingests combine content
            # instead of silently overwriting.
            full_path = wiki_root / clean_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            new_content = sanitize_page_content(block.content)

            # page-merge: if the page already exists, use LLM to merge old + new.
            # Reference: nashsu/llm_wiki writeFileBlocks + page-merge.ts (lines 829-867).
            if full_path.exists() and self.merge:
                try:
                    existing_content = full_path.read_text(encoding="utf-8")
                except OSError:
                    existing_content = ""

                if existing_content:
                    # Build the LLM merger function for this file.
                    def make_merger(path: str):
                        def merger(existing: str, incoming: str, source_fn: str, *, _path: str = path) -> str:
                            merge_prompt = f"""You are a wiki page merger. Two versions of the same wiki page are provided.
Merge them into a single coherent page. Preserve all valuable information from both versions.
Keep the frontmatter from the existing version (type, title, created, updated, sources, tags, related).

Output ONLY the merged wiki page content (frontmatter + body), no explanation.

---EXISTING VERSION---
{existing}
---END EXISTING---

---INCOMING VERSION---
{incoming}
---END INCOMING---"""
                            # Use the same LLM client
                            return self.llm.generate(merge_prompt)
                        return merger

                    merged_content = merge_page_content(
                        new_content=new_content,
                        existing_content=existing_content,
                        merger=make_merger(clean_path),
                        opts=MergePageOptions(
                            source_file_name=filename,
                            page_path=clean_path,
                        ),
                    )
                    new_content = merged_content
            else:
                existing_content = ""

            try:
                full_path.write_text(new_content, encoding="utf-8")
                output_paths.append(clean_path)
            except OSError as e:
                # Disk full, permission denied, I/O error — hard failure, retry later
                hard_failures.append(f"{clean_path}: {e}")
        # Check: did LLM generate a source summary page?
        source_slug = self.wiki.slugify(Path(filename).stem)
        has_source_summary = any(p.startswith(f"sources/{source_slug}") for p in output_paths)

        # Fallback: if LLM missed the source summary, create a minimal one
        if not has_source_summary and output_paths:
            fallback_path = wiki_root / "sources" / f"{source_slug}.md"
            fallback_path.parent.mkdir(parents=True, exist_ok=True)
            date = datetime.now().strftime("%Y-%m-%d")
            analysis_text = ""
            if analysis:
                # Include first 2000 chars of analysis as body
                import json
                try:
                    analysis_text = json.dumps(analysis, ensure_ascii=False, indent=2)[:2000]
                except Exception:
                    analysis_text = str(analysis)[:2000]
            fallback_content = (
                f"---\n"
                f'type: source\n'
                f'title: "{filename}"\n'
                f'created: {date}\n'
                f'updated: {date}\n'
                f'sources: ["{filename}"]\n'
                f"tags: []\n"
                f"related: []\n"
                f"---\n"
                f"\n"
                f"# {filename}\n"
                f"\n"
                f"{analysis_text or '(Analysis not available)'}\n"
            )
            try:
                fallback_path.write_text(fallback_content, encoding="utf-8")
                output_paths.append(f"sources/{source_slug}.md")
            except OSError as e:
                hard_failures.append(f"sources/{source_slug}.md: {e}")

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

        # Save cache only when ALL writes succeeded (no hard failures).
        # If any block failed to write (OS error), skip cache so re-ingest retries.
        if hard_failures:
            import sys
            print(f"⚠ Hard failures during ingest — skipping cache save for '{filename}':", file=sys.stderr)
            for hf in hard_failures:
                print(f"  • {hf}", file=sys.stderr)
        else:
            self.cache.save(filename, source_content, output_paths)

        # Combine parser warnings (H2/H6), blocked paths, hard failures, and language mismatches
        all_warnings = gen_warnings[:]
        for p in blocked_paths:
            all_warnings.append(f"Blocked unsafe path: {p}")
        for hf in hard_failures:
            all_warnings.append(f"Hard failure: {hf}")
        for lm in language_mismatches:
            all_warnings.append(lm)

        return {
            "status": "ingested",
            "filename": filename,
            "output_paths": output_paths,
            "analysis": analysis,
            "review_items": len(review_items),
            "warnings": all_warnings,
            "blocked_paths": blocked_paths,
            "hard_failures": hard_failures,
            "language_mismatches": language_mismatches,
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
