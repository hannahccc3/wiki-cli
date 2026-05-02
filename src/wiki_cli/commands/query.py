"""`wiki query` — Query the wiki using semantic or keyword search."""

import json
import sys
from pathlib import Path

import click

from wiki_cli.core.wiki import WikiManager


def _keyword_search(manager: WikiManager, question: str, limit: int) -> list[dict]:
    """Hybrid search: keyword + optional vector semantic search."""
    terms = question.lower().split()
    results = []

    for page in manager.list_pages():
        page_data = manager.read_page(page["slug"])
        if not page_data:
            continue

        text = (
            page_data.get("content", "").lower()
            + " "
            + page_data.get("frontmatter", {}).get("title", "").lower()
            + " "
            + " ".join(page_data.get("frontmatter", {}).get("tags", [])).lower()
        )

        score = sum(1 for t in terms if t in text)
        if score > 0:
            results.append({
                "slug": page["slug"],
                "type": page["type"],
                "title": page["title"],
                "score": float(score),
                "path": page["path"],
                "snippet": page_data.get("content", "")[:200],
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    try:
        from wiki_cli.core.config import Config
        from wiki_cli.core.embedding import EmbeddingClient, VectorStore, search_by_embedding
        cfg = Config.load(".")
        emb_cfg = cfg.embeddings
        if emb_cfg.get("enabled"):
            client = EmbeddingClient(config=emb_cfg)
            store = VectorStore(".")
            vec_results = search_by_embedding(question, client, store, top_k=limit)
            vec_slugs = {r["slug"] for r in vec_results}
            for r in results:
                if r["slug"] in vec_slugs:
                    r["score"] += 5.0
            for vr in vec_results:
                if vr["slug"] not in {r["slug"] for r in results}:
                    page_data = manager.read_page(vr["slug"])
                    if page_data:
                        results.append({
                            "slug": vr["slug"],
                            "type": page_data.get("frontmatter", {}).get("type", "unknown"),
                            "title": page_data.get("frontmatter", {}).get("title", vr["slug"]),
                            "score": vr["score"],
                            "path": str(manager.project_path / "wiki" / vr["slug"]),
                            "snippet": page_data.get("content", "")[:200],
                        })
            results.sort(key=lambda x: x["score"], reverse=True)
    except Exception:
        pass

    return results[:limit]


def _llm_query(manager: WikiManager, question: str, limit: int) -> list[dict]:
    """LLM-powered query: analyze question, find relevant pages, synthesize answer."""
    try:
        from wiki_cli.core.llm import create_llm_client
    except Exception:
        return _keyword_search(manager, question, limit)

    # Gather all pages for context
    pages = manager.list_pages()
    if not pages:
        return []

    # Build context from top pages (by keyword pre-filter)
    keyword_hits = _keyword_search(manager, question, min(limit, len(pages)))

    context_parts = []
    for hit in keyword_hits:
        page_data = manager.read_page(hit["slug"])
        if page_data:
            context_parts.append(
                f"## {hit['title']} (type: {hit['type']}, slug: {hit['slug']})\n"
                f"{page_data.get('content', '')[:2000]}"
            )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are a wiki assistant. Answer the following question using ONLY the wiki content provided below.

Question: {question}

Wiki Content:
{context}

Provide a concise answer. If the wiki doesn't contain enough information, say so.
Also list which wiki pages are most relevant (by slug)."""

    try:
        llm = create_llm_client()
        answer = llm.generate(prompt, system="You are a helpful wiki assistant.")
        click.echo("\n📝 Answer:\n")
        click.echo(answer)
        click.echo()
    except Exception as e:
        click.echo(f"⚠  LLM query failed ({e}), falling back to keyword search.\n")

    return keyword_hits


def query(question: str, limit: int, output_format: str, llm: bool) -> None:
    """Query the wiki for matching documents.

    Searches through all wiki pages by keyword matching and optionally
    uses an LLM to synthesize a comprehensive answer.
    """
    manager = WikiManager(".")

    pages = manager.list_pages()
    if not pages:
        click.echo("⚠  Wiki is empty. Use `wiki ingest <file>` to add documents first.")
        sys.exit(0)

    click.echo(f"🔍 Searching: \"{question}\"")
    click.echo(f"   Corpus: {len(pages)} pages")
    click.echo()

    if llm:
        results = _llm_query(manager, question, limit)
    else:
        results = _keyword_search(manager, question, limit)

    if not results:
        click.echo("❌ No matching documents found.")
        sys.exit(0)

    if output_format == "json":
        click.echo(json.dumps(results, indent=2, ensure_ascii=False))
    elif output_format == "brief":
        for r in results:
            click.echo(f"  [{r['type']}] {r['title']} — score: {r['score']}")
    else:
        # Table format
        click.echo(f"{'Type':<12} {'Score':<6} {'Title':<40} {'Slug'}")
        click.echo("─" * 80)
        for r in results:
            click.echo(f"{r['type']:<12} {r['score']:<6} {r['title'][:38]:<40} {r['slug']}")

    click.echo(f"\n📊 {len(results)} results found.")
