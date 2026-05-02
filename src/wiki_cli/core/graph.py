"""Knowledge graph builder with 4-signal model and Louvain community detection.

Implements a 4-signal knowledge graph model:
  Signal 1: Direct wikilinks ([[page-slug]]), weight 3.0
  Signal 2: Source overlap (pages sharing same raw source), weight 4.0
  Signal 3: Common neighbors via Adamic-Adar index, weight 1.5
  Signal 4: Type affinity matrix, weight 1.0

Uses python-louvain (community.community_louvain) for community detection.
"""

import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx

try:
    import community as community_louvain
except ImportError:
    community_louvain = None  # graceful fallback

from .wiki import WikiManager


# ── Constants ────────────────────────────────────────────────────────────────

# Wikilink regex: [[page-slug]] or [[page-slug|display text]]
WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]")

# Signal weights
W_LINK = 3.0        # Signal 1: direct wikilinks
W_SOURCE = 4.0      # Signal 2: source overlap
W_ADAMIC = 1.5      # Signal 3: Adamic-Adar common neighbors
W_TYPE = 1.0        # Signal 4: type affinity

# Type affinity matrix — asymmetric pairs get the average
TYPE_AFFINITY: Dict[Tuple[str, str], float] = {
    ("entity", "concept"):  1.2,
    ("concept", "entity"):  1.2,
    ("entity", "entity"):   0.8,
    ("concept", "concept"): 0.8,
    ("source", "source"):   0.5,
    ("entity", "source"):   0.6,
    ("source", "entity"):   0.6,
    ("concept", "source"):  0.6,
    ("source", "concept"):  0.6,
}
DEFAULT_AFFINITY = 0.3  # fallback for unmatched type pairs


# ── Helpers ──────────────────────────────────────────────────────────────────

def _extract_wikilinks(content: str) -> List[str]:
    """Return all [[wikilink]] targets from content."""
    return WIKILINK_RE.findall(content)


def _parse_sources(fm: dict) -> Set[str]:
    """Extract source identifiers from frontmatter.

    Handles:
      sources: [a, b, c]
      sources:
        - a
        - b
    """
    raw = fm.get("sources", [])
    if isinstance(raw, str):
        # Could be "[a, b]" or a single value
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            raw = [v.strip().strip('"').strip("'")
                   for v in raw[1:-1].split(",") if v.strip()]
        else:
            raw = [raw] if raw else []
    return set(raw)


def _type_affinity(t1: str, t2: str) -> float:
    """Look up type affinity score."""
    return TYPE_AFFINITY.get((t1, t2), DEFAULT_AFFINITY)


# ── GraphBuilder ─────────────────────────────────────────────────────────────

