"""`wiki research` — Deep research with web search."""

import click

from wiki_cli.core.llm import create_llm_client
from wiki_cli.core.research import DeepResearch
from wiki_cli.core.wiki import WikiManager


def research(question: str, max_topics: int = 3, auto_ingest: bool = True, wiki_path: str = ".") -> None:
    click.echo(f"🔬 Deep Research: {question}")
    click.echo(f"   Topics: {max_topics}, Auto-ingest: {auto_ingest}")
    click.echo()

    manager = WikiManager(wiki_path)
    llm = create_llm_client(wiki_path)
    engine = DeepResearch(llm, manager)

    click.echo("📡 Generating search topics...")
    result = engine.research(question, max_topics=max_topics, auto_ingest=auto_ingest)

    click.echo(f"📋 Search topics:")
    for t in result.get("topics", []):
        click.echo(f"   • {t}")
    click.echo()

    click.echo(f"🌐 Found {len(result.get('search_results', []))} results:")
    for r in result.get("search_results", []):
        click.echo(f"   • {r.get('title', 'Untitled')}")
        click.echo(f"     {r.get('url', '')}")
    click.echo()

    if result.get("synthesis"):
        click.echo("📝 Synthesis:")
        click.echo("─" * 60)
        synthesis = result["synthesis"]
        click.echo(synthesis[:3000])
        if len(synthesis) > 3000:
            click.echo(f"\n... ({len(synthesis) - 3000} more characters)")
    click.echo()

    if result.get("ingested"):
        click.echo("✅ Results auto-ingested into wiki")
    else:
        click.echo("ℹ️  Results not ingested (use --ingest to auto-ingest)")
