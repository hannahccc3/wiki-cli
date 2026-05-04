"""`wiki lint` — Lint wiki documents for common issues."""

import re
import sys
from pathlib import Path

import click

from wiki_cli.core.wiki import WikiManager


class LintIssue:
    """Represents a single lint issue."""

    def __init__(self, file_path: str, line: int, severity: str, code: str, message: str):
        self.file_path = file_path
        self.line = line
        self.severity = severity  # "error", "warning", "info"
        self.code = code
        self.message = message

    def __str__(self) -> str:
        icon = {"error": "❌", "warning": "⚠ ", "info": "ℹ "}.get(self.severity, "•")
        return f"{icon} {self.file_path}:{self.line} [{self.code}] {self.message}"


def _lint_page(manager: WikiManager, page_info: dict) -> list[LintIssue]:
    """Lint a single wiki page and return a list of issues."""
    issues = []
    path = Path(page_info["path"])
    slug = page_info["slug"]

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        issues.append(LintIssue(str(path), 0, "error", "E001", f"Cannot read file: {e}"))
        return issues

    # --- Frontmatter checks ---
    if not raw.startswith("---"):
        issues.append(LintIssue(str(path), 1, "error", "E100", "Missing frontmatter (must start with ---)"))
    else:
        fm, content = manager._parse_frontmatter(raw)

        if not fm.get("type"):
            issues.append(LintIssue(str(path), 1, "error", "E101", "Missing 'type' in frontmatter"))
        elif fm["type"] not in manager.VALID_TYPES:
            issues.append(LintIssue(
                str(path), 1, "warning", "W101",
                f"Unknown type '{fm['type']}', expected one of {manager.VALID_TYPES}"
            ))

        if not fm.get("title"):
            issues.append(LintIssue(str(path), 1, "warning", "W102", "Missing 'title' in frontmatter"))

        if not fm.get("tags") or fm.get("tags") == "[]":
            issues.append(LintIssue(str(path), 1, "info", "I101", "No tags defined in frontmatter"))

    # --- Content checks ---
    lines = raw.splitlines()

    # Check for empty content after frontmatter
    fm_end = 0
    if raw.startswith("---"):
        second_dash = raw.find("---", 3)
        if second_dash != -1:
            fm_end = raw[:second_dash].count("\n") + 2

    body = "\n".join(lines[fm_end:]).strip()
    if not body:
        issues.append(LintIssue(str(path), len(lines), "warning", "W200", "Page has no content after frontmatter"))

    # Check for broken wiki links [[slug]] or [[slug|display]]
    wiki_links = re.findall(r"\[\[([^\]]+)\]\]", raw)
    for link_text in wiki_links:
        # Handle [[target|display]] format - only use target part
        target = link_text.split('|')[0]
        target_slug = manager.slugify(target)
        if not manager._find_page(target_slug):
            # Only warn if it's not a section link
            if not link_text.startswith("#"):
                # Find line number
                for i, line in enumerate(lines, 1):
                    if f"[[{link_text}]]" in line:
                        issues.append(LintIssue(
                            str(path), i, "warning", "W300",
                            f"Broken wiki link: [[{link_text}]]"
                        ))
                        break

    # Check for very short pages
    word_count = len(body.split())
    if 0 < word_count < 20:
        issues.append(LintIssue(str(path), len(lines), "info", "I200", f"Very short page ({word_count} words)"))

    # Check for duplicate H1 headers
    h1_count = len(re.findall(r"^#\s+", body, re.MULTILINE))
    if h1_count > 1:
        issues.append(LintIssue(str(path), 1, "warning", "W201", f"Multiple H1 headers ({h1_count} found)"))

    # Check filename matches slug convention
    expected_slug = manager.slugify(slug)
    if slug != expected_slug:
        issues.append(LintIssue(
            str(path), 0, "info", "I300",
            f"Filename '{slug}' doesn't match slug convention (expected '{expected_slug}')"
        ))

    return issues


def _fix_issues(manager: WikiManager, page_info: dict, issues: list[LintIssue]) -> int:
    """Attempt to auto-fix issues. Returns number of fixes applied."""
    fixes = 0
    path = Path(page_info["path"])
    raw = path.read_text(encoding="utf-8")

    for issue in issues:
        if issue.code == "E100":
            # Add minimal frontmatter
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            fm = manager._make_frontmatter("entity", page_info["slug"], [], [], today)
            raw = fm + "\n" + raw
            fixes += 1

        elif issue.code == "W102":
            # Add title from slug
            if raw.startswith("---"):
                raw = raw.replace("---\n", f"---\ntitle: {page_info['slug']}\n", 1)
                fixes += 1

        elif issue.code == "W201":
            # Keep only first H1, convert rest to H2
            lines = raw.splitlines()
            h1_seen = False
            new_lines = []
            for line in lines:
                if re.match(r"^#\s+", line):
                    if h1_seen:
                        new_lines.append("#" + line)
                    else:
                        h1_seen = True
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            raw = "\n".join(new_lines)
            fixes += 1

    if fixes > 0:
        path.write_text(raw, encoding="utf-8")

    return fixes


def lint(fix: bool, semantic: bool, severity: str, output_format: str) -> None:
    """Lint wiki documents for common issues.

    Checks frontmatter completeness, broken wiki links, content quality,
    and naming conventions. Use --fix to attempt automatic repairs.
    Use --no-semantic to skip the expensive LLM semantic lint pass.
    """
    manager = WikiManager(".")
    pages = manager.list_pages()

    if not pages:
        click.echo("⚠  No wiki pages found. Run `wiki init` first.")
        sys.exit(0)

    severity_order = {"info": 0, "warning": 1, "error": 2}
    min_severity = severity_order.get(severity, 0)

    all_issues: list[LintIssue] = []
    total_fixes = 0

    for page in pages:
        issues = _lint_page(manager, page)
        filtered = [i for i in issues if severity_order.get(i.severity, 0) >= min_severity]
        all_issues.extend(filtered)

        if fix and filtered:
            n = _fix_issues(manager, page, filtered)
            total_fixes += n

    # ── Semantic lint (LLM-driven, expensive — runs once globally) ────────
    semantic_issues: list[LintIssue] = []
    if semantic:
        from wiki_cli.core.lint import LintEngine
        engine = LintEngine(manager)
        for iss in engine.run_semantic_lint():
            # Convert LintEngine issue dict → LintIssue for unified output
            semantic_issues.append(LintIssue(
                file_path=iss["file"],
                line=0,
                severity=iss["severity"],
                code=iss["rule_id"],
                message=iss["message"],
            ))
        # Filter by minimum severity
        semantic_issues = [i for i in semantic_issues if severity_order.get(i.severity, 0) >= min_severity]
        all_issues.extend(semantic_issues)

    # Output
    if output_format == "json":
        import json
        data = [
            {"file": i.file_path, "line": i.line, "severity": i.severity, "code": i.code, "message": i.message}
            for i in all_issues
        ]
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        if not all_issues:
            click.echo("✅ All wiki pages pass lint checks!")
        else:
            error_count = sum(1 for i in all_issues if i.severity == "error")
            warning_count = sum(1 for i in all_issues if i.severity == "warning")
            info_count = sum(1 for i in all_issues if i.severity == "info")

            click.echo(f"📋 Lint Results ({len(pages)} pages scanned):\n")
            for issue in all_issues:
                click.echo(f"  {issue}")

            click.echo(f"\n📊 Summary: {error_count} errors, {warning_count} warnings, {info_count} info")

            if fix:
                click.echo(f"🔧 Auto-fixed {total_fixes} issues.")

            if error_count > 0:
                sys.exit(1)
