"""
Duplicate-entity / duplicate-concept detection and merge.

Problem: across re-ingests, the LLM names the same underlying topic
differently — "paos" vs "聚磷菌", "dpao" vs "反硝化除磷菌", "vfa" vs
"volatile-fatty-acids". Each becomes a separate page even though they're
the same entity. The page-merge layer only catches *exact* slug collisions;
this module catches the soft-collision case via an LLM-driven self-check.

Three stages:
  1. extractEntitySummaries: walk wiki/entities/ and wiki/concepts/,
     pull (slug, title, description, tags) per page. No LLM.
  2. detectDuplicateGroups: hand the summary list to an LLM, ask it to
     identify groups of slugs likely to refer to the same thing.
     Returns parsed JSON groups with reason + confidence.
  3. mergeDuplicateGroup: given a confirmed group + chosen canonical slug,
     merge bodies (LLM call), union frontmatter array fields
     (deterministic), rewrite every wikilink / related: reference across
     the wiki, and package up a result the caller writes to disk + backs up.

The caller (WikiManager) is responsible for filesystem reads/writes.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional


# ── Types ─────────────────────────────────────────────────────────────────────

@dataclass
class EntitySummary:
    """A lightweight summary of one wiki page."""
    slug: str
    path: str  # relative to project root, e.g. wiki/entities/foo.md
    ptype: str  # entity | concept | source | ...
    title: str
    description: Optional[str] = None  # first non-empty body paragraph, ~200 chars
    tags: list[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class DuplicateGroup:
    """A group of slugs the LLM believes are the same entity."""
    slugs: list[str]
    reason: str
    confidence: str  # "high" | "medium" | "low"


@dataclass
class MergeResult:
    """Everything needed to execute a merge. Caller handles I/O."""
    canonical_content: str  # final content of the canonical page
    canonical_path: str    # path relative to project root
    rewrites: list[dict]   # [{"path": str, "new_content": str}, ...]
    pages_to_delete: list[str]  # relative paths to delete
    backup: list[dict]     # [{"path": str, "content": str}, ...] of all touched files


# ── Prompts ──────────────────────────────────────────────────────────────────

_DETECTOR_SYSTEM = """You are a wiki maintenance assistant. You will receive a list of entity / concept pages from a wiki. Identify groups of slugs that likely refer to the same underlying topic under different names — for example:

- Same name in two languages (English vs Chinese, etc.)
- Plural vs singular form (e.g. "dpao" vs "dpaos")
- Abbreviation vs full form (e.g. "vfa" vs "volatile-fatty-acids")
- Synonyms in the same language
- The same proper noun spelled differently

Output ONLY valid JSON. No prose, no markdown fences, no explanation outside the JSON. The schema is:

{
  "groups": [
    {
      "slugs": ["slug-a", "slug-b"],
      "reason": "Both refer to X; first is English, second is Chinese.",
      "confidence": "high"
    }
  ]
}

Rules:
- Only include groups of 2 or more slugs from the input list.
- "high" = clearly the same entity, only naming differs.
- "medium" = likely the same but context-dependent.
- "low" = uncertain; user should review carefully.
- Never invent slugs that aren't in the input.
- If no duplicates exist, output {"groups": []}.
- Pages of different `type` (e.g. an entity and a concept) usually should NOT be grouped — only group across types when they're unambiguously the same thing."""


_MERGER_SYSTEM = """You are a wiki maintenance assistant. You will be given several wiki pages that all describe the same entity or concept under different names. Merge them into a single coherent wiki page.

Output the COMPLETE merged file (frontmatter + body). The first character of your response MUST be "-" (the opening of "---"). No preamble, no explanation outside the file.

Rules:
- Preserve every distinct factual claim from every input page.
- Eliminate redundancy (don't say the same thing twice across sections).
- Reorganize sections so the structure is logical for the unified topic, not a concatenation of inputs.
- Use [[wikilink]] syntax in the body where the inputs did.
- Frontmatter: keep the standard fields (type, title, created, updated, tags, related, sources). The caller will overwrite sources / tags / related / updated with deterministic unions afterward — your job is to produce a sensible body and reasonable frontmatter shape.
- Pick the most descriptive title. If the inputs use different languages, prefer the language that matches the majority of the body content."""


# ── Stage 1: Extract summaries ──────────────────────────────────────────────

