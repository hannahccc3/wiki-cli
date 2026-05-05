"""
Merge a wiki page that the LLM just generated with whatever's already on disk.
Solves silent data loss across re-ingests where a second source contributes
content to the same entity/concept page.

Architecture: pure logic, LLM call injected as a parameter.

Three layers of protection:
  1. Frontmatter array fields (sources / tags / related) — always
     union-merged at the application layer regardless of whether
     the LLM is involved. Zero-cost, deterministic.
  2. Body — if old and new bodies differ, ask the LLM to produce
     a coherent merge. Sanity-checked on length and structure
     before accepting.
  3. Locked frontmatter fields (type / title / created) — even if
     the LLM rewrote them, the existing values are forced back.
     type/title shifting breaks wikilinks; created is a one-time stamp.

Fallback: any LLM failure or sanity-check rejection falls back to
the previous (array-merged-frontmatter + new body) behavior, with
an optional backup of the existing content for user recovery.

Reference: nashsu/llm_wiki/src/lib/page-merge.ts
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Callable, Optional

from .sources_merge import (
    merge_array_fields_into_content,
    UNION_FIELDS,
)


# Frontmatter scalar fields whose existing value MUST survive an ingest.
LOCKED_FIELDS = ("type", "title", "created")

# Body length safety threshold. If the LLM's merged body is shorter
# than 70% of the longer of (existing body, incoming body), reject
# the merge — the LLM almost certainly stripped content rather than
# legitimately deduplicating.
BODY_SHRINK_THRESHOLD = 0.7


# ── Types ────────────────────────────────────────────────────────────────

MergeFn = Callable[[str, str, str], str]
"""Signature: merger(existing_content, incoming_content, source_filename) -> merged_content"""


@dataclass
class MergePageOptions:
    source_file_name: str
    page_path: str
    backup: Optional[Callable[[str], None]] = None
    today: Optional[Callable[[], str]] = None

    def today_fn(self) -> str:
        return self.today() if self.today else date.today().isoformat()


# ── Public API ──────────────────────────────────────────────────────────

def merge_page_content(
    new_content: str,
    existing_content: Optional[str],
    merger: MergeFn,
    opts: MergePageOptions,
) -> str:
    """Merge incoming content with the existing on-disk page.

    Returns the final merged content string, which the caller writes
    to disk. Does NOT write — the caller decides when and where.

    Fast paths (no LLM call):
      1. Brand-new page (existing_content is None/empty).
      2. Byte-identical content.
      3. Bodies identical after array-field merge (only frontmatter
         array-fields differed).
    """
    # Fast path 1: brand-new page.
    if not existing_content:
        return new_content

    # Fast path 2: byte-identical.
    if new_content == existing_content:
        return existing_content

    # Step 1 — always-on: union the array frontmatter fields.
    array_merged = merge_array_fields_into_content(
        new_content,
        existing_content,
        UNION_FIELDS,
    )

    # Fast path 3: bodies are identical (only array-fields differed).
    old_body = _body_only(existing_content)
    array_merged_body = _body_only(array_merged)
    if old_body.strip() == array_merged_body.strip():
        return array_merged

    # Step 2 — ask the merger to produce a unified body.
    try:
        llm_output = merger(existing_content, array_merged, opts.source_file_name)
    except Exception as exc:
        _warn(f"LLM merge failed for {opts.page_path}, falling back: {exc}")
        _try_backup(opts, existing_content)
        return array_merged

    # Sanity 1: LLM output must have frontmatter.
    if not _has_frontmatter(llm_output):
        _warn(f"LLM output for {opts.page_path} has no frontmatter — rejecting, falling back")
        _try_backup(opts, existing_content)
        return array_merged

    # Sanity 2: body length. Reject obvious truncation / lazy summary.
    old_body_len = len(old_body)
    new_body_len = len(array_merged_body)
    llm_body_len = len(_body_only(llm_output))
    min_threshold = max(old_body_len, new_body_len) * BODY_SHRINK_THRESHOLD
    if llm_body_len < min_threshold:
        _warn(
            f"LLM merge for {opts.page_path} produced body {llm_body_len} chars, "
            f"below threshold {min_threshold:.0f} — rejecting, falling back"
        )
        _try_backup(opts, existing_content)
        return array_merged

    # Step 3 — apply deterministic post-processing.
    final = llm_output

    # Locked fields: force existing values back.
    old_fm = _parse_frontmatter(existing_content)
    for field in LOCKED_FIELDS:
        existing_value = old_fm.get(field)
        if isinstance(existing_value, str) and existing_value:
            final = _set_frontmatter_scalar(final, field, existing_value)

    # Re-apply union merges on top of the LLM's frontmatter so neither
    # contributor's array values are dropped.
    final = merge_array_fields_into_content(final, array_merged, UNION_FIELDS)

    # Updated is always today on a successful merge.
    final = _set_frontmatter_scalar(final, "updated", opts.today_fn())

    return final


# ── Frontmatter helpers ─────────────────────────────────────────────────

def _has_frontmatter(content: str) -> bool:
    return bool(re.match(r"^---\n", content))


def _body_only(content: str) -> str:
    """Return just the body (strip frontmatter)."""
    fm_match = re.match(r"^---\n[\s\S]*?\n---\n", content)
    return content[fm_match.end() :] if fm_match else content


def _parse_frontmatter(content: str) -> dict[str, str]:
    """Parse frontmatter into a flat dict. Returns {} if no frontmatter."""
    fm_match = re.match(r"^---\n([\s\S]*?)\n---", content)
    if not fm_match:
        return {}
    result: dict[str, str] = {}
    for line in fm_match.group(1).split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ": " in line:
            key, val = line.split(": ", 1)
            result[key.strip()] = val.strip().strip('"').strip("'")
        elif line.startswith("- "):
            pass  # skip list items for now
    return result


def _set_frontmatter_scalar(content: str, field_name: str, value: str) -> str:
    """Set a scalar frontmatter field in-place.

    If the field already exists in the frontmatter, the line is replaced.
    If it doesn't, the field is appended at the end of the frontmatter block.

    Keeps the rest of the document unchanged. Returns content unchanged
    if it has no frontmatter at all.
    """
    fm_match = re.match(r"^(---\n)([\s\S]*?)(\n---)", content)
    if not fm_match:
        return content

    open_delim, fm_body, close_delim = fm_match.group(1), fm_match.group(2), fm_match.group(3)
    escaped_name = re.escape(field_name)
    new_line = f"{field_name}: {value}"

    # Only match scalar form (no '['). Array-form fields are handled by sources_merge.
    line_re = re.compile(rf"^{escaped_name}:\s*(?!\[)[^\n]*", re.MULTILINE)
    if line_re.search(fm_body):
        rewritten = line_re.sub(new_line, fm_body, count=1)
        return f"{open_delim}{rewritten}{close_delim}{content[fm_match.end():]}"

    # Field absent — append.
    rewritten = f"{fm_body}\n{new_line}"
    return f"{open_delim}{rewritten}{close_delim}{content[fm_match.end():]}"


def _warn(msg: str) -> None:
    import sys
    print(f"[page-merge] {msg}", file=sys.stderr)


def _try_backup(opts: MergePageOptions, existing_content: str) -> None:
    if opts.backup:
        try:
            opts.backup(existing_content)
        except Exception as exc:
            _warn(f"backup failed for {opts.page_path}: {exc}")
