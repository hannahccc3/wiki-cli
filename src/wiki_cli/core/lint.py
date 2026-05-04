"""LintEngine — wiki health checks and auto-fix.

Rules:
  ORPHAN    – page has zero inbound [[wikilinks]] from other pages
  BROKEN    – [[wikilink]] targets a page that doesn't exist
  INDEX     – page is not listed in wiki/index.md
  FM        – frontmatter missing required fields (type, title, created, updated)
  STALE     – 'updated' date is older than 90 days
  XREF      – page has fewer than 2 outbound [[wikilinks]]

Each issue is a dict with keys:
  severity  – "error" | "warning" | "info"
  rule_id   – one of the codes above
  message   – human-readable description
  file      – relative path to the offending file
  suggestion – suggested fix (plain text)
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .wiki import WikiManager

# ── Severity mapping ────────────────────────────────────────────────────
SEVERITY: Dict[str, str] = {
    "ORPHAN": "warning",
    "BROKEN": "error",
    "INDEX": "warning",
    "FM": "error",
    "STALE": "info",
    "XREF": "warning",
}

# Required frontmatter fields for every page.
_REQUIRED_FM_FIELDS = ("type", "title", "created", "updated")

# Days threshold for stale content detection.
_STALE_DAYS = 90

# Minimum number of outbound [[wikilinks]] a page should have.
_MIN_OUTBOUND_LINKS = 2


class LintEngine:
    """Runs structural / content health checks on a wiki project."""

    def __init__(self, wiki_manager: WikiManager) -> None:
        self.wm = wiki_manager
        self.project_path: Path = wiki_manager.project_path

    # ── Special pages excluded from orphan/no-outlinks checks ─────────
    _EXCLUDED_FROM_ORPHAN = {"index", "log"}

    # ── Public API ──────────────────────────────────────────────────────

    def lint(self) -> List[Dict[str, Any]]:
        """Run all checks and return a list of issue dicts."""
        issues: List[Dict[str, Any]] = []
        pages = self._collect_pages()          # slug -> {path, frontmatter, content}
        index_entries = self._index_slugs()     # set of slugs in index.md

        for slug, info in pages.items():
            fm = info["frontmatter"]
            content = info["content"]
            relpath = str(info["path"].relative_to(self.project_path))

            # 1. Frontmatter validation
            issues.extend(self._check_frontmatter(slug, fm, relpath))

            # 2. Index completeness
            issues.extend(self._check_indexed(slug, index_entries, relpath))

            # 3. Stale content
            issues.extend(self._check_stale(slug, fm, relpath))

            # 4. Cross-reference minimum (outbound links) — skip special pages
            if slug not in self._EXCLUDED_FROM_ORPHAN:
                issues.extend(self._check_xref_min(slug, content, relpath))

        # Build global slug set for orphan / broken checks
        # Use lowercase slugs for case-insensitive wikilink matching
        all_slugs_lower = {s.lower() for s in pages.keys()}
        all_slugs_raw = set(pages.keys())
        inbound: Dict[str, int] = {s: 0 for s in all_slugs_raw}

        for slug, info in pages.items():
            targets = self._extract_wikilinks(info["content"])
            for target in targets:
                # Case-insensitive wikilink matching (standard wiki convention)
                target_lower = target.lower()
                if target_lower in all_slugs_lower:
                    # Find the canonical slug (original-case) for this target
                    canonical = next(s for s in all_slugs_raw if s.lower() == target_lower)
                    inbound[canonical] += 1
                else:
                    # 5. Broken wikilink
                    issues.append(self._issue(
                        "BROKEN", str(info["path"].relative_to(self.project_path)),
                        f"Broken [[wikilink]] → [[{target}]] (page does not exist)",
                        f"Create page '{target}' or fix the link",
                    ))

        for slug, count in inbound.items():
            if count == 0 and slug not in self._EXCLUDED_FROM_ORPHAN:
                relpath = str(pages[slug]["path"].relative_to(self.project_path))
                # 6. Orphan page — skip index.md / log.md
                issues.append(self._issue(
                    "ORPHAN", relpath,
                    f"Orphan page '{slug}' — no inbound [[wikilinks]] from other pages",
                    f"Add a [[{slug}]] link from a related page",
                ))

        return issues

    def lint_and_fix(self) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Run lint, then apply safe auto-fixes.

        Returns (issues, fix_descriptions).
        """
        issues = self.lint()
        fixes: List[str] = []

        # Group issues by rule for batch fixes
        by_rule: Dict[str, List[Dict[str, Any]]] = {}
        for iss in issues:
            by_rule.setdefault(iss["rule_id"], []).append(iss)

        # Fix INDEX — add missing pages to index.md
        if "INDEX" in by_rule:
            added = self._fix_index(by_rule["INDEX"])
            fixes.extend(added)

        # Fix FM — fill in missing frontmatter fields with defaults
        if "FM" in by_rule:
            filled = self._fix_frontmatter(by_rule["FM"])
            fixes.extend(filled)

        return issues, fixes

    # ── Page collection helpers ─────────────────────────────────────────

    def _collect_pages(self) -> Dict[str, Dict[str, Any]]:
        """Walk all TYPE_DIRS and return slug → {path, frontmatter, content}."""
        pages: Dict[str, Dict[str, Any]] = {}
        for ptype, dirname in WikiManager.TYPE_DIRS.items():
            dirpath = self.project_path / dirname
            if not dirpath.exists():
                continue
            for md_file in sorted(dirpath.glob("*.md")):
                slug = md_file.stem
                raw = md_file.read_text(encoding="utf-8")
                fm, content = WikiManager._parse_frontmatter(raw)
                pages[slug] = {
                    "path": md_file,
                    "frontmatter": fm,
                    "content": content,
                    "raw": raw,
                }
        return pages

    def _index_slugs(self) -> set[str]:
        """Return the set of slugs that are [[linked]] inside wiki/index.md."""
        index_path = self.project_path / "wiki" / "index.md"
        if not index_path.exists():
            return set()
        raw = index_path.read_text(encoding="utf-8")
        return self._extract_wikilinks(raw)

    # ── Individual checks ───────────────────────────────────────────────

    def _check_frontmatter(
        self, slug: str, fm: Dict[str, Any], relpath: str
    ) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        missing = [f for f in _REQUIRED_FM_FIELDS if f not in fm]
        if missing:
            issues.append(self._issue(
                "FM", relpath,
                f"Missing frontmatter field(s): {', '.join(missing)}",
                f"Add {', '.join(missing)} to the frontmatter block",
            ))
        return issues

    def _check_indexed(
        self, slug: str, index_entries: set[str], relpath: str
    ) -> List[Dict[str, Any]]:
        if slug not in index_entries:
            return [self._issue(
                "INDEX", relpath,
                f"Page '{slug}' is not listed in wiki/index.md",
                f"Add [[{slug}]] to wiki/index.md",
            )]
        return []

    def _check_stale(
        self, slug: str, fm: Dict[str, Any], relpath: str
    ) -> List[Dict[str, Any]]:
        updated_str = fm.get("updated", "")
        if not updated_str:
            return []
        try:
            updated = datetime.strptime(str(updated_str), "%Y-%m-%d")
        except (ValueError, TypeError):
            return []
        if datetime.now() - updated > timedelta(days=_STALE_DAYS):
            days = (datetime.now() - updated).days
            return [self._issue(
                "STALE", relpath,
                f"Page '{slug}' was last updated {days} days ago (>{_STALE_DAYS}d)",
                "Review and refresh this page",
            )]
        return []

    def _check_xref_min(
        self, slug: str, content: str, relpath: str
    ) -> List[Dict[str, Any]]:
        # Exclude self-references from count
        outbound = {t for t in self._extract_wikilinks(content) if t != slug}
        if len(outbound) < _MIN_OUTBOUND_LINKS:
            return [self._issue(
                "XREF", relpath,
                f"Page '{slug}' has only {len(outbound)} outbound [[wikilink(s)]] "
                f"(minimum {_MIN_OUTBOUND_LINKS})",
                "Add more [[wikilink]] references to related pages",
            )]
        return []

    # ── Auto-fix helpers ────────────────────────────────────────────────

    def _fix_index(self, index_issues: List[Dict[str, Any]]) -> List[str]:
        """Rebuild wiki/index.md via WikiManager.update_index()."""
        if not index_issues:
            return []
        self.wm.update_index()
        return [
            f"Rebuilt wiki/index.md to include {len(index_issues)} missing page(s)"
        ]

    def _fix_frontmatter(self, fm_issues: List[Dict[str, Any]]) -> List[str]:
        """Attempt to fill missing frontmatter fields with sensible defaults."""
        fixes: List[str] = []
        today = datetime.now().strftime("%Y-%m-%d")
        for iss in fm_issues:
            relpath = iss["file"]
            full_path = self.project_path / relpath
            if not full_path.exists():
                continue
            raw = full_path.read_text(encoding="utf-8")
            fm, content = WikiManager._parse_frontmatter(raw)
            changed = False
            if "type" not in fm:
                # Infer from directory
                parts = Path(relpath).parts
                fm["type"] = "overview"
                for ptype, dirname in WikiManager.TYPE_DIRS.items():
                    if dirname in parts:
                        fm["type"] = ptype
                        break
                changed = True
            if "title" not in fm:
                fm["title"] = full_path.stem.replace("-", " ").replace("_", " ").title()
                changed = True
            if "created" not in fm:
                fm["created"] = today
                changed = True
            if "updated" not in fm:
                fm["updated"] = today
                changed = True
            if changed:
                # Rebuild the file with the corrected frontmatter
                new_fm = self._rebuild_frontmatter(fm)
                full_path.write_text(new_fm + "\n" + content, encoding="utf-8")
                fixes.append(f"Filled missing frontmatter in {relpath}")
        return fixes

    @staticmethod
    def _rebuild_frontmatter(fm: Dict[str, Any]) -> str:
        """Reconstruct a frontmatter block from a dict."""
        lines = ["---"]
        for key in _REQUIRED_FM_FIELDS:
            if key in fm:
                lines.append(f"{key}: {fm[key]}")
        # Preserve any extra fields
        skip = set(_REQUIRED_FM_FIELDS)
        for key, val in fm.items():
            if key not in skip:
                lines.append(f"{key}: {val}")
        lines.append("---")
        return "\n".join(lines)

    # ── Utilities ───────────────────────────────────────────────────────

    @staticmethod
    def _extract_wikilinks(text: str) -> set[str]:
        """Return the set of [[target]] names in *text*."""
        return set(re.findall(r"\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]", text))

    @staticmethod
    def _issue(rule_id: str, file: str, message: str, suggestion: str) -> Dict[str, Any]:
        return {
            "severity": SEVERITY.get(rule_id, "warning"),
            "rule_id": rule_id,
            "message": message,
            "file": file,
            "suggestion": suggestion,
        }