class GraphBuilder:
    """Build a knowledge graph from wiki pages using a 4-signal model."""

    def __init__(self, wiki_manager: WikiManager):
        self.wiki = wiki_manager
        self._pages: Dict[str, dict] = {}       # slug -> {fm, content, path, type, sources}
        self._graph: Optional[nx.Graph] = None
        self._partition: Optional[Dict[str, int]] = None

    # ── Page loading ─────────────────────────────────────────────────────

    def _load_pages(self) -> None:
        """Scan all wiki directories and parse every .md page."""
        self._pages.clear()
        for ptype, dirname in WikiManager.TYPE_DIRS.items():
            dirpath = self.wiki.project_path / dirname
            if not dirpath.exists():
                continue
            for f in sorted(dirpath.glob("*.md")):
                slug = f.stem
                raw = f.read_text(encoding="utf-8")
                fm, content = WikiManager._parse_frontmatter(raw)
                self._pages[slug] = {
                    "fm": fm,
                    "content": content,
                    "path": str(f),
                    "type": fm.get("type", ptype),
                    "sources": _parse_sources(fm),
                }
        # Also scan wiki/ root for overview etc.
        wiki_root = self.wiki.project_path / "wiki"
        if wiki_root.exists():
            for f in sorted(wiki_root.glob("*.md")):
                slug = f.stem
                if slug in self._pages:
                    continue
                raw = f.read_text(encoding="utf-8")
                fm, content = WikiManager._parse_frontmatter(raw)
                self._pages[slug] = {
                    "fm": fm,
                    "content": content,
                    "path": str(f),
                    "type": fm.get("type", "overview"),
                    "sources": _parse_sources(fm),
                }

    # ── Signal computation ───────────────────────────────────────────────

    def _signal1_links(self, G: nx.Graph) -> None:
        """Signal 1: direct [[wikilinks]] with weight W_LINK."""
        for slug, page in self._pages.items():
            targets = _extract_wikilinks(page["content"])
            for target in targets:
                target_slug = WikiManager.slugify(target)
                if target_slug in self._pages and target_slug != slug:
                    if G.has_edge(slug, target_slug):
                        G[slug][target_slug]["weight"] += W_LINK
                        G[slug][target_slug]["signals"].add("link")
                    else:
                        G.add_edge(slug, target_slug,
                                   weight=W_LINK, signals={"link"})

    def _signal2_source_overlap(self, G: nx.Graph) -> None:
        """Signal 2: pages sharing the same raw source get weight W_SOURCE."""
        # Group pages by source
        source_pages: Dict[str, List[str]] = defaultdict(list)
        for slug, page in self._pages.items():
            for src in page["sources"]:
                source_pages[src].append(slug)

        for src, slugs in source_pages.items():
            for i, a in enumerate(slugs):
                for b in slugs[i + 1:]:
                    if a == b:
                        continue
                    if G.has_edge(a, b):
                        G[a][b]["weight"] += W_SOURCE
                        G[a][b]["signals"].add("source")
                    else:
                        G.add_edge(a, b,
                                   weight=W_SOURCE, signals={"source"})

    def _signal3_adamic_adar(self, G: nx.Graph) -> None:
        """Signal 3: common-neighbors boost via Adamic-Adar index, weight W_ADAMIC."""
        # Use existing graph edges (from signals 1 & 2) as the basis
        existing = list(G.nodes())
        if len(existing) < 2:
            return

        # For every pair of non-adjacent nodes that share a neighbor,
        # add a weighted edge proportional to the Adamic-Adar index.
        nodes = set(existing)
        processed: Set[Tuple[str, str]] = set()

        for node in existing:
            neighbors = set(G.neighbors(node))
            for n1 in neighbors:
                for n2 in neighbors:
                    if n1 >= n2:
                        continue
                    pair = (n1, n2)
                    if pair in processed:
                        continue
                    if G.has_edge(n1, n2):
                        # Already connected — still boost with Adamic-Adar
                        # contribution from this shared neighbor
                        deg = G.degree(node)
                        if deg > 1:
                            aa = 1.0 / math.log(deg)
                            G[n1][n2]["weight"] += W_ADAMIC * aa
                            G[n1][n2]["signals"].add("adamic")
                        processed.add(pair)
                    else:
                        # Check all common neighbors
                        common = set(G.neighbors(n1)) & set(G.neighbors(n2))
                        aa_sum = 0.0
                        for cn in common:
                            deg = G.degree(cn)
                            if deg > 1:
                                aa_sum += 1.0 / math.log(deg)
                        if aa_sum > 0:
                            G.add_edge(n1, n2,
                                       weight=W_ADAMIC * aa_sum,
                                       signals={"adamic"})
                        processed.add(pair)

    def _signal4_type_affinity(self, G: nx.Graph) -> None:
        """Signal 4: add edges between nodes whose types are semantically related."""
        slugs = list(self._pages.keys())
        for i, a in enumerate(slugs):
            for b in slugs[i + 1:]:
                t1 = self._pages[a]["type"]
                t2 = self._pages[b]["type"]
                aff = _type_affinity(t1, t2)
                if aff <= 0:
                    continue
                if G.has_edge(a, b):
                    G[a][b]["weight"] += W_TYPE * aff
                    G[a][b]["signals"].add("type")
                else:
                    G.add_edge(a, b,
                               weight=W_TYPE * aff, signals={"type"})

    # ── Community detection ──────────────────────────────────────────────

    def _detect_communities(self, G: nx.Graph) -> Dict[str, int]:
        """Run Louvain community detection. Returns slug -> community_id map."""
        if community_louvain is not None:
            partition = community_louvain.best_partition(G, weight="weight",
                                                         random_state=42)
        else:
            # Fallback: greedy modularity via networkx
            from networkx.algorithms.community import greedy_modularity_communities
            communities = greedy_modularity_communities(G, weight="weight")
            partition = {}
            for idx, comm in enumerate(communities):
                for node in comm:
                    partition[node] = idx
        return partition

    # ── Public API ───────────────────────────────────────────────────────

    def build(self) -> Dict[str, Any]:
        """Build the full knowledge graph and return structured result.

        Returns:
            {
              "nodes": [{id, label, type, path, linkCount, community}, ...],
              "edges": [{source, target, weight, signals}, ...],
              "communities": [{id, nodeCount, cohesion, topNodes}, ...]
            }
        """
        self._load_pages()

        if not self._pages:
            return {"nodes": [], "edges": [], "communities": []}

        # Ensure all pages are nodes
        G = nx.Graph()
        for slug, page in self._pages.items():
            G.add_node(slug,
                       label=page["fm"].get("title", slug),
                       type=page["type"],
                       path=page["path"])

        # Apply 4 signals
        self._signal1_links(G)
        self._signal2_source_overlap(G)
        self._signal3_adamic_adar(G)
        self._signal4_type_affinity(G)

        # Remove zero/negative weight edges
        to_remove = [(u, v) for u, v, d in G.edges(data=True) if d.get("weight", 0) <= 0]
        G.remove_edges_from(to_remove)

        # Community detection
        partition = self._detect_communities(G)
        self._partition = partition

        # Build node list
        nodes = []
        for slug in G.nodes():
            page = self._pages.get(slug, {})
            fm = page.get("fm", {})
            link_count = len(_extract_wikilinks(page.get("content", "")))
            nodes.append({
                "id": slug,
                "label": fm.get("title", slug),
                "type": page.get("type", "unknown"),
                "path": page.get("path", ""),
                "linkCount": link_count,
                "community": partition.get(slug, 0),
            })

        # Build edge list
        edges = []
        for u, v, d in G.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "weight": round(d.get("weight", 0), 4),
                "signals": sorted(d.get("signals", set())),
            })

        # Build community summaries
        communities = self._summarize_communities(G, partition)

        self._graph = G
        return {
            "nodes": nodes,
            "edges": edges,
            "communities": communities,
        }

    def _summarize_communities(self, G: nx.Graph,
                                partition: Dict[str, int]) -> List[Dict[str, Any]]:
        """Produce per-community stats."""
        comm_data: Dict[int, List[str]] = defaultdict(list)
        for slug, cid in partition.items():
            comm_data[cid].append(slug)

        communities = []
        for cid, members in sorted(comm_data.items()):
            # Cohesion: fraction of possible internal edges that exist
            n = len(members)
            if n < 2:
                cohesion = 1.0
            else:
                member_set = set(members)
                internal = sum(
                    1 for u, v in G.edges(members)
                    if u in member_set and v in member_set
                )
                max_edges = n * (n - 1) / 2
                cohesion = round(internal / max_edges, 4) if max_edges > 0 else 0.0

            # Top nodes by degree within community
            deg = [(slug, G.degree(slug, weight="weight")) for slug in members]
            deg.sort(key=lambda x: x[1], reverse=True)
            top_nodes = [s for s, _ in deg[:5]]

            communities.append({
                "id": cid,
                "nodeCount": n,
                "cohesion": cohesion,
                "topNodes": top_nodes,
            })

        return communities

    # ── Save ─────────────────────────────────────────────────────────────

    def save(self, output_path: str, format: str = "json") -> str:
        """Build (if needed) and save the graph to *output_path*.

        Args:
            output_path: destination file path
            format: 'json' (default) — structured JSON; 'gexf' / 'graphml' via networkx

        Returns:
            The resolved output path.
        """
        if self._graph is None:
            self.build()

        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            data = self.build()  # idempotent
            dest.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        elif format == "gexf":
            nx.write_gexf(self._graph, str(dest))
        elif format == "graphml":
            nx.write_graphml(self._graph, str(dest))
        else:
            raise ValueError(f"Unsupported format: {format}")

        return str(dest.resolve())

    # ── Insights ─────────────────────────────────────────────────────────

    def get_insights(self) -> Dict[str, Any]:
        """Analyze the graph and return actionable insights.

        Returns:
            {
              "surprising_connections": [...],
              "knowledge_gaps": [...],
              "hub_nodes": [...]
            }
        """
        if self._graph is None:
            self.build()
        G = self._graph
        partition = self._partition or {}

        # ── Hub nodes (top by weighted degree) ───────────────────────────
        hub_nodes = []
        for slug in G.nodes():
            wdeg = G.degree(slug, weight="weight")
            hub_nodes.append({
                "id": slug,
                "label": self._pages.get(slug, {}).get("fm", {}).get("title", slug),
                "weightedDegree": round(wdeg, 2),
                "neighborCount": len(list(G.neighbors(slug))),
                "community": partition.get(slug, 0),
            })
        hub_nodes.sort(key=lambda x: x["weightedDegree"], reverse=True)

        # ── Surprising connections ───────────────────────────────────────
        # Edges whose weight comes entirely/mostly from non-obvious signals
        surprising = []
        for u, v, d in G.edges(data=True):
            signals = d.get("signals", set())
            # Surprising if no direct link signal but still connected
            if "link" not in signals and d.get("weight", 0) > 0:
                surprising.append({
                    "source": u,
                    "target": v,
                    "weight": round(d["weight"], 4),
                    "signals": sorted(signals),
                    "reason": self._explain_connection(u, v, signals),
                })
        surprising.sort(key=lambda x: x["weight"], reverse=True)

        # ── Knowledge gaps ───────────────────────────────────────────────
        # Nodes with low degree, or type-pairs with few connections
        gaps: List[Dict[str, Any]] = []
        for slug in G.nodes():
            degree = len(list(G.neighbors(slug)))
            link_count = len(_extract_wikilinks(self._pages.get(slug, {}).get("content", "")))
            if degree <= 1 and link_count == 0:
                gaps.append({
                    "id": slug,
                    "type": self._pages.get(slug, {}).get("type", "unknown"),
                    "reason": "Isolated — no outgoing links and no graph neighbors",
                })

        # Check for types with no cross-connections
        all_types = {p["type"] for p in self._pages.values()}
        connected_types: Set[str] = set()
        for u, v in G.edges():
            tu = self._pages.get(u, {}).get("type", "")
            tv = self._pages.get(v, {}).get("type", "")
            connected_types.add(tu)
            connected_types.add(tv)
        for t in all_types - connected_types:
            gaps.append({
                "id": f"type:{t}",
                "type": t,
                "reason": f"No '{t}' pages are connected to any other page",
            })

        return {
            "surprising_connections": surprising[:20],
            "knowledge_gaps": gaps,
            "hub_nodes": hub_nodes[:15],
            "deep_research_suggestions": self._suggest_deep_research(gaps, surprising),
        }

    def _suggest_deep_research(self, gaps: list, surprising: list) -> list:
        """Generate deep research suggestions based on gaps and surprising connections."""
        suggestions = []

        for gap in gaps[:5]:
            if gap.get("id", "").startswith("type:"):
                t = gap.get("type", "")
                suggestions.append({
                    "topic": f"Research connections for '{t}' type pages",
                    "reason": f"Type '{t}' has no cross-connections — deep research could find relationships",
                    "priority": "medium",
                })
            else:
                slug = gap.get("id", "")
                title = self._pages.get(slug, {}).get("fm", {}).get("title", slug)
                suggestions.append({
                    "topic": f"Find related knowledge for '{title}'",
                    "reason": f"Page '{slug}' is isolated — deep research could find connections",
                    "priority": "low",
                })

        for conn in surprising[:3]:
            u_title = self._pages.get(conn["source"], {}).get("fm", {}).get("title", conn["source"])
            v_title = self._pages.get(conn["target"], {}).get("fm", {}).get("title", conn["target"])
            suggestions.append({
                "topic": f"Verify connection: {u_title} ↔ {v_title}",
                "reason": f"Surprising non-obvious connection ({conn['reason']})",
                "priority": "high",
            })

        return suggestions[:10]

    def _explain_connection(self, u: str, v: str, signals: set) -> str:
        """Human-readable explanation of why two pages are connected."""
        parts = []
        if "source" in signals:
            u_src = self._pages.get(u, {}).get("sources", set())
            v_src = self._pages.get(v, {}).get("sources", set())
            shared = u_src & v_src
            if shared:
                parts.append(f"shared sources: {', '.join(sorted(shared))}")
        if "adamic" in signals:
            parts.append("share common neighbors (Adamic-Adar)")
        if "type" in signals:
            tu = self._pages.get(u, {}).get("type", "?")
            tv = self._pages.get(v, {}).get("type", "?")
            parts.append(f"type affinity ({tu} ↔ {tv})")
        return "; ".join(parts) if parts else "multi-signal connection"