def extract_entity_summaries(project_path: str | Path) -> list[EntitySummary]:
    """Walk wiki/entities/ and wiki/concepts/, build EntitySummary per page.

    No LLM involved. Pure data extraction.
    """
    wiki_root = Path(project_path) / "wiki"
    summaries = []

    for ptype, dirname in [
        ("entity", "entities"),
        ("concept", "concepts"),
    ]:
        dirpath = wiki_root / dirname
        if not dirpath.exists():
            continue
        for f in sorted(dirpath.glob("*.md")):
            summary = _extract_summary(f, ptype, wiki_root)
            if summary:
                summaries.append(summary)

    return summaries


def _extract_summary(path: Path, ptype: str, wiki_root: Path) -> Optional[EntitySummary]:
    """Build one EntitySummary from a file."""
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        return None

    fm, body = _parse_frontmatter(raw)
    title = _fm_string(fm.get("title")) or path.stem
    tags = _fm_array(fm.get("tags", []))
    description = _first_body_paragraph(body)

    rel = path.relative_to(wiki_root)
    return EntitySummary(
        slug=path.stem,
        path=str(rel),
        ptype=ptype,
        title=title,
        description=description,
        tags=tags,
    )


# ── Stage 2: LLM duplicate detection ─────────────────────────────────────────

def detect_duplicate_groups(
    summaries: list[EntitySummary],
    llm_call: Callable[[str, str], str],
    not_duplicates: Optional[list[list[str]]] = None,
) -> list[DuplicateGroup]:
    """Run the LLM duplicate-detector.

    llm_call(system_prompt, user_message) -> LLM response text.
    Returns parsed, validated groups — invalid entries (slugs not in input,
    single-element groups) are filtered out.
    """
    if len(summaries) < 2:
        return []

    user_message = _build_detector_user_message(summaries)
    response = llm_call(_DETECTOR_SYSTEM, user_message)
    parsed = _parse_detector_response(response)

    valid_slugs = {s.slug for s in summaries}
    not_dup_set = {_normalize_group_key(g) for g in (not_duplicates or [])}

    result = []
    for g in parsed:
        # Filter out groups with slugs not in our input
        valid = [s for s in g.slugs if s in valid_slugs]
        if len(valid) < 2:
            continue
        # Filter out known-not-duplicates
        if _normalize_group_key(valid) in not_dup_set:
            continue
        result.append(DuplicateGroup(
            slugs=valid,
            reason=g.reason,
            confidence=g.confidence if g.confidence in ("high", "medium", "low") else "low",
        ))

    return result


def _build_detector_user_message(summaries: list[EntitySummary]) -> str:
    lines = []
    for s in summaries:
        tag_part = f" [{', '.join(s.tags)}]" if s.tags else ""
        desc_part = f" — {s.description}" if s.description else ""
        lines.append(f'- type={s.ptype}, slug={s.slug}, title={json.dumps(s.title)}{tag_part}{desc_part}')
    return f"## Wiki pages to scan ({len(summaries)} entries)\n\n" + "\n".join(lines) + "\n\nReturn duplicate groups as JSON only."


def _parse_detector_response(raw: str) -> list[DuplicateGroup]:
    """Tolerant JSON extraction — handles code fences, prefix/suffix prose."""
    json_text = _extract_first_json_object(raw)
    if not json_text:
        return []
    try:
        parsed = json.loads(json_text)
    except Exception:
        return []
    if not isinstance(parsed, dict):
        return []
    groups_raw = parsed.get("groups", [])
    if not isinstance(groups_raw, list):
        return []

    out = []
    for g in groups_raw:
        if not isinstance(g, dict):
            continue
        slugs_raw = g.get("slugs", [])
        if not isinstance(slugs_raw, list) or len(slugs_raw) < 2:
            continue
        slugs = [s for s in slugs_raw if isinstance(s, str) and s.strip()]
        if len(slugs) < 2:
            continue
        reason = g.get("reason", "") if isinstance(g.get("reason"), str) else ""
        confidence = g.get("confidence", "low") if g.get("confidence") in ("high", "medium", "low") else "low"
        out.append(DuplicateGroup(slugs=slugs, reason=reason, confidence=confidence))
    return out


def _extract_first_json_object(text: str) -> Optional[str]:
    """Find the first balanced {...} substring in arbitrary text."""
    try:
        start = text.index("{")
    except ValueError:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def _normalize_group_key(slugs: list[str]) -> str:
    """Canonical key for a duplicate group — lowercased, sorted, comma-joined."""
    return ",".join(sorted(s.lower() for s in slugs))


