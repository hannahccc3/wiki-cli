"""`wiki graph` — Generate a link-graph of wiki documents."""

import json
import sys
from pathlib import Path

import click

from wiki_cli.core.wiki import WikiManager


def _build_graph(manager: WikiManager) -> dict:
    """Build a graph of wiki pages and their links."""
    import re

    pages = manager.list_pages()
    nodes = []
    edges = []
    edge_set = set()

    slug_set = {p["slug"] for p in pages}

    for page in pages:
        page_data = manager.read_page(page["slug"])
        if not page_data:
            continue

        # Add node
        nodes.append({
            "id": page["slug"],
            "type": page["type"],
            "title": page["title"],
            "path": page["path"],
        })

        # Find wiki links in content
        content = page_data.get("content", "")
        links = re.findall(r"\[\[([^\]]+)\]\]", content)

        for link_text in links:
            target_slug = manager.slugify(link_text)
            if target_slug in slug_set:
                edge_key = (page["slug"], target_slug)
                if edge_key not in edge_set:
                    edge_set.add(edge_key)
                    edges.append({
                        "source": page["slug"],
                        "target": target_slug,
                        "relation": "links_to",
                    })

    # Also connect pages by related field in frontmatter
    for page in pages:
        page_data = manager.read_page(page["slug"])
        if not page_data:
            continue

        related = page_data.get("frontmatter", {}).get("related", [])
        if isinstance(related, str):
            # Parse [a, b, c] format
            related = [r.strip() for r in related.strip("[]").split(",") if r.strip()]

        for rel in related:
            rel_slug = manager.slugify(str(rel))
            if rel_slug in slug_set:
                edge_key = (page["slug"], rel_slug)
                if edge_key not in edge_set:
                    edge_set.add(edge_key)
                    edges.append({
                        "source": page["slug"],
                        "target": rel_slug,
                        "relation": "related_to",
                    })

    # Compute metrics
    in_degree = {}
    out_degree = {}
    for edge in edges:
        out_degree[edge["source"]] = out_degree.get(edge["source"], 0) + 1
        in_degree[edge["target"]] = in_degree.get(edge["target"], 0) + 1

    for node in nodes:
        node["in_degree"] = in_degree.get(node["id"], 0)
        node["out_degree"] = out_degree.get(node["id"], 0)

    # Try community detection
    communities = {}
    try:
        import networkx as nx
        import community as community_louvain

        G = nx.DiGraph()
        for node in nodes:
            G.add_node(node["id"])
        for edge in edges:
            G.add_edge(edge["source"], edge["target"])

        if len(G.nodes) > 0:
            partition = community_louvain.best_partition(G.to_undirected())
            for node_id, comm_id in partition.items():
                communities[node_id] = comm_id
            for node in nodes:
                node["community"] = communities.get(node["id"], 0)
    except ImportError:
        pass
    except Exception:
        pass

    return {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "node_types": list(set(n["type"] for n in nodes)),
        },
    }


def graph(output: str | None, output_format: str) -> None:
    """Generate a link-graph of wiki documents.

    Analyzes wiki links ([[...]]) and related fields to build a
    knowledge graph. Outputs JSON by default, suitable for
    visualization with D3.js, Gephi, or similar tools.
    """
    manager = WikiManager(".")

    pages = manager.list_pages()
    if not pages:
        click.echo("⚠  No wiki pages found. Run `wiki init` first.")
        sys.exit(0)

    click.echo(f"📊 Building graph from {len(pages)} pages...")
    graph_data = _build_graph(manager)

    if output_format == "summary":
        click.echo(f"\n📈 Graph Summary:")
        click.echo(f"   Nodes: {graph_data['metadata']['total_nodes']}")
        click.echo(f"   Edges: {graph_data['metadata']['total_edges']}")
        click.echo(f"   Types: {', '.join(graph_data['metadata']['node_types'])}")

        # Top connected nodes
        nodes_sorted = sorted(graph_data["nodes"], key=lambda n: n["in_degree"] + n["out_degree"], reverse=True)
        if nodes_sorted:
            click.echo(f"\n   Top connected pages:")
            for n in nodes_sorted[:10]:
                total = n["in_degree"] + n["out_degree"]
                if total == 0:
                    break
                click.echo(f"     {n['title'][:40]:<42} in:{n['in_degree']} out:{n['out_degree']}")

        # Orphan nodes
        orphans = [n for n in graph_data["nodes"] if n["in_degree"] == 0 and n["out_degree"] == 0]
        if orphans:
            click.echo(f"\n   Orphan pages (no links): {len(orphans)}")
            for o in orphans[:5]:
                click.echo(f"     • {o['title']}")

    elif output_format == "dot":
        # Graphviz DOT format
        lines = ["digraph wiki {"]
        lines.append('  rankdir=LR;')
        lines.append('  node [shape=box, style=filled, fillcolor=lightyellow];')
        for node in graph_data["nodes"]:
            label = node["title"].replace('"', '\\"')
            lines.append(f'  "{node["id"]}" [label="{label}"];')
        for edge in graph_data["edges"]:
            style = "solid" if edge["relation"] == "links_to" else "dashed"
            lines.append(f'  "{edge["source"]}" -> "{edge["target"]}" [style={style}];')
        lines.append("}")

        dot_text = "\n".join(lines)
        if output:
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            Path(output).write_text(dot_text, encoding="utf-8")
            click.echo(f"✅ DOT graph saved to: {output}")
        else:
            click.echo(dot_text)

    else:
        # JSON format
        json_text = json.dumps(graph_data, indent=2, ensure_ascii=False)
        if output:
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            Path(output).write_text(json_text, encoding="utf-8")
            click.echo(f"✅ Graph saved to: {output}")
            click.echo(f"   {graph_data['metadata']['total_nodes']} nodes, {graph_data['metadata']['total_edges']} edges")
        else:
            click.echo(json_text)
