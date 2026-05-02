"""`wiki list`, `wiki stats`, `wiki index` — Index and listing commands."""

import json
import sys

import click

from wiki_cli.core.wiki import WikiManager


def list_docs(page_type: str | None, output_format: str) -> None:
    """List all ingested wiki documents."""
    manager = WikiManager(".")
    pages = manager.list_pages(type=page_type)

    if not pages:
        msg = f"No wiki pages found" + (f" of type '{page_type}'" if page_type else "") + "."
        click.echo(f"⚠  {msg}")
        sys.exit(0)

    if output_format == "json":
        click.echo(json.dumps(pages, indent=2, ensure_ascii=False))
    elif output_format == "brief":
        for p in pages:
            click.echo(f"{p['slug']}")
    else:
        # Table format
        click.echo(f"📖 Wiki Pages ({len(pages)} total)\n")
        click.echo(f"{'Slug':<35} {'Type':<12} {'Title'}")
        click.echo("─" * 80)
        for p in pages:
            click.echo(f"{p['slug']:<35} {p['type']:<12} {p['title']}")

    if page_type:
        click.echo(f"\n(filtered by type: {page_type})")


def stats(output_format: str) -> None:
    """Show statistics about the wiki corpus."""
    manager = WikiManager(".")
    page_stats = manager.get_stats()

    if output_format == "json":
        click.echo(json.dumps(page_stats, indent=2))
        return

    total = page_stats.get("total", 0)

    if total == 0:
        click.echo("📊 Wiki Statistics\n")
        click.echo("   No pages found. Run `wiki init` and `wiki ingest` to get started.")
        return

    click.echo(f"📊 Wiki Statistics\n")
    click.echo(f"   Total pages: {total}\n")

    # Per-type breakdown
    type_icons = {
        "entity": "🏷 ",
        "concept": "💡",
        "source": "📄",
        "query": "❓",
        "comparison": "⚖ ",
        "synthesis": "🔬",
    }

    click.echo("   Page Types:")
    for ptype in ["source", "entity", "concept", "query", "comparison", "synthesis"]:
        count = page_stats.get(ptype, 0)
        icon = type_icons.get(ptype, "•")
        bar = "█" * count + "░" * (20 - min(count, 20))
        click.echo(f"   {icon} {ptype:<12} {count:>4}  {bar}")

    # Additional info
    all_pages = manager.list_pages()
    tags = set()
    for p in all_pages:
        page_data = manager.read_page(p["slug"])
        if page_data:
            fm = page_data.get("frontmatter", {})
            page_tags = fm.get("tags", [])
            if isinstance(page_tags, list):
                tags.update(page_tags)

    if tags:
        click.echo(f"\n   Unique tags: {len(tags)}")
        tag_list = sorted(tags)[:15]
        click.echo(f"   Tags: {', '.join(tag_list)}")

    # Coverage analysis
    orphans = []
    for p in all_pages:
        page_data = manager.read_page(p["slug"])
        if page_data:
            content = page_data.get("content", "")
            if "[[" not in content:
                orphans.append(p["slug"])

    if orphans:
        click.echo(f"\n   Orphan pages (no outgoing links): {len(orphans)}")

    click.echo()


def index(update: bool, overview: bool) -> None:
    """View or update the wiki index.

    Without flags, displays the current index.
    With --update, regenerates wiki/index.md from all existing pages.
    """
    manager = WikiManager(".")

    if update:
        index_path = manager.update_index()
        click.echo(f"✅ Index updated: {index_path}")

        if overview:
            overview_path = manager.update_overview()
            click.echo(f"✅ Overview updated: {overview_path}")
        return

    # Display current index
    index_file = manager.project_path / "wiki" / "index.md"
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        click.echo(content)
    else:
        click.echo("⚠  No index found. Run `wiki init` first, or use `wiki index --update` to generate one.")
