"""Deep Research — LLM-driven multi-query web research.

Flow:
  1. LLM generates search topics based on wiki gaps / user question
  2. Web search for each topic (using requests + search API or scraping)
  3. LLM summarizes findings
  4. Results auto-ingested into wiki as source/synthesis pages
"""

import json
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


class DeepResearch:
    """LLM-driven deep research with web search integration."""

    def __init__(self, llm_client, wiki_manager, search_api_key: str = ""):
        self.llm = llm_client
        self.wiki = wiki_manager
        self.search_api_key = search_api_key

    def generate_research_topics(self, question: str, max_topics: int = 5) -> List[str]:
        """LLM generates focused search queries for the given question."""
        prompt = f"""Given this research question, generate {max_topics} specific web search queries that would help answer it comprehensively.

Question: {question}

Return a JSON array of search query strings. Example: ["query 1", "query 2"]
Only return the JSON array, nothing else."""

        try:
            response = self.llm.generate(prompt, system="You are a research assistant. Generate targeted search queries.", max_tokens=500)
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if match:
                return json.loads(match.group())[:max_topics]
            return [question]
        except Exception:
            return [question]

    def web_search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Search the web using DuckDuckGo (no API key needed) or a configured API."""
        if self.search_api_key:
            return self._search_via_api(query, max_results)
        return self._search_ddg(query, max_results)

    def _search_ddg(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """DuckDuckGo HTML search (no API key needed)."""
        results = []
        try:
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
            resp = requests.get(
                "https://html.duckduckgo.com/html/",
                params={"q": query},
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()

            for match in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', resp.text, re.DOTALL):
                url = match.group(1)
                title = re.sub(r'<[^>]+>', '', match.group(2)).strip()
                if url and title and "duckduckgo" not in url.lower():
                    results.append({"title": title, "url": url})
                    if len(results) >= max_results:
                        break
        except Exception as e:
            print(f"[DeepResearch] DDG search failed: {e}")

        return results

    def _search_via_api(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """Search using a configured API (placeholder for SearXNG, Brave, etc.)."""
        return []

    def fetch_content(self, url: str) -> str:
        """Fetch and extract text content from a URL."""
        try:
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            text = resp.text

            # Strip HTML tags (basic)
            text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:5000]
        except Exception:
            return ""

    def synthesize_findings(self, question: str, search_results: List[Dict[str, Any]]) -> str:
        """LLM synthesizes search results into a coherent answer."""
        context_parts = []
        for r in search_results:
            context_parts.append(f"### {r.get('title', 'Untitled')}\nSource: {r.get('url', '')}\n{r.get('content', '')[:2000]}")

        context = "\n\n---\n\n".join(context_parts)

        prompt = f"""Synthesize the following research findings into a comprehensive answer.

Research Question: {question}

Findings:
{context}

Provide:
1. A comprehensive answer to the question
2. Key insights and findings
3. Sources consulted
4. Areas that need further research"""

        try:
            return self.llm.generate(prompt, system="You are a research synthesizer. Be thorough and cite sources.", max_tokens=4000)
        except Exception as e:
            return f"Synthesis failed: {e}"

    def research(self, question: str, max_topics: int = 3, auto_ingest: bool = True) -> Dict[str, Any]:
        """Run a complete deep research cycle.

        Returns: {
            "question": str,
            "topics": [str],
            "search_results": [{title, url, content}],
            "synthesis": str,
            "ingested": bool
        }
        """
        topics = self.generate_research_topics(question, max_topics)

        all_results = []
        for topic in topics:
            hits = self.web_search(topic, max_results=3)
            for hit in hits:
                content = self.fetch_content(hit["url"])
                if content:
                    hit["content"] = content
                    hit["search_query"] = topic
                    all_results.append(hit)

        synthesis = self.synthesize_findings(question, all_results)

        ingested = False
        if auto_ingest and synthesis:
            ingested = self._ingest_research(question, synthesis, all_results)

        return {
            "question": question,
            "topics": topics,
            "search_results": [{"title": r.get("title", ""), "url": r.get("url", "")} for r in all_results],
            "synthesis": synthesis,
            "ingested": ingested,
        }

    def _ingest_research(self, question: str, synthesis: str, results: List[dict]) -> bool:
        """Write research results as a wiki synthesis page."""
        try:
            slug = re.sub(r'[^a-z0-9]+', '-', question.lower())[:50].strip('-')
            if not slug:
                slug = f"research-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            sources = [r.get("url", "") for r in results if r.get("url")]
            content = f"# Deep Research: {question}\n\n{synthesis}\n\n## Sources\n"
            for r in results:
                content += f"- [{r.get('title', 'Link')}]({r.get('url', '')})\n"

            self.wiki.write_page(
                slug=slug,
                page_type="synthesis",
                title=f"Research: {question[:80]}",
                content=content,
                tags=["deep-research", "auto-generated"],
                related=[],
                sources=sources,
            )
            return True
        except Exception as e:
            print(f"[DeepResearch] Ingest failed: {e}")
            return False
