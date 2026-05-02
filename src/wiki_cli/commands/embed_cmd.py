"""`wiki embed` — Manage vector embeddings for semantic search."""

import click

from wiki_cli.core.config import Config
from wiki_cli.core.embedding import EmbeddingClient, VectorStore, embed_page, embed_all_pages


def embed(embed_all: bool, slug: str | None, model: str | None, show_status: bool, wiki_path: str = ".") -> None:
    cfg = Config.load(wiki_path)
    emb_cfg = cfg.embeddings

    if not emb_cfg.get("enabled"):
        click.echo("⚠  Embeddings not enabled. Add to wiki-cli.yaml:")
        click.echo("  embeddings:")
        click.echo("    enabled: true")
        click.echo("    base_url: http://localhost:11434/v1")
        click.echo("    model: nomic-embed-text")
        return

    client = EmbeddingClient(config=emb_cfg)
    if model:
        client.model = model
    store = VectorStore(wiki_path)

    if show_status:
        count = store.count()
        click.echo(f"📊 Embedding status:")
        click.echo(f"   Model: {client.model}")
        click.echo(f"   Endpoint: {client.base_url}")
        click.echo(f"   Total chunks: {count}")
        test = client.embed("test")
        if test:
            click.echo(f"   Connection: ✅ (dim={len(test)})")
        else:
            click.echo(f"   Connection: ❌ Failed")
        return

    if embed_all:
        click.echo(f"🔄 Embedding all wiki pages with {client.model}...")
        max_chars = emb_cfg.get("max_chunk_chars", 1000)
        overlap = emb_cfg.get("overlap_chars", 200)
        count = embed_all_pages(wiki_path, client, store, max_chars, overlap)
        click.echo(f"✅ Embedded {count} pages ({store.count()} total chunks)")
        return

    if slug:
        from wiki_cli.core.wiki import WikiManager
        manager = WikiManager(wiki_path)
        page = manager.read_page(slug)
        if not page:
            click.echo(f"❌ Page not found: {slug}")
            return
        title = page.get("frontmatter", {}).get("title", slug)
        content = page.get("content", "")
        click.echo(f"🔄 Embedding: {title} ({slug})...")
        n = embed_page(wiki_path, slug, title, content, client, store)
        click.echo(f"✅ Indexed {n} chunks")
        return

    click.echo("Use --all to embed all pages, or --slug <name> for a specific page.")
