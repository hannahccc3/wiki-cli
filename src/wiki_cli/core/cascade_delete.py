"""
Cascade delete for wiki pages.

When a wiki page is deleted, we must also:
1. Remove its embedding chunks (LanceDB)
2. Remove its media directory (wiki/media/<slug>/) if it exists
3. Strip [[deleted-slug]] / [[deleted-slug|alias]] wikilinks from all other pages
4. Strip deleted slugs from all frontmatter 'related:' arrays
5. Strip entries from wiki/index.md that point at the deleted slug

This mirrors nashsu/llm_wiki's wiki-page-delete.ts cascade logic.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Set


# ── helpers ─────────────────────────────────────────────────────────────────

def _normalize_key(s: str) -> str:
    """Lower-case + strip whitespace/hyphens/underscores.

    Used so that [[alice-chen]] and related: [aliceChen] match
    for the purpose of cross-reference cleanup.
    """
    return s.lower().replace(" ", "").replace("-", "").replace("_", "")


def _slug_from_path(path: Path) -> str:
    """Kebab-case slug from a wiki page path."""
    return path.stem  # e.g. wiki/entities/gpt-4.md → gpt-4


def _extract_title(raw: str) -> str:
    """Extract title from frontmatter or fall back to slug."""
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if line.strip().startswith("title:"):
                    val = line.split(":", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    return ""


def _strip_wikilinks_in_body(content: str, deleted_keys: Set[str]) -> str:
    """Replace [[deleted|alias]] and [[deleted]] with plain text (alias preserved)."""
    def replacer(m: re.Match) -> str:
        inner = m.group(1)
        if "|" in inner:
            slug_part, alias = inner.split("|", 1)
            if _normalize_key(slug_part.strip()) in deleted_keys:
                return alias.strip()
        else:
            if _normalize_key(inner.strip()) in deleted_keys:
                return inner.strip()
        return m.group(0)

    # Match [[slug]] and [[slug|alias]], handles nested brackets carefully
    # [^\\[\]]+ means non-bracket chars (so we don't cross into outer [[ ]])
    return re.sub(r"\[\[([^\[\]|]+(?:\|[^\[\]]+)?)\]\]", replacer, content)


def _parse_frontmatter_related(raw: str) -> list[str]:
    """Parse 'related:' field from raw frontmatter text, return list of slugs."""
    if not raw.startswith("---"):
        return []
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return []
    for line in parts[1].splitlines():
        line = line.strip()
        if line.startswith("related:"):
            val = line.split(":", 1)[1].strip()
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                items = []
                for item in inner.split(","):
                    item = item.strip().strip('"').strip("'")
                    if item:
                        items.append(item)
                return items
            elif val.startswith("-"):
                # Block format:  - slug1\n  - slug2
                items = []
                for ln in parts[1].splitlines():
                    ln = ln.strip()
                    if ln.startswith("-"):
                        item = ln.lstrip("-").strip().strip('"').strip("'")
                        if item:
                            items.append(item)
                return items
    return []


def _rewrite_frontmatter_related(raw: str, deleted_keys: Set[str]) -> str:
    """Remove deleted slugs from frontmatter 'related:' array, return new frontmatter block."""
    if not raw.startswith("---"):
        return raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return raw

    fm_block = parts[1]
    body = parts[2]

    new_fm_lines = []
    in_related_block = False

    for line in fm_block.splitlines():
        stripped = line.strip()

        # Detect inline array: related: [[a]], [[b]]
        if stripped.startswith("related:") and "[[" in stripped:
            val = stripped.split(":", 1)[1].strip()
            if "[[" in val:
                # Format: related: [[slug1]], [[slug2]], ...
                # val looks like "[[gpt-4]], [[gpt-3.5]]"
                inner = val
                kept = []
                for item in inner.split(","):
                    item = item.strip()
                    # Extract slug from [[slug]] or [[slug|alias]]
                    m = re.match(r"\[\[([^\]|]+)", item)
                    if m:
                        slug = m.group(1).strip()
                        if _normalize_key(slug) not in deleted_keys:
                            kept.append(item)
                    elif item and _normalize_key(item) not in deleted_keys:
                        kept.append(item)
                if kept:
                    # Convert each [[slug]] to a quoted YAML string
                    quoted = [f'"{w}"' for w in kept]
                    new_fm_lines.append(f"related: [{', '.join(quoted)}]")
                continue

        # Detect block-format related: start
        if stripped.startswith("related:") and not "[[" in stripped:
            in_related_block = True
            new_fm_lines.append(line)
            val = stripped.split(":", 1)[1].strip()
            if val and val != "[]":
                # Non-empty single-line, not a block — treat as inline
                in_related_block = False
            continue

        if in_related_block:
            if stripped.startswith("-") or stripped.startswith('"') or stripped.startswith("'"):
                item = stripped.lstrip("-").strip().strip('"').strip("'")
                m = re.match(r"\[\[([^\]|]+)", item)
                if m:
                    if _normalize_key(m.group(1)) not in deleted_keys:
                        new_fm_lines.append(line)
                elif item and _normalize_key(item) not in deleted_keys:
                    new_fm_lines.append(line)
                continue
            elif not stripped:
                in_related_block = False
                new_fm_lines.append(line)
                continue
            else:
                in_related_block = False

        new_fm_lines.append(line)

    new_fm_block = "\n".join(new_fm_lines)
    return f"---\n{new_fm_block}\n---" + body


def _clean_index_entry(line: str, deleted_keys: Set[str]) -> str | None:
    """Check if an index.md list line points at a deleted slug. Return None to drop, str to keep."""
    # Format: - [[slug]] — "title"  OR  - [[slug]] — Title
    m = re.match(r"^\s*-\s+\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", line)
    if m:
        slug = m.group(1).strip()
        if _normalize_key(slug) in deleted_keys:
            return None
    return line


def _strip_index_entries(content: str, deleted_keys: Set[str]) -> str:
    """Remove index.md list entries that point at deleted slugs."""
    trailing_newline = content.endswith("\n")
    lines = content.splitlines()
    kept = []
    for line in lines:
        result = _clean_index_entry(line, deleted_keys)
        if result is not None:
            kept.append(result)
    result = "\n".join(kept)
    if trailing_newline:
        result += "\n"
    return result


# ── main cascade ─────────────────────────────────────────────────────────────

def cascade_delete_page(project_path: str | Path, page_path: Path) -> dict:
    """Delete a wiki page with full cascade cleanup.

    Returns a dict with:
      - deleted: list of file paths removed
      - rewritten: number of wiki files cleaned
      - warnings: list of issues encountered
    """
    project = Path(project_path)
    wiki_root = project / "wiki"
    slug = _slug_from_path(page_path)
    slug_key = _normalize_key(slug)

    result = {
        "deleted": [],
        "rewritten": 0,
        "warnings": [],
    }

    # Step 1: Read title before delete (for index cleanup key)
    title = ""
    try:
        title = _extract_title(page_path.read_text(encoding="utf-8"))
    except Exception:
        pass

    # Build deleted key set (slug + title)
    deleted_keys: Set[str] = {slug_key}
    if title:
        deleted_keys.add(_normalize_key(title))

    # Step 2: Delete the page file
    try:
        page_path.unlink()
        result["deleted"].append(str(page_path))
    except Exception as e:
        result["warnings"].append(f"Failed to delete {page_path}: {e}")
        return result

    # Step 3: Delete embedding chunks
    try:
        from wiki_cli.core.embedding import VectorStore
        vs = VectorStore(str(project))
        vs.delete_page(slug)
    except Exception:
        pass  # embedding may not exist

    # Step 4: Delete media directory (only for source pages)
    media_dir = wiki_root / "media" / slug
    if media_dir.exists():
        try:
            import shutil
            shutil.rmtree(media_dir)
        except Exception:
            pass

    # Step 5: Sweep all wiki/*.md files and clean references
    if not wiki_root.exists():
        return result

    deleted_slug_set = {slug_key}
    if title:
        deleted_slug_set.add(_normalize_key(title))

    index_path = wiki_root / "index.md"
    index_content = ""
    if index_path.exists():
        try:
            index_content = index_path.read_text(encoding="utf-8")
        except Exception:
            index_content = ""

    all_md = list(wiki_root.rglob("*.md"))

    for md_file in all_md:
        if str(md_file) in result["deleted"]:
            continue  # already deleted

        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        original = content

        if md_file.name == "index.md":
            # For index.md: clean list entries BEFORE wikilink body strip,
            # so [[slug]] — title format is still recognizable for removal.
            content = _strip_index_entries(content, deleted_keys)

        # Strip wikilinks from body (for all files including index.md)
        content = _strip_wikilinks_in_body(content, deleted_keys)

        # Rewrite frontmatter related: array
        if content.startswith("---"):
            content = _rewrite_frontmatter_related(content, deleted_keys)

        if content != original:
            try:
                md_file.write_text(content, encoding="utf-8")
                result["rewritten"] += 1
            except Exception:
                pass

    return result
