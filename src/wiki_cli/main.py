"""wiki-cli — a CLI tool for managing and querying wiki documents."""

import os
from pathlib import Path

import click
from dotenv import load_dotenv


def _load_env() -> None:
    """Load .env from the current working directory or project root."""
    env_path = Path.cwd() / ".env"
    load_dotenv(env_path)


@click.group()
@click.version_option(package_name="wiki-cli")
@click.option("--path", "-p", "wiki_path", default=None,
              type=click.Path(exists=False),
              help="Wiki project directory (default: current directory).")
@click.pass_context
def cli(ctx: click.Context, wiki_path: str | None) -> None:
    """wiki-cli — manage and query wiki documents from the command line."""
    _load_env()
    ctx.ensure_object(dict)
    ctx.obj["wiki_path"] = wiki_path or "."
    if wiki_path and wiki_path != ".":
        target = Path(wiki_path).resolve()
        if target.exists():
            os.chdir(target)


# ── Commands ───────────────────────────────────────────────────────────

@cli.command("init")
@click.option("--template", "-t", default="research",
              type=click.Choice(["research", "reading", "personal", "business", "general"], case_sensitive=False),
              help="Template to use for the new wiki.")
@click.option("--name", "-n", default=None, help="Project name.")
@click.option("--path", "-p", "project_path", default=".", type=click.Path(exists=False),
              help="Directory to initialize.")
def init(template: str, name: str | None, project_path: str) -> None:
    """Initialize a new wiki project in the target directory."""
    from wiki_cli.commands.init_cmd import init as _init
    _init(template=template, name=name, project_path=project_path)


@cli.command("ingest")
@click.argument("file", type=click.Path(exists=True))
@click.option("--collection", "-c", default=None, help="Collection label.")
@click.option("--force", "-f", is_flag=True, default=False, help="Force re-ingestion.")
@click.option("--merge/--no-merge", "merge", default=True, help="Use page-merge when re-ingesting (default: enabled). Disable with --no-merge for faster re-ingest.")
@click.pass_context
def ingest(ctx: click.Context, file: str, collection: str | None, force: bool, merge: bool) -> None:
    """Ingest a single document FILE into the wiki."""
    from wiki_cli.commands.ingest import ingest as _ingest
    _ingest(file=file, collection=collection, force=force, merge=merge, wiki_path=ctx.obj["wiki_path"])


@cli.command("ingest-batch")
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--recursive", "-r", is_flag=True, default=False, help="Scan recursively.")
@click.option("--md-only", is_flag=True, default=False, help="Only ingest .md files.")
@click.option("--collection", "-c", default=None, help="Collection label.")
@click.option("--force", "-f", is_flag=True, default=False, help="Force re-ingestion.")
@click.option("--merge/--no-merge", "merge", default=True, help="Use page-merge when re-ingesting (default: enabled). Disable with --no-merge for faster re-ingest.")
@click.pass_context
def ingest_batch(ctx: click.Context, directory: str, recursive: bool, md_only: bool,
                 collection: str | None, force: bool, merge: bool) -> None:
    """Ingest all documents from DIRECTORY into the wiki."""
    from wiki_cli.commands.ingest import ingest_batch as _ingest_batch
    _ingest_batch(directory=directory, recursive=recursive, md_only=md_only,
                  collection=collection, force=force, merge=merge, wiki_path=ctx.obj["wiki_path"])


@cli.command("query")
@click.argument("question")
@click.option("--limit", "-l", default=10, type=int, help="Max results.")
@click.option("--format", "output_format", default="table",
              type=click.Choice(["table", "json", "brief"], case_sensitive=False),
              help="Output format.")
@click.option("--llm/--no-llm", default=True, help="Use LLM for answering.")
def query(question: str, limit: int, output_format: str, llm: bool) -> None:
    """Query the wiki for matching documents."""
    from wiki_cli.commands.query import query as _query
    _query(question=question, limit=limit, output_format=output_format, llm=llm)


@cli.command("lint")
@click.option("--fix", is_flag=True, default=False, help="Auto-fix issues.")
@click.option("--semantic/--no-semantic", "semantic", default=True,
              help="Run LLM semantic lint (contradictions, stale content). Default: enabled.")
@click.option("--severity", "-s", default="info",
              type=click.Choice(["error", "warning", "info"], case_sensitive=False),
              help="Minimum severity to report.")