# ── Stage 3: Merge a confirmed duplicate group ───────────────────────────────

_FIELDS_TO_UNION = ["sources", "tags", "related"]


def merge_duplicate_group(
    summaries: list[EntitySummary],
    slugs: list[str],
    canonical_slug: str,
    llm_call: Callable[[str, str], str],
    today: Optional[Callable[[], str]] = None,
) -> MergeResult:
    """Compute everything needed to merge a confirmed duplicate group.

    Returns a MergeResult; the CALLER is responsible for:
      - Writing canonical_content to canonical_path
      - Writing each rewrite back to disk
      - Deleting pages in pages_to_delete
      - Storing the backup snapshot

    This split keeps the function testable without touching the filesystem.
    """
    # 1. Load all pages in the group
    group_pages = []
    for s in summaries:
        if s.slug in slugs:
            group_pages.append({"slug": s.slug, "path": s.path})

    if len(group_pages) < 2:
        raise ValueError(f"mergeDuplicateGroup requires at least 2 pages in the group, got {len(group_pages)}")

    canonical = next((p for p in group_pages if p["slug"] == canonical_slug), None)
    if not canonical:
        raise ValueError(f"canonical_slug '{canonical_slug}' not in group: {[p['slug'] for p in group_pages]}")

    # 2. Read all group page contents
    from .wiki import WikiManager
    wiki = WikiManager(".")  # will be overridden by caller passing project path
    # Actually, we need project_path. Let's use a simpler approach: caller passes content dict.
    raise NotImplementedError("Use merge_duplicate_group_with_contents() instead")


def merge_duplicate_group_with_contents(
    group: list[dict],  # [{"slug": str, "path": str, "content": str}]
    canonical_slug: str,
    llm_call: Callable[[str, str], str],
    other_pages: Optional[list[dict]] = None,  # [{"path": str, "content": str}] of all other wiki pages
    today: Optional[str] = None,
) -> MergeResult:
    """Compute merge result given page contents.

    other_pages are used to rewrite cross-references. If None, rewrites will be empty
    (caller can do the sweep separately).

    Caller is responsible for I/O as described in merge_duplicate_group docs.
    """
    if len(group) < 2:
        raise ValueError("group must have at least 2 pages")

    canonical = next((p for p in group if p["slug"] == canonical_slug), None)
    if not canonical:
        raise ValueError(f"canonical_slug '{canonical_slug}' not in group")

    # 1. LLM body merge
    user_message = _build_merger_user_message(group, canonical_slug)
    llm_output = llm_call(_MERGER_SYSTEM, user_message)

    # 2. Deterministic frontmatter union (sources, tags, related)
    merged = llm_output
    for page in group:
        merged = _merge_array_fields(merged, page["content"], list(_FIELDS_TO_UNION))

    # 3. Stamp updated date
    date_str = today or _default_today()
    merged = _set_frontmatter_scalar(merged, "updated", date_str)

    # 4. Cross-reference rewrites: every other wiki page that mentions
    #    a non-canonical slug gets its wikilinks / related entries rewritten.
    slug_redirects: dict[str, str] = {}
    for page in group:
        if page["slug"] != canonical_slug:
            slug_redirects[page["slug"]] = canonical_slug

    rewrites = []
    if other_pages:
        for page in other_pages:
            rewritten = _rewrite_cross_references(page["content"], slug_redirects)
            if rewritten != page["content"]:
                rewrites.append({"path": page["path"], "new_content": rewritten})

    # 5. Backup: all touched files' PRE-merge content
    backup: list[dict] = []
    for page in group:
        backup.append({"path": page["path"], "content": page["content"]})
    for r in rewrites:
        orig = next((p for p in other_pages if p["path"] == r["path"]), None)
        if orig:
            backup.append({"path": orig["path"], "content": orig["content"]})

    # 6. Pages to delete: every group member except canonical
    pages_to_delete = [p["path"] for p in group if p["slug"] != canonical_slug]

    return MergeResult(
        canonical_content=merged,
        canonical_path=canonical["path"],
        rewrites=rewrites,
        pages_to_delete=pages_to_delete,
        backup=backup,
    )


# ── Internal helpers ─────────────────────────────────────────────────────────

