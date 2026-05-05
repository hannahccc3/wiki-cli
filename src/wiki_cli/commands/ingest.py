"""`wiki ingest` and `wiki ingest-batch` — Ingest documents into the wiki."""

import os
import sys
from pathlib import Path

import click

from wiki_cli.core.cache import IngestCache
from wiki_cli.core.ingest import IngestEngine
from wiki_cli.core.llm import create_llm_client
from wiki_cli.core.wiki import WikiManager


def _get_engine(wiki_path: str = ".") -> IngestEngine:
    """Create an IngestEngine with default components."""
    wiki = WikiManager(wiki_path)
    llm = create_llm_client(wiki_path)
    return IngestEngine(wiki, llm)


def ingest(file: str, collection: str | None, force: bool, merge: bool = True, wiki_path: str = ".") -> None:
    """Ingest a single document FILE into the wiki.

    The document is analyzed by the LLM and relevant wiki pages are generated
    automatically using a 2-step Chain-of-Thought process.
    """
    engine = _get_engine(wiki_path)

    if force:
        engine.cache.invalidate(os.path.basename(file))

    click.echo(f"📄 Ingesting: {file}")
    if collection:
        click.echo(f"   Collection: {collection}")

    try:
        result = engine.ingest(file, collection=collection, merge=merge)
    except FileNotFoundError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    except RuntimeError as e:
        click.echo(f"❌ Ingest failed: {e}", err=True)
        sys.exit(1)

    if result["status"] == "cached":
        click.echo(f"⏭  Skipped (cached): {file}")
        click.echo(f"   Existing pages: {', '.join(result['output_paths'])}")
    else:
        click.echo(f"✅ Ingested: {result['filename']}")
        if result.get("analysis"):
            analysis = result["analysis"]
            click.echo(f"   Title: {analysis.get('title', 'N/A')}")
            click.echo(f"   Confidence: {analysis.get('confidence', 'N/A')}")
            click.echo(f"   Summary: {analysis.get('summary', 'N/A')[:120]}")
        click.echo(f"   Generated {len(result['output_paths'])} pages:")
        for p in result["output_paths"]:
            click.echo(f"     • {p}")


def ingest_batch(
    directory: str,
    recursive: bool,
    md_only: bool,
    collection: str | None,
    force: bool,
    merge: bool = True,
    wiki_path: str = ".",
) -> None:
    """Ingest all documents from DIRECTORY into the wiki.

    Supports batch processing with optional recursive scanning and
    file type filtering.
    """
    engine = _get_engine(wiki_path)
    dir_path = Path(directory)

    # Collect files
    if recursive:
        pattern = "*.md" if md_only else "*"
        candidates = sorted(dir_path.rglob(pattern))
    else:
        pattern = "*.md" if md_only else "*"
        candidates = sorted(dir_path.glob(pattern))

    # Filter to supported file types
    supported_ext = {".md", ".txt", ".pdf", ".json", ".csv", ".html", ".rst"}
    files = [
        f for f in candidates
        if f.is_file() and (f.suffix.lower() in supported_ext or not md_only)
    ]

    if not files:
        click.echo(f"⚠  No ingestible files found in {directory}")
        sys.exit(0)

    click.echo(f"📂 Batch ingest from: {directory}")
    click.echo(f"   Found {len(files)} files")
    click.echo(f"   Recursive: {recursive}, MD-only: {md_only}")
    if collection:
        click.echo(f"   Collection: {collection}")
    click.echo()

    succeeded = 0
    skipped = 0
    failed = 0

    for i, fpath in enumerate(files, 1):
        rel = fpath.relative_to(dir_path)
        click.echo(f"[{i}/{len(files)}] {rel} ... ", nl=False)

        if force:
            engine.cache.invalidate(fpath.name)

        try:
            result = engine.ingest(str(fpath), collection=collection, merge=merge)
            if result["status"] == "cached":
                click.echo("⏭ cached")
                skipped += 1
            else:
                click.echo(f"✅ {len(result['output_paths'])} pages")
                succeeded += 1
        except Exception as e:
            click.echo(f"❌ {e}")
            failed += 1

    click.echo()
    click.echo(f"📊 Batch ingest complete:")
    click.echo(f"   ✅ Succeeded: {succeeded}")
    click.echo(f"   ⏭  Skipped:   {skipped}")
    click.echo(f"   ❌ Failed:    {failed}")