@click.option("--format", "output_format", default="text",
              type=click.Choice(["text", "json"], case_sensitive=False),
              help="Output format.")
def lint(fix: bool, semantic: bool, severity: str, output_format: str) -> None:
    """Lint wiki documents for common issues."""
    from wiki_cli.commands.lint_cmd import lint as _lint
    _lint(fix=fix, semantic=semantic, severity=severity, output_format=output_format)


@cli.command("graph")
@click.option("--output", "-o", default=None, type=click.Path(),
              help="Output file path for the graph JSON.")
@click.option("--format", "output_format", default="json",
              type=click.Choice(["json", "dot", "summary"], case_sensitive=False),
              help="Output format.")
def graph(output: str | None, output_format: str) -> None:
    """Generate a link-graph of wiki documents."""
    from wiki_cli.commands.graph_cmd import graph as _graph
    _graph(output=output, output_format=output_format)


@cli.command("list")
@click.option("--type", "-t", "page_type", default=None,
              type=click.Choice(
                  ["entity", "concept", "source", "query", "comparison", "synthesis"],
                  case_sensitive=False),
              help="Filter by page type.")
@click.option("--format", "output_format", default="table",
              type=click.Choice(["table", "json", "brief"], case_sensitive=False),
              help="Output format.")
def list_docs(page_type: str | None, output_format: str) -> None:
    """List all ingested wiki documents."""
    from wiki_cli.commands.index_cmd import list_docs as _list_docs
    _list_docs(page_type=page_type, output_format=output_format)


@cli.command("stats")
@click.option("--format", "output_format", default="text",
              type=click.Choice(["text", "json"], case_sensitive=False),
              help="Output format.")
def stats(output_format: str) -> None:
    """Show statistics about the wiki corpus."""
    from wiki_cli.commands.index_cmd import stats as _stats
    _stats(output_format=output_format)


@cli.command("index")
@click.option("--update", "-u", is_flag=True, default=False,
              help="Regenerate wiki/index.md.")
@click.option("--overview", is_flag=True, default=False,
              help="Also regenerate wiki/overview.md.")
def index(update: bool, overview: bool) -> None:
    """View or update the wiki index."""
    from wiki_cli.commands.index_cmd import index as _index
    _index(update=update, overview=overview)


@cli.command("delete")
@click.argument("slug")
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation.")
@click.pass_context
def delete(ctx: click.Context, slug: str, yes: bool) -> None:
    """Delete a wiki page by slug."""
    from wiki_cli.core.wiki import WikiManager

    manager = WikiManager(ctx.obj["wiki_path"])
    page_data = manager.read_page(slug)
    if not page_data:
        click.echo(f"❌ Page not found: {slug}")
        raise SystemExit(1)

    title = page_data.get("frontmatter", {}).get("title", slug)
    if not yes:
        click.echo(f"⚠  About to delete: {title} ({slug})")
        if not click.confirm("Are you sure?"):
            click.echo("Aborted.")
            return

    deleted = manager.delete_page(slug)
    if deleted:
        manager.update_index()
        click.echo(f"✅ Deleted: {slug} ({title})")
    else:
        click.echo(f"❌ Failed to delete: {slug}")


@cli.command("dedup-detect")
@click.pass_context
def dedup_detect(ctx: click.Context) -> None:
    """Detect potential duplicate entity/concept pages using LLM."""
    from wiki_cli.core.wiki import WikiManager
    import json

    manager = WikiManager(ctx.obj["wiki_path"])
    click.echo("🔍 Scanning for duplicates ...")
    groups = manager.detect_duplicates()
    if not groups:
        click.echo("✅ No duplicates found.")
        return
    click.echo(f"Found {len(groups)} duplicate group(s):\n")
    for i, g in enumerate(groups, 1):
        click.echo(f"  Group {i} [{g['confidence'].upper()}] — {g['reason']}")
        for slug in g["slugs"]:
            click.echo(f"    - {slug}")
        click.echo()