def _parse_frontmatter(raw: str) -> tuple[dict, str]:
    """Parse YAML frontmatter. Returns (fm_dict, body)."""
    fm: dict = {}
    content = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            fm_block = parts[1].strip()
            content = parts[2].strip()
            for line in fm_block.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    val = val.strip()
                    key = key.strip()
                    if val.startswith("[") and val.endswith("]"):
                        inner = val[1:-1].strip()
                        val = [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()]
                    fm[key] = val
    return fm, content


def _fm_string(v) -> Optional[str]:
    if isinstance(v, str) and v.strip():
        return v.strip()
    return None


def _fm_array(v) -> list[str]:
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return []


def _first_body_paragraph(body: str, max_len: int = 200) -> Optional[str]:
    """Return the first non-heading, non-table body line, truncated to max_len."""
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("|"):
            continue
        if len(line) > max_len:
            return line[:max_len - 1] + "…"
        return line
    return None


def _build_merger_user_message(group: list[dict], canonical_slug: str) -> str:
    sections = []
    for i, page in enumerate(group):
        sections.append(f"## Page {i + 1} (slug: {page['slug']})\n\n{page['content']}\n")
    return (
        f"These {len(group)} wiki pages have been confirmed to describe the same topic.\n"
        f"Merge them into a single coherent page (canonical slug: \"{canonical_slug}\").\n\n"
        + "\n---\n\n".join(sections)
        + "\n\nNow output the merged file. First character must be `-`."
    )


def _merge_array_fields(merged: str, original: str, fields: list[str]) -> str:
    """For each field in fields, union the values from original into merged's frontmatter."""
    orig_fm, orig_body = _parse_frontmatter(original)
    merg_fm, merg_body = _parse_frontmatter(merged)

    for field in fields:
        orig_vals = _fm_array(orig_fm.get(field, []))
        merg_vals = _fm_array(merg_fm.get(field, []))
        if not orig_vals:
            continue
        # Union: all unique values, case-insensitive dedup, first-seen casing wins
        seen: dict[str, str] = {}
        for v in merg_vals + orig_vals:
            key = v.lower()
            if key not in seen:
                seen[key] = v
        merged_vals = list(seen.values())
        if merged_vals != merg_vals:
            merg_fm[field] = merged_vals

    return _frontmatter_to_string(merg_fm) + "\n" + merg_body


def _set_frontmatter_scalar(content: str, field: str, value: str) -> str:
    """Set or add a scalar frontmatter field."""
    fm, body = _parse_frontmatter(content)
    fm[field] = value
    return _frontmatter_to_string(fm) + "\n" + body


def _frontmatter_to_string(fm: dict) -> str:
    """Serialize a frontmatter dict to a ---...--- string."""
    lines = []
    for key, val in fm.items():
        if isinstance(val, list):
            if val:
                items = ", ".join(f'"{v}"' for v in val)
                lines.append(f"{key}: [{items}]")
            else:
                lines.append(f"{key}: []")
        else:
            lines.append(f"{key}: {val}")
    return "---\n" + "\n".join(lines) + "\n---"


def _rewrite_cross_references(content: str, slug_redirects: dict[str, str]) -> str:
    """Rewrite [[old]] and [[old|alias]] to [[new]] and [[new|alias]] throughout one page."""
    out = content
    for old_slug, new_slug in slug_redirects.items():
        escaped = re.escape(old_slug)
        # Match [[slug]] and [[slug|alias]]
        pattern = rf"\[\[{escaped}(\|[^\]]+)?\]\]"
        replacement = f"[[{new_slug}\\1]]"
        out = re.sub(pattern, replacement, out)

    # Also rewrite frontmatter related: arrays
    fm, body = _parse_frontmatter(out)
    changed = False
    related = _fm_array(fm.get("related", []))
    if related:
        rewritten = [slug_redirects.get(r, r) for r in related]
        # Case-insensitive dedup
        seen: dict[str, str] = {}
        for r in rewritten:
            key = r.lower()
            if key not in seen:
                seen[key] = r
        rewritten = list(seen.values())
        if rewritten != related:
            fm["related"] = rewritten
            changed = True

    if changed:
        out = _frontmatter_to_string(fm) + "\n" + body
    return out


def _normalize_key(s: str) -> str:
    """Lower-case + strip whitespace/hyphens/underscores."""
    return s.lower().replace(" ", "").replace("-", "").replace("_", "")


def _default_today() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")
