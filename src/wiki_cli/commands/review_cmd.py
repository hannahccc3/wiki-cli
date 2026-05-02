"""`wiki review` — Manage review queue and flagged items."""

import click

from wiki_cli.core.review import ReviewSystem, REVIEW_ACTIONS
from wiki_cli.core.queue import IngestQueue


def review(list_items: bool, show_stats: bool, resolve: str | None, action: str, retry_failed: bool, wiki_path: str = ".") -> None:
    system = ReviewSystem(wiki_path)

    if show_stats:
        stats = system.get_stats()
        click.echo("📊 Review Queue Statistics:")
        click.echo(f"   Total:   {stats['total']}")
        click.echo(f"   Pending: {stats['pending']}")
        click.echo(f"   Resolved: {stats['resolved']}")
        click.echo(f"   Dismissed: {stats['dismissed']}")
        if stats.get("by_priority"):
            click.echo(f"   Priority: " + ", ".join(f"{k}={v}" for k, v in stats["by_priority"].items()))
        if stats.get("by_type"):
            click.echo(f"   Types: " + ", ".join(f"{k}={v}" for k, v in stats["by_type"].items()))
        return

    if resolve:
        if system.resolve(resolve, action):
            click.echo(f"✅ Resolved {resolve} with action: {action}")
        else:
            click.echo(f"❌ Review item not found: {resolve}")
        return

    if retry_failed:
        queue = IngestQueue(wiki_path)
        count = queue.retry_failed()
        click.echo(f"✅ Reset {count} failed items to pending")
        return

    if list_items or True:
        items = system.get_pending()
        if not items:
            click.echo("✅ No pending review items.")
            return

        click.echo(f"📋 Pending Review Items ({len(items)}):")
        click.echo("─" * 70)
        for item in items:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(item["priority"], "⚪")
            click.echo(f"{priority_icon} [{item['id'][:30]}]")
            click.echo(f"   Type: {item['type']}, Page: {item['page_slug']}")
            click.echo(f"   Reason: {item['reason']}")
            click.echo(f"   Suggested: {item['suggested_action']} ({REVIEW_ACTIONS.get(item['suggested_action'], '')})")
            if item.get("search_queries"):
                click.echo(f"   Search: {', '.join(item['search_queries'][:2])}")
            click.echo()