@cli.command("dedup-merge")
@click.argument("slugs", nargs=-1, required=True)
@click.option("--canonical", "-c", required=True, help="Slug to keep as the canonical page.")
@click.pass_context
def dedup_merge(ctx: click.Context, slugs: tuple, canonical: str) -> None:
    """Merge duplicate pages into a single canonical page.

    Example: wiki dedup-merge gpt-4 gpt4 gpt-4o --canonical gpt-4
    """
    from wiki_cli.core.wiki import WikiManager

    manager = WikiManager(ctx.obj["wiki_path"])
    click.echo(f"🔀 Merging {len(slugs)} pages into canonical '{canonical}' ...")
    result = manager.merge_duplicate(list(slugs), canonical)
    click.echo(f"✅ Merge complete:")
    click.echo(f"   Canonical page: {result['canonical']}")
    click.echo(f"   Pages rewritten: {result['rewritten']}")
    click.echo(f"   Pages deleted: {result['deleted']}")
    click.echo(f"   Backup dir: {result['backup_dir']}")


@cli.command("move")
@click.argument("old_slug")
@click.argument("new_slug")
@click.pass_context
def move(ctx: click.Context, old_slug: str, new_slug: str) -> None:
    """Rename a wiki page (change its slug)."""
    from wiki_cli.core.wiki import WikiManager

    manager = WikiManager(ctx.obj["wiki_path"])
    page_data = manager.read_page(old_slug)
    if not page_data:
        click.echo(f"❌ Page not found: {old_slug}")
        raise SystemExit(1)

    title = page_data.get("frontmatter", {}).get("title", old_slug)
    new_path = manager.move_page(old_slug, new_slug)
    if new_path:
        manager.update_index()
        click.echo(f"✅ Moved: {old_slug} → {new_slug} ({title})")
    else:
        click.echo(f"❌ Failed to move: {old_slug}")


@cli.command("serve")
@click.option("--port", "-p", default=8000, type=int, help="Port to listen on.")
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind to.")
def serve(host: str, port: int) -> None:
    """Start a local HTTP server to browse the wiki."""
    from wiki_cli.commands.serve import serve as _serve
    _serve(host=host, port=port)


@cli.command("embed")
@click.option("--all", "embed_all", is_flag=True, default=False, help="Embed all wiki pages.")
@click.option("--slug", default=None, help="Embed a specific page by slug.")
@click.option("--model", default=None, help="Embedding model (default: from config).")
@click.option("--status", "show_status", is_flag=True, default=False, help="Show embedding status.")
@click.pass_context
def embed(ctx: click.Context, embed_all: bool, slug: str | None, model: str | None, show_status: bool) -> None:
    """Manage vector embeddings for semantic search."""
    from wiki_cli.commands.embed_cmd import embed as _embed
    _embed(embed_all=embed_all, slug=slug, model=model, show_status=show_status, wiki_path=ctx.obj["wiki_path"])


@cli.command("research")
@click.argument("question")
@click.option("--topics", "-t", default=3, type=int, help="Number of search topics.")
@click.option("--no-ingest", is_flag=True, default=False, help="Don't auto-ingest results.")
@click.pass_context
def research(ctx: click.Context, question: str, topics: int, no_ingest: bool) -> None:
    """Run deep research on a question using web search."""
    from wiki_cli.commands.research_cmd import research as _research
    _research(question=question, max_topics=topics, auto_ingest=not no_ingest, wiki_path=ctx.obj["wiki_path"])


@cli.command("review")
@click.option("--list", "list_items", is_flag=True, default=False, help="List pending review items.")
@click.option("--stats", "show_stats", is_flag=True, default=False, help="Show review statistics.")
@click.option("--resolve", default=None, help="Resolve a review item by ID.")
@click.option("--action", default="approve", help="Action for resolve (approve/reject/merge/edit/verify).")
@click.option("--retry-failed", is_flag=True, default=False, help="Retry all failed ingest items.")
@click.pass_context
def review(ctx: click.Context, list_items: bool, show_stats: bool, resolve: str | None, action: str, retry_failed: bool) -> None:
    """Manage review queue and flagged items."""
    from wiki_cli.commands.review_cmd import review as _review
    _review(list_items=list_items, show_stats=show_stats, resolve=resolve, action=action, retry_failed=retry_failed, wiki_path=ctx.obj["wiki_path"])


@cli.command("mcp")
def mcp() -> None:
    """Start the MCP (Model Context Protocol) server."""
    from wiki_cli.mcp.server import run_mcp
    run_mcp()


@cli.command("setup")
def setup() -> None:
    """Interactive setup wizard for creating or updating a wiki knowledge base."""
    from wiki_cli.commands.setup_cmd import setup_wizard
    setup_wizard()


if __name__ == "__main__":
    cli()
