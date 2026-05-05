"""
Frontmatter array-field merging during ingest.

Originally written for the `sources:` field alone — re-ingesting a page
from a second source would clobber `sources: [...]` to a single entry,
silently losing the first source's contribution. The fix unions old and
new values before writing.

Generalized to handle any frontmatter array field (sources, tags, related):
the same loss-on-clobber pattern applied to tags and related too.

Reference: nashsu/llm_wiki/src/lib/sources-merge.ts
"""

from __future__ import annotations
import re
from typing import Final


# Frontmatter array fields that are union-merged (not overwritten).
UNION_FIELDS: Final[tuple[str, ...]] = ("sources", "tags", "related")


# ── Generic helpers ────────────────────────────────────────────────────

def parse_frontmatter_array(content: str, field_name: str) -> list[str]:
    """Extract a frontmatter array field by name.

    Handles both:
      - inline form:    `name: ["a", "b"]` or `name: [a, b]`
      - block form:     `name:\\n  - a\\n  - b`

    Strips quotes (single or double) from items. Returns [] for missing
    field, malformed parse, or content with no frontmatter.
    """
    fm_match = re.match(r"^---\n([\s\S]*?)\n---", content)
    if not fm_match:
        return []
    fm = fm_match.group(1)

    escaped_name = re.escape(field_name)

    # Block form: key:\n  - value\n  - value
    block_re = re.compile(
        rf"^{escaped_name}:\s*\n((?:[ \t]+-\s+.+\n?)+)",
        re.MULTILINE,
    )
    block = block_re.search(fm)
    if block:
        out: list[str] = []
        for line in block.group(1).split("\n"):
            m = re.match(r"^\s+-\s+[\"']?(.+?)[\"']?\s*$", line)
            if m and m.group(1):
                out.append(m.group(1).strip())
        return out

    # Inline form: key: ["a", "b"] or key: [a, b]
    inline_re = re.compile(rf"^{escaped_name}:\s*\[([^\]]*)\]", re.MULTILINE)
    inline = inline_re.search(fm)
    if not inline:
        return []
    body = inline.group(1).strip()
    if not body:
        return []
    return [
        s.strip().strip('"').strip("'")
        for s in body.split(",")
        if s.strip()
    ]


def write_frontmatter_array(content: str, field_name: str, values: list[str]) -> str:
    """Rewrite (or insert) a frontmatter array field.

    Preserves all other frontmatter lines and order. Returns content
    unchanged if the input has no frontmatter at all.

    Always emits the inline form `name: ["a", "b"]` so downstream
    parsers see a consistent shape regardless of the original input.
    """
    fm_match = re.match(r"^(---\n)([\s\S]*?)(\n---)", content)
    if not fm_match:
        return content

    open_delim, fm_body, close_delim = fm_match.group(1), fm_match.group(2), fm_match.group(3)
    escaped_name = re.escape(field_name)
    serialized = ", ".join(f'"{s}"' for s in values)
    new_line = f"{field_name}: [{serialized}]"

    # Replace inline form in place.
    inline_re = re.compile(rf"^{escaped_name}:\s*\[[^\]]*\]", re.MULTILINE)
    if inline_re.search(fm_body):
        rewritten = inline_re.sub(new_line, fm_body, count=1)
        return f"{open_delim}{rewritten}{close_delim}{content[fm_match.end():]}"

    # Replace block form in place, normalized to inline.
    block_re = re.compile(
        rf"^{escaped_name}:\s*\n((?:[ \t]+-\s+.+\n?)+)",
        re.MULTILINE,
    )
    if block_re.search(fm_body):
        rewritten = block_re.sub(new_line, fm_body, count=1)
        return f"{open_delim}{rewritten}{close_delim}{content[fm_match.end():]}"

    # Field absent — append at end of frontmatter.
    rewritten = f"{fm_body}\n{new_line}"
    return f"{open_delim}{rewritten}{close_delim}{content[fm_match.end():]}"


def _merge_lists(existing: tuple[str, ...], incoming: tuple[str, ...]) -> list[str]:
    """Union-merge two array values. Case-insensitive dedup; first-seen casing wins."""
    seen: set[str] = set()
    out: list[str] = []
    for s in list(existing) + list(incoming):
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def merge_array_fields_into_content(
    new_content: str,
    existing_content: str | None,
    fields: tuple[str, ...],
) -> str:
    """Multi-field merge entry point.

    For each requested field, union the existing-on-disk value with the
    LLM-emitted new value, and rewrite the new content's frontmatter
    with the merged values.

    Fast-paths:
      - existing_content null/empty → return new_content verbatim
      - existing has no frontmatter at all → return new_content verbatim
      - no field actually changes → return new_content verbatim
    """
    if not existing_content:
        return new_content
    if not re.match(r"^---\n", existing_content):
        return new_content

    result = new_content
    changed = False
    for field in fields:
        old_values = parse_frontmatter_array(existing_content, field)
        if not old_values:
            continue
        new_values = parse_frontmatter_array(result, field)
        merged = _merge_lists(tuple(old_values), tuple(new_values))
        if (
            len(merged) == len(new_values)
            and all(s == new_values[i] for i, s in enumerate(merged))
        ):
            continue
        result = write_frontmatter_array(result, field, merged)
        changed = True
    return result if changed else new_content


# ── Backward-compatible single-field exports ────────────────────────────

def parse_sources(content: str) -> list[str]:
    """Extract `sources: [...]` from a wiki page's frontmatter."""
    return parse_frontmatter_array(content, "sources")


def write_sources(content: str, sources: list[str]) -> str:
    """Rewrite the `sources:` field."""
    return write_frontmatter_array(content, "sources", sources)


def merge_sources_lists(existing: tuple[str, ...], incoming: tuple[str, ...]) -> list[str]:
    """Merge two source lists (case-insensitive dedup, first-seen casing wins)."""
    return _merge_lists(existing, incoming)


def merge_sources_into_content(new_content: str, existing_content: str | None) -> str:
    """Sources-only convenience wrapper for merge_array_fields_into_content."""
    return merge_array_fields_into_content(new_content, existing_content, ("sources",))
