"""WikiManager - Core wiki management engine.

Directory structure:
    project_root/
    ├── schema.md          ← root level
    ├── purpose.md         ← root level
    ├── raw/               ← source documents
    ├── .llm-wiki/         ← config/cache
    └── wiki/              ← ALL wiki pages
        ├── index.md
        ├── log.md
        ├── overview.md
        ├── sources/
        ├── entities/
        ├── concepts/
        ├── queries/
        ├── comparisons/
        └── synthesis/
"""

import json
import os
import re
import unicodedata
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class WikiManager:
    """Manages a local wiki knowledge base with structured page types."""

    VALID_TYPES = ("entity", "concept", "source", "query", "comparison", "synthesis", "overview")
    TYPE_DIRS = {
        "entity": "wiki/entities",
        "concept": "wiki/concepts",
        "source": "wiki/sources",
        "query": "wiki/queries",
        "comparison": "wiki/comparisons",
        "synthesis": "wiki/synthesis",
    }

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()

    # ── Initialization ──────────────────────────────────────────────────

    def init_wiki(self, template: str = "research") -> Dict[str, Any]:
        """Create the full wiki directory structure and core files.

        Create the full wiki directory structure and core files:
        - schema.md at PROJECT ROOT
        - purpose.md at PROJECT ROOT
        - wiki/* subdirectories
        """
        created: List[str] = []

        # Get template-specific extra directories
        self._current_template = template
        template_config = self._get_template(template)
        extra_dirs = template_config.get("extra_dirs", [])

        # Directories (base structure + template extras)
        for rel in [
            "raw",
            "raw/sources",
            "raw/assets",
            "wiki",
            "wiki/entities",
            "wiki/concepts",
            "wiki/sources",
            "wiki/queries",
            "wiki/comparisons",
            "wiki/synthesis",
            *extra_dirs,
            ".llm-wiki",
            ".llm-wiki/chats",
            ".llm-wiki/assets/images",
        ]:
            d = self.project_path / rel
            d.mkdir(parents=True, exist_ok=True)
            created.append(rel + "/")

        # project.json (id + createdAt in milliseconds)
        proj_file = self.project_path / ".llm-wiki" / "project.json"
        if not proj_file.exists():
            project_id = str(uuid.uuid4())
            created_ms = int(datetime.now().timestamp() * 1000)
            proj_file.write_text(json.dumps({"id": project_id, "createdAt": created_ms}, indent=2) + "\n")
            created.append(".llm-wiki/project.json")
        else:
            proj_file_data = json.loads(proj_file.read_text())
            project_id = proj_file_data.get("id", proj_file_data.get("uuid", str(uuid.uuid4())))

        today = datetime.now().strftime("%Y-%m-%d")

        # .obsidian/ config (app.json + appearance.json + core-plugins.json)
        obsidian_dir = self.project_path / ".obsidian"
        obsidian_dir.mkdir(parents=True, exist_ok=True)

        obsidian_app = obsidian_dir / "app.json"
        if not obsidian_app.exists():
            obsidian_app.write_text(
                '{\n'
                '  "attachmentFolderPath": "raw/assets",\n'
                '  "userIgnoreFilters": [".cache", ".llm-wiki", ".superpowers"],\n'
                '  "useMarkdownLinks": false,\n'
                '  "newLinkFormat": "shortest",\n'
                '  "showUnsupportedFiles": false\n'
                '}\n'
            )
            created.append(".obsidian/app.json")

        obsidian_appearance = obsidian_dir / "appearance.json"
        if not obsidian_appearance.exists():
            obsidian_appearance.write_text(
                '{\n'
                '  "baseFontSize": 16,\n'
                '  "theme": "obsidian"\n'
                '}\n'
            )
            created.append(".obsidian/appearance.json")

        obsidian_plugins = obsidian_dir / "core-plugins.json"
        if not obsidian_plugins.exists():
            obsidian_plugins.write_text(
                '[\n'
                '  "file-explorer",\n'
                '  "global-search",\n'
                '  "switcher",\n'
                '  "graph",\n'
                '  "backlink",\n'
                '  "outgoing-link",\n'
                '  "tag-pane",\n'
                '  "page-preview",\n'
                '  "starred",\n'
                '  "outline",\n'
                '  "word-count",\n'
                '  "editor-status"\n'
                ']\n'
            )
            created.append(".obsidian/core-plugins.json")

        # schema.md at PROJECT ROOT (not in wiki/)
        schema = self.project_path / "schema.md"
        if not schema.exists():
            schema.write_text(self._template_schema(today))
            created.append("schema.md")

        # purpose.md at PROJECT ROOT (not in wiki/)
        purpose = self.project_path / "purpose.md"
        if not purpose.exists():
            purpose.write_text(template_config["purpose"])
            created.append("purpose.md")

        # wiki/index.md (pre-create section headers)
        index = self.project_path / "wiki" / "index.md"
        if not index.exists():
            index.write_text(
                "# Wiki Index\n\n"
                "## Entities\n\n"
                "## Concepts\n\n"
                "## Sources\n\n"
                "## Queries\n\n"
                "## Comparisons\n\n"
                "## Synthesis\n"
            )
            created.append("wiki/index.md")

        # wiki/log.md
        log = self.project_path / "wiki" / "log.md"
        if not log.exists():
            log.write_text("# Research Log\n\n")
            created.append("wiki/log.md")

        # wiki/overview.md (H1 heading)
        overview = self.project_path / "wiki" / "overview.md"
        if not overview.exists():
            overview.write_text(
                "---\n"
                "type: overview\n"
                "title: Project Overview\n"
                "tags: []\n"
                "related: []\n"
                "---\n\n"
                "# Overview\n\n"
                "<!-- Provide a high-level summary of what this wiki covers and its current state. Update regularly as understanding deepens. -->\n"
            )
            created.append("wiki/overview.md")

        # AGENTS.md at project root (agent operating rules)
        agents_file = self.project_path / "AGENTS.md"
        if not agents_file.exists():
            agents_src = Path(__file__).parent.parent / "references" / "AGENTS.md"
            if agents_src.exists():
                agents_file.write_text(agents_src.read_text(encoding="utf-8"), encoding="utf-8")
                created.append("AGENTS.md")

        self.append_log("init", "wiki", f"Wiki initialized (template={template})")

        return {"project_id": project_id, "created": created}

    # ── Read / Write ────────────────────────────────────────────────────

    def read_page(self, slug: str) -> Optional[Dict[str, Any]]:
        """Read a wiki page by slug."""
        path = self._find_page(slug)
        if path is None:
            return None
        raw = path.read_text(encoding="utf-8")
        frontmatter, content = self._parse_frontmatter(raw)
        return {"frontmatter": frontmatter, "content": content, "path": str(path)}

    def write_page(
        self,
        slug: str,
        page_type: str,
        title: str,
        content: str,
        **extra_fm,
    ) -> str:
        """Create or overwrite a wiki page. Returns the file path.

        Frontmatter format:
        - type, title, tags, related, sources, created, updated (all pages)
        - authors, year, url, venue (source pages only)
        """
        if page_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid page type '{page_type}'. Must be one of {self.VALID_TYPES}")

        today = datetime.now().strftime("%Y-%m-%d")
        tags = extra_fm.pop("tags", [])
        related = extra_fm.pop("related", [])
        sources = extra_fm.pop("sources", [])
        created = extra_fm.pop("created", today)
        updated = today

        if page_type == "source":
            authors = extra_fm.pop("authors", [])
            year = extra_fm.pop("year", "")
            url = extra_fm.pop("url", "")
            venue = extra_fm.pop("venue", "")
            fm = self._make_source_frontmatter(
                title, tags, related, sources, created, updated,
                authors, year, url, venue
            )
        else:
            fm = self._make_frontmatter(
                page_type, title, tags, related, sources, created, updated
            )

        body = fm + "\n" + content

        dest_dir = self.TYPE_DIRS.get(page_type, "wiki")
        path = self.project_path / dest_dir / f"{slug}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

        self.append_log("write", slug, f"Wrote {page_type} page: {title}")
        return str(path)

    def write_raw_file(self, filename: str, content: str) -> str:
        """Write a source document to raw/ directory."""
        path = self.project_path / "raw" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return str(path)

    def update_page(self, slug: str, content: str | None = None, **fm_updates) -> str | None:
        """Incrementally update an existing wiki page.

        Reads the current page, merges new frontmatter fields, optionally
        replaces the content, and writes it back.

        Parameters
        ----------
        slug : str
            Page slug to update.
        content : str or None
            If provided, replaces the entire body content.
            If None, the existing content is preserved.
        **fm_updates
            Frontmatter fields to merge (e.g. tags=[], related=[]).
            List fields (tags, related, sources) are *merged* (union),
            not replaced. Scalar fields are overwritten.

        Returns
        -------
        str or None
            The file path if updated, None if the page doesn't exist.
        """
        path = self._find_page(slug)
        if path is None:
            return None

        raw = path.read_text(encoding="utf-8")
        fm, old_content = self._parse_frontmatter(raw)

        new_content = content if content is not None else old_content

        list_keys = {"tags", "related", "sources"}
        for key, val in fm_updates.items():
            if key in list_keys and isinstance(val, list):
                existing = fm.get(key, [])
                if isinstance(existing, str):
                    existing = [existing]
                merged = list(set(str(e) for e in existing) | set(str(v) for v in val))
                fm[key] = merged
            else:
                fm[key] = val

        if "updated" not in fm_updates:
            fm["updated"] = datetime.now().strftime("%Y-%m-%d")

        page_type = fm.get("type", "entity")
        title = fm.get("title", slug)
        tags = fm.get("tags", [])
        related = fm.get("related", [])
        sources = fm.get("sources", [])
        created = fm.get("created", fm["updated"])
        updated = fm["updated"]

        if page_type == "source":
            fm_text = self._make_source_frontmatter(
                title, tags, related, sources, created, updated,
                fm.get("authors", []), fm.get("year", ""),
                fm.get("url", ""), fm.get("venue", ""),
            )
        else:
            fm_text = self._make_frontmatter(
                page_type, title, tags, related, sources, created, updated,
            )

        path.write_text(fm_text + "\n" + new_content, encoding="utf-8")
        self.append_log("update", slug, f"Updated page: {title}")
        return str(path)

    def delete_page(self, slug: str) -> bool:
        """Delete a wiki page by slug.

        Returns True if the page was found and deleted, False otherwise.
        Also removes the page from the cache if present.
        """
        path = self._find_page(slug)
        if path is None:
            return False

        title = slug
        fm, _ = self._parse_frontmatter(path.read_text(encoding="utf-8"))
        title = fm.get("title", slug)

        path.unlink()

        self.append_log("delete", slug, f"Deleted page: {title}")
        return True

    def move_page(self, old_slug: str, new_slug: str) -> str | None:
        """Rename a wiki page (move to a new slug).

        Parameters
        ----------
        old_slug : str
            Current slug of the page.
        new_slug : str
            Desired new slug (kebab-case).

        Returns
        -------
        str or None
            New file path if successful, None if the page doesn't exist.
        """
        path = self._find_page(old_slug)
        if path is None:
            return None

        raw = path.read_text(encoding="utf-8")
        fm, content = self._parse_frontmatter(raw)

        fm["title"] = fm.get("title", old_slug)
        today = datetime.now().strftime("%Y-%m-%d")
        fm["updated"] = today

        page_type = fm.get("type", "entity")
        title = fm["title"]
        tags = fm.get("tags", [])
        related = fm.get("related", [])
        sources = fm.get("sources", [])
        created = fm.get("created", today)
        updated = today

        if page_type == "source":
            fm_text = self._make_source_frontmatter(
                title, tags, related, sources, created, updated,
                fm.get("authors", []), fm.get("year", ""),
                fm.get("url", ""), fm.get("venue", ""),
            )
        else:
            fm_text = self._make_frontmatter(
                page_type, title, tags, related, sources, created, updated,
            )

        new_path = path.parent / f"{new_slug}.md"
        new_path.write_text(fm_text + "\n" + content, encoding="utf-8")
        path.unlink()

        self.append_log("move", f"{old_slug} -> {new_slug}", f"Renamed page: {title}")
        return str(new_path)

    # ── Index & Log ─────────────────────────────────────────────────────

    def update_index(self) -> str:
        """Regenerate wiki/index.md from all existing pages.

        Format: section headers per type, - [[slug]] — title
        """
        lines = ["# Wiki Index\n"]

        for ptype, dirname, header in [
            ("entity", "wiki/entities", "Entities"),
            ("concept", "wiki/concepts", "Concepts"),
            ("source", "wiki/sources", "Sources"),
            ("query", "wiki/queries", "Queries"),
            ("comparison", "wiki/comparisons", "Comparisons"),
            ("synthesis", "wiki/synthesis", "Synthesis"),
        ]:
            lines.append(f"## {header}\n")
            dirpath = self.project_path / dirname
            if dirpath.exists():
                files = sorted(dirpath.glob("*.md"))
                for f in files:
                    slug = f.stem
                    fm, _ = self._parse_frontmatter(f.read_text(encoding="utf-8"))
                    title = fm.get("title", slug)
                    lines.append(f"- [[{slug}]] — {title}")
            lines.append("")

        index_path = self.project_path / "wiki" / "index.md"
        index_path.write_text("\n".join(lines), encoding="utf-8")
        return str(index_path)

    def append_log(self, action: str, subject: str, details: str = "") -> None:
        """Append an entry to wiki/log.md.

        Format: ## [YYYY-MM-DD] action | subject
        """
        today = datetime.now().strftime("%Y-%m-%d")
        entry = f"## [{today}] {action} | {subject}\n"
        if details:
            entry += f"- {details}\n"
        entry += "\n"

        log_path = self.project_path / "wiki" / "log.md"
        if not log_path.exists():
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text("# Research Log\n\n", encoding="utf-8")

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    # ── Overview ────────────────────────────────────────────────────────

    def update_overview(self) -> str:
        """Regenerate wiki/overview.md with a summary of all pages."""
        today = datetime.now().strftime("%Y-%m-%d")
        stats = self.get_stats()

        sections = []
        for ptype in ["source", "entity", "concept", "query", "comparison", "synthesis"]:
            count = stats.get(ptype, 0)
            if count == 0:
                continue
            pages = self.list_pages(type=ptype)
            items = ", ".join(f"[[{p['slug']}]]" for p in pages)
            plural = {"entity": "Entities", "concept": "Concepts", "source": "Sources",
                      "query": "Queries", "comparison": "Comparisons", "synthesis": "Synthesis"}
            label = plural.get(ptype, ptype.title() + "s")
            sections.append(f"### {label} ({count})\n{items}\n")

        content = "## Overview\n\n"
        content += f"This wiki contains **{stats['total']}** pages.\n\n"
        if sections:
            content += "\n".join(sections)
        else:
            content += "No pages have been created yet.\n"

        # Overview format (H1 heading)
        fm = (
            "---\n"
            "type: overview\n"
            "title: Project Overview\n"
            "tags: []\n"
            "related: []\n"
            "---\n"
        )
        overview_path = self.project_path / "wiki" / "overview.md"
        overview_path.write_text(fm + "\n# Overview\n\n" + content.replace("## Overview\n\n", ""), encoding="utf-8")
        return str(overview_path)

    # ── Listing & Stats ─────────────────────────────────────────────────

    def list_pages(self, type: Optional[str] = None) -> List[Dict[str, str]]:
        """List all wiki pages, optionally filtered by type."""
        results = []
        types_to_scan = {type: self.TYPE_DIRS[type]} if type and type in self.TYPE_DIRS else self.TYPE_DIRS

        for ptype, dirname in types_to_scan.items():
            dirpath = self.project_path / dirname
            if not dirpath.exists():
                continue
            for f in sorted(dirpath.glob("*.md")):
                slug = f.stem
                fm, _ = self._parse_frontmatter(f.read_text(encoding="utf-8"))
                results.append({
                    "slug": slug,
                    "type": ptype,
                    "title": fm.get("title", slug),
                    "path": str(f),
                })

        return results

    def get_stats(self) -> Dict[str, int]:
        """Return page counts per type plus total."""
        stats: Dict[str, int] = {}
        total = 0
        for ptype, dirname in self.TYPE_DIRS.items():
            dirpath = self.project_path / dirname
            if dirpath.exists():
                count = len(list(dirpath.glob("*.md")))
            else:
                count = 0
            stats[ptype] = count
            total += count
        stats["total"] = total
        return stats

    # ── Schema & Purpose readers ────────────────────────────────────────

    def read_schema(self) -> str:
        """Read schema.md from project root."""
        schema_path = self.project_path / "schema.md"
        if schema_path.exists():
            return schema_path.read_text(encoding="utf-8")
        return ""

    def read_purpose(self) -> str:
        """Read purpose.md from project root."""
        purpose_path = self.project_path / "purpose.md"
        if purpose_path.exists():
            return purpose_path.read_text(encoding="utf-8")
        return ""

    def read_index(self) -> str:
        """Read wiki/index.md."""
        index_path = self.project_path / "wiki" / "index.md"
        if index_path.exists():
            return index_path.read_text(encoding="utf-8")
        return ""

    # ── Utilities ───────────────────────────────────────────────────────

    @staticmethod
    def slugify(name: str) -> str:
        """Convert a name to kebab-case slug.

        Slugify rules:
        - NFKC normalized
        - Lowercased
        - Whitespace to hyphen
        - Keep Unicode letters/digits + hyphens only
        - Truncated to 100 chars
        """
        s = name.strip()
        s = unicodedata.normalize("NFKC", s)
        s = s.lower()
        s = re.sub(r"\s+", "-", s)
        s = re.sub(r"[^\w\-\./]", "", s, flags=re.UNICODE)  # 保留点和斜杠（entity slug需匹配官方名称如claude-2.0）
        s = re.sub(r"-+", "-", s)
        s = s.strip("-")
        s = s[:100]
        return s if s else "query"

    # ── Private helpers ─────────────────────────────────────────────────

    def _find_page(self, slug: str) -> Optional[Path]:
        """Search all type directories for a page by slug."""
        for dirname in self.TYPE_DIRS.values():
            path = self.project_path / dirname / f"{slug}.md"
            if path.exists():
                return path
        path = self.project_path / "wiki" / f"{slug}.md"
        if path.exists():
            return path
        return None

    @staticmethod
    def _parse_frontmatter(raw: str) -> tuple:
        """Parse YAML frontmatter delimited by ---."""
        fm: Dict[str, Any] = {}
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
                        if val.startswith("[") and val.endswith("]"):
                            inner = val[1:-1].strip()
                            val = [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()]
                        fm[key.strip()] = val

        return fm, content

    @staticmethod
    def _make_frontmatter(
        ptype: str, title: str, tags: list, related: list,
        sources: list, created: str, updated: str,
    ) -> str:
        """Generate frontmatter.

        Required fields: type, title, tags, related, sources, created, updated
        """
        tags_str = "[" + ", ".join(str(t) for t in tags) + "]"
        related_str = "[" + ", ".join(str(r) for r in related) + "]"
        sources_str = "[" + ", ".join(f'"{s}"' for s in sources) + "]"
        return (
            "---\n"
            f"type: {ptype}\n"
            f"title: {title}\n"
            f"created: {created}\n"
            f"updated: {updated}\n"
            f"tags: {tags_str}\n"
            f"related: {related_str}\n"
            f"sources: {sources_str}\n"
            "---\n"
        )

    @staticmethod
    def _make_source_frontmatter(
        title: str, tags: list, related: list, sources: list,
        created: str, updated: str,
        authors: list, year: str, url: str, venue: str,
    ) -> str:
        """Generate source page frontmatter with additional fields."""
        tags_str = "[" + ", ".join(str(t) for t in tags) + "]"
        related_str = "[" + ", ".join(str(r) for r in related) + "]"
        sources_str = "[" + ", ".join(f'"{s}"' for s in sources) + "]"
        authors_str = "[" + ", ".join(str(a) for a in authors) + "]"
        return (
            "---\n"
            f"type: source\n"
            f"title: {title}\n"
            f"created: {created}\n"
            f"updated: {updated}\n"
            f"tags: {tags_str}\n"
            f"related: {related_str}\n"
            f"sources: {sources_str}\n"
            f"authors: {authors_str}\n"
            f"year: {year}\n"
            f'url: "{url}"\n'
            f'venue: "{venue}"\n'
            "---\n"
        )

    def _template_schema(self, today: str) -> str:
        """Generate schema.md for current template."""
        return self._get_template(getattr(self, "_current_template", "general"))["schema"]

    # PLACEHOLDER_FOR_TEMPLATE_METHODS
    def _old_template_schema(self, today: str) -> str:
        """UNUSED - kept for reference"""
        return f"""# Wiki Schema — Research Deep-Dive

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| entity | wiki/entities/ | Named things (people, tools, organizations, datasets) |
| concept | wiki/concepts/ | Ideas, techniques, phenomena, frameworks |
| source | wiki/sources/ | Papers, articles, talks, books, blog posts |
| query | wiki/queries/ | Open questions under active investigation |
| comparison | wiki/comparisons/ | Side-by-side analysis of related entities |
| synthesis | wiki/synthesis/ | Cross-cutting summaries and conclusions |
| overview | wiki/ | High-level project summary (one per project) |

## Naming Conventions

- Files: `kebab-case.md`
- Entities: match official name where possible (e.g., `openai.md`, `gpt-4.md`)
- Concepts: descriptive noun phrases (e.g., `chain-of-thought.md`)
- Sources: `author-year-slug.md` (e.g., `wei-2022-cot.md`)
- Queries: question as slug (e.g., `does-scale-improve-reasoning.md`)

## Frontmatter

All pages must include YAML frontmatter:

```yaml
---
type: entity | concept | source | query | comparison | synthesis | overview
title: Human-readable title
tags: []
related: []
sources: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Source pages also include:
```yaml
authors: []
year: YYYY
url: ""
venue: ""
```

## Index Format

`wiki/index.md` lists all pages grouped by type. Each entry:
```
- [[page-slug]] — one-line description
```

## Log Format

`wiki/log.md` records activity in reverse chronological order:
```
## YYYY-MM-DD

- Action taken / finding noted
```

## Cross-referencing Rules

- Use `[[page-slug]]` syntax to link between wiki pages
- Every entity and concept should appear in `wiki/index.md`
- Queries link to the sources and concepts they draw on
- Synthesis pages cite all contributing sources via `related:`

## Contradiction Handling

When sources contradict each other:
1. Note the contradiction in the relevant concept or entity page
2. Create or update a query page to track the open question
3. Link both sources from the query page
4. Resolve in a synthesis page once sufficient evidence exists

## Research-Specific Conventions

- Keep the thesis pages updated as evidence accumulates — they are living documents
- Every finding should assess replication status when known
- Confidence levels: low (speculative), medium (some evidence), high (well-established)
"""

    def _get_template(self, template_id: str) -> dict:
        """Return template definition.

        Each template has: schema, purpose, extra_dirs
        """
        templates = {
            "research": {
                "schema": self._schema_research(),
                "purpose": self._purpose_research(),
                "extra_dirs": ["wiki/thesis", "wiki/methodology", "wiki/findings"],
            },
            "reading": {
                "schema": self._schema_reading(),
                "purpose": self._purpose_reading(),
                "extra_dirs": ["wiki/notes"],
            },
            "personal": {
                "schema": self._schema_personal(),
                "purpose": self._purpose_personal(),
                "extra_dirs": ["wiki/habits", "wiki/goals", "wiki/reflections"],
            },
            "business": {
                "schema": self._schema_business(),
                "purpose": self._purpose_business(),
                "extra_dirs": ["wiki/meetings", "wiki/decisions", "wiki/projects", "wiki/stakeholders"],
            },
            "general": {
                "schema": self._schema_general(),
                "purpose": self._purpose_general(),
                "extra_dirs": [],
            },
        }
        return templates.get(template_id, templates["general"])

    def _template_purpose(self, today: str) -> str:
        """Return purpose.md for current template."""
        return self._get_template(getattr(self, "_current_template", "general"))["purpose"]

    # ════════════════════════════════════════════════════════════════════
    # Template definitions
    # ════════════════════════════════════════════════════════════════════

    _BASE_SCHEMA_TYPES = """| entity | wiki/entities/ | Named things (people, tools, organizations, datasets) |
| concept | wiki/concepts/ | Ideas, techniques, phenomena, frameworks |
| source | wiki/sources/ | Papers, articles, talks, books, blog posts |
| query | wiki/queries/ | Open questions under active investigation |
| comparison | wiki/comparisons/ | Side-by-side analysis of related entities |
| synthesis | wiki/synthesis/ | Cross-cutting summaries and conclusions |
| overview | wiki/ | High-level project summary (one per project) |"""

    _BASE_NAMING = """- Files: `kebab-case.md`
- Entities: match official name where possible (e.g., `openai.md`, `gpt-4.md`)
- Concepts: descriptive noun phrases (e.g., `chain-of-thought.md`)
- Sources: `author-year-slug.md` (e.g., `wei-2022-cot.md`)
- Queries: question as slug (e.g., `does-scale-improve-reasoning.md`)"""

    _BASE_FRONTMATTER = """All pages must include YAML frontmatter:

```yaml
---
type: entity | concept | source | query | comparison | synthesis | overview
title: Human-readable title
tags: []
related: []
sources: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Source pages also include:
```yaml
authors: []
year: YYYY
url: ""
venue: ""
```"""

    _BASE_INDEX_FORMAT = """`wiki/index.md` lists all pages grouped by type. Each entry:
```
- [[page-slug]] — one-line description
```"""

    _BASE_LOG_FORMAT = """`wiki/log.md` records activity in reverse chronological order:
```
## YYYY-MM-DD

- Action taken / finding noted
```"""

    _BASE_CROSSREF = """- Use `[[page-slug]]` syntax to link between wiki pages
- Every entity and concept should appear in `wiki/index.md`
- Queries link to the sources and concepts they draw on
- Synthesis pages cite all contributing sources via `related:`"""

    _BASE_CONTRADICTION = """When sources contradict each other:
1. Note the contradiction in the relevant concept or entity page
2. Create or update a query page to track the open question
3. Link both sources from the query page
4. Resolve in a synthesis page once sufficient evidence exists"""

    def _schema_research(self) -> str:
        return f"""# Wiki Schema — Research Deep-Dive

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
{self._BASE_SCHEMA_TYPES}
| thesis | wiki/thesis/ | Working hypothesis and its evolution over time |
| methodology | wiki/methodology/ | Research methods, protocols, and study designs |
| finding | wiki/findings/ | Individual empirical results or observations |

## Naming Conventions

{self._BASE_NAMING}
- Theses: hypothesis as slug (e.g., `scaling-improves-reasoning.md`)
- Methodologies: method name (e.g., `systematic-review.md`, `ablation-study.md`)
- Findings: descriptive slug (e.g., `larger-models-better-few-shot.md`)

## Frontmatter

{self._BASE_FRONTMATTER}

Thesis pages also include:
```yaml
confidence: low | medium | high
status: speculative | supported | refuted | settled
```

Finding pages also include:
```yaml
source: "[[source-slug]]"
confidence: low | medium | high
replicated: true | false | null
```

## Index Format

{self._BASE_INDEX_FORMAT}

## Log Format

{self._BASE_LOG_FORMAT}

## Cross-referencing Rules

{self._BASE_CROSSREF}
- Findings link back to their source via the `source:` frontmatter field
- Thesis pages reference supporting and refuting findings via `related:`
- Methodology pages are cited by the findings that used them

## Contradiction Handling

{self._BASE_CONTRADICTION}

## Research-Specific Conventions

- Keep the thesis pages updated as evidence accumulates — they are living documents
- Every finding should assess replication status when known
- Methodology pages explain the *why* (rationale) not just the *how*
- Distinguish between direct evidence and inference in finding pages
"""

    def _purpose_research(self) -> str:
        return """# Project Purpose — Research Deep-Dive

## Research Question

<!-- State the central question this research aims to answer. Be specific and falsifiable. -->

>

## Hypothesis / Working Thesis

<!-- Your current best guess. This will evolve — update it as evidence accumulates. -->

>

## Background

<!-- What prior work or context motivates this research? What gap does it fill? -->

## Sub-questions

<!-- Break down the main question into tractable sub-questions. -->

1.
2.
3.
4.

## Scope

**In scope:**
-

**Out of scope:**
-

## Methodology

<!-- How will you investigate this? What types of sources or experiments are relevant? -->

-

## Success Criteria

<!-- How will you know when you have a satisfying answer? -->

-

## Current Status

> Not started — update this section as research progresses.
"""

    def _schema_reading(self) -> str:
        return f"""# Wiki Schema — Reading Notes

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
{self._BASE_SCHEMA_TYPES}
| note | wiki/notes/ | Reading notes, quotes, and personal annotations |

## Naming Conventions

{self._BASE_NAMING}
- Notes: descriptive slug (e.g., `key-insight-from-ch3.md`, `connection-to-prior-work.md`)

## Frontmatter

{self._BASE_FRONTMATTER}

Note pages also include:
```yaml
source: "[[source-slug]]"
page: ""
chapter: ""
```

## Index Format

{self._BASE_INDEX_FORMAT}

## Log Format

{self._BASE_LOG_FORMAT}

## Cross-referencing Rules

{self._BASE_CROSSREF}
- Notes link back to their source via `source:` frontmatter
- Notes can link to each other when ideas connect

## Contradiction Handling

{self._BASE_CONTRADICTION}
"""

    def _purpose_reading(self) -> str:
        return """# Project Purpose — Reading Notes

## What are you reading?

<!-- List the books, papers, or articles you are working through. -->

-

## Why?

<!-- What motivated this reading? What do you hope to learn or accomplish? -->

## Key questions to keep in mind while reading

1.
2.
3.

## How will you capture insights?

<!-- e.g., per-chapter notes, thematic collections, quote banks -->

-

## Connections to other work

<!-- How does this reading relate to other projects or knowledge areas? -->

-
"""

    def _schema_personal(self) -> str:
        return f"""# Wiki Schema — Personal Growth

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
{self._BASE_SCHEMA_TYPES}
| habit | wiki/habits/ | Habits you are building or breaking |
| goal | wiki/goals/ | Short-term and long-term goals |
| reflection | wiki/reflections/ | Periodic reflections and journal entries |

## Naming Conventions

{self._BASE_NAMING}
- Habits: descriptive slug (e.g., `morning-journaling.md`, `reduce-screen-time.md`)
- Goals: descriptive slug (e.g., `read-50-books-this-year.md`)
- Reflections: `YYYY-MM-topic.md` (e.g., `2024-03-march-review.md`)

## Frontmatter

{self._BASE_FRONTMATTER}

Habit pages also include:
```yaml
frequency: daily | weekly | monthly
status: building | maintaining | breaking | paused
streak: 0
```

Goal pages also include:
```yaml
status: not-started | in-progress | achieved | abandoned
deadline: YYYY-MM-DD
progress: 0%
```

## Index Format

{self._BASE_INDEX_FORMAT}

## Log Format

{self._BASE_LOG_FORMAT}

## Cross-referencing Rules

{self._BASE_CROSSREF}
- Goals can reference habits they depend on
- Reflections can reference goals and habits being tracked

## Contradiction Handling

{self._BASE_CONTRADICTION}

## Personal Growth Conventions

- Be honest in reflections — this wiki is for you
- Update habit streaks regularly to maintain momentum
- Review goals monthly and adjust as needed
"""

    def _purpose_personal(self) -> str:
        return """# Project Purpose — Personal Growth

## Core Values

<!-- What values or principles guide your growth work? -->

1.
2.
3.

## This Year's Theme

<!-- One phrase or sentence that captures your intention for the year. -->

>
"""

    def _schema_business(self) -> str:
        return f"""# Wiki Schema — Business / Team

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
{self._BASE_SCHEMA_TYPES}
| meeting | wiki/meetings/ | Meeting notes, agendas, and action items |
| decision | wiki/decisions/ | Architectural or strategic decisions (ADR-style) |
| project | wiki/projects/ | Project briefs, status, and retrospectives |
| stakeholder | wiki/stakeholders/ | People, teams, and organisations involved |

## Naming Conventions

{self._BASE_NAMING}
- Meetings: `YYYY-MM-DD-slug.md` (e.g., `2024-03-15-sprint-planning.md`)
- Decisions: `NNN-slug.md` (e.g., `001-adopt-typescript.md`)
- Projects: descriptive slug (e.g., `payments-redesign.md`)
- Stakeholders: name or team in kebab-case (e.g., `alice-chen.md`, `platform-team.md`)

## Frontmatter

{self._BASE_FRONTMATTER}

Meeting pages also include:
```yaml
date: YYYY-MM-DD
attendees: []
action_items: []
```

Decision pages also include:
```yaml
status: proposed | accepted | deprecated | superseded
deciders: []
date: YYYY-MM-DD
supersedes: ""
```

Project pages also include:
```yaml
status: planned | active | on-hold | complete | cancelled
owner: ""
start_date: YYYY-MM-DD
target_date: YYYY-MM-DD
```

## Index Format

{self._BASE_INDEX_FORMAT}

## Log Format

{self._BASE_LOG_FORMAT}

## Cross-referencing Rules

{self._BASE_CROSSREF}
- Meeting notes reference attendees via `attendees:` frontmatter and `[[stakeholder-slug]]` links
- Decision pages link to the meetings where the decision was discussed
- Project pages link to their key decisions via `related:`
- Stakeholder pages list projects and decisions they are involved in

## Contradiction Handling

{self._BASE_CONTRADICTION}

## Business-Specific Conventions

- Write meeting notes during or within 24 hours — memory fades fast
- Action items must have a named owner and due date to be actionable
- Decision pages capture *context and consequences*, not just the decision itself
- Deprecated decisions should link to the decision that superseded them
- Projects should have a retrospective section added on completion
"""

    def _purpose_business(self) -> str:
        return """# Project Purpose — Business / Team

## Business Context

**Organisation / Team:**
**Domain:**
**Time period covered:**

## Objectives

<!-- What are the top-level business objectives this wiki supports? -->

1.
2.
3.

## Key Projects

<!-- High-level list — create detailed pages in wiki/projects/ -->

-

## Key Stakeholders

<!-- Who are the primary people or teams involved? -->

-

## Open Decisions

<!-- Decisions currently in flight — create ADR pages in wiki/decisions/ -->

-

## Metrics / Success Criteria

<!-- How does the team measure progress toward its objectives? -->

-

## Constraints and Risks

<!-- Known constraints (budget, time, org) and risks to track -->

-

## Review Cadence

**Weekly sync notes:**
**Monthly status update:**
**Quarterly retrospective:**
"""

    def _schema_general(self) -> str:
        return f"""# Wiki Schema

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
{self._BASE_SCHEMA_TYPES}

## Naming Conventions

{self._BASE_NAMING}

## Frontmatter

{self._BASE_FRONTMATTER}

## Index Format

{self._BASE_INDEX_FORMAT}

## Log Format

{self._BASE_LOG_FORMAT}

## Cross-referencing Rules

{self._BASE_CROSSREF}

## Contradiction Handling

{self._BASE_CONTRADICTION}
"""

    def _purpose_general(self) -> str:
        return """# Project Purpose

## Goal

<!-- What are you trying to understand or build? -->

## Key Questions

<!-- List the primary questions driving this research -->

1.
2.
3.

## Scope

**In scope:**
-

**Out of scope:**
-

## Thesis

<!-- Your current working hypothesis or conclusion (update as research progresses) -->

> TBD
"""
