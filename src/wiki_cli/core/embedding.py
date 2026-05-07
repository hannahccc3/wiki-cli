"""Embedding pipeline — vector semantic search over wiki pages.

Architecture:
  - Chunks wiki pages by markdown headings
  - Embeds chunks via Ollama (or any OpenAI-compatible /v1/embeddings endpoint)
  - Stores vectors in LanceDB (embedded, no external DB needed)
  - Search: embed query → vector search → rerank by blended score

Config (wiki-cli.yaml):
  embeddings:
    enabled: true
    base_url: "http://localhost:11434/v1"
    api_key: ""
    model: "nomic-embed-text"
    dimensions: 768
    max_chunk_chars: 1000
    overlap_chars: 200
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


def _default_embeddings_config() -> dict:
    return {
        "enabled": False,
        "base_url": "http://localhost:11434/v1",
        "api_key": "",
        "model": "qwen3-embedding:8b",
        "dimensions": 4096,
        "max_chunk_chars": 1000,
        "overlap_chars": 200,
    }


# ── Text Chunking ──────────────────────────────────────────────────────

class Chunk:
    __slots__ = ("index", "text", "heading_path")

    def __init__(self, index: int, text: str, heading_path: str):
        self.index = index
        self.text = text
        self.heading_path = heading_path


def chunk_markdown(content: str, target_chars: int = 1000, overlap_chars: int = 200) -> List[Chunk]:
    """Split markdown content into chunks by heading boundaries."""
    lines = content.split("\n")
    sections: List[tuple[str, str]] = []
    current_heading = ""
    current_text: List[str] = []

    for line in lines:
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            if current_text:
                sections.append((current_heading, "\n".join(current_text)))
            current_heading = heading_match.group(2).strip()
            current_text = []
        else:
            current_text.append(line)

    if current_text:
        sections.append((current_heading, "\n".join(current_text)))

    chunks: List[Chunk] = []
    buffer = ""
    buffer_heading = ""
    idx = 0

    for heading, text in sections:
        combined = f"{heading}\n{text}" if heading else text
        if len(buffer) + len(combined) > target_chars and buffer:
            chunks.append(Chunk(idx, buffer.strip(), buffer_heading))
            idx += 1
            overlap = buffer[-overlap_chars:] if overlap_chars > 0 else ""
            buffer = overlap + "\n" + combined
            buffer_heading = heading
        else:
            buffer = buffer + "\n" + combined if buffer else combined
            if not buffer_heading:
                buffer_heading = heading

    if buffer.strip():
        chunks.append(Chunk(idx, buffer.strip(), buffer_heading))

    return chunks


# ── Embedding Client ───────────────────────────────────────────────────

class EmbeddingClient:
    """Fetch embeddings from Ollama or any OpenAI-compatible endpoint."""

    def __init__(self, config: dict | None = None):
        cfg = {**_default_embeddings_config(), **(config or {})}
        self.base_url = cfg["base_url"].rstrip("/")
        self.model = cfg["model"]
        self.api_key = cfg.get("api_key", "")
        self.dimensions = cfg.get("dimensions", 768)
        self._is_ollama = (
            "localhost:11434" in self.base_url
            or "127.0.0.1:11434" in self.base_url
            or self.base_url.endswith(":11434")
            or self.base_url.endswith(":11434/")
        )

    def embed(self, text: str) -> List[float] | None:
        """Get embedding vector for a single text."""
        if self._is_ollama:
            return self._embed_ollama(text)
        return self._embed_openai([text])[0] if text else None

    def _embed_ollama(self, text: str) -> List[float] | None:
        """Ollama native API: POST /api/embeddings with {model, prompt}."""
        url = f"{self.base_url.replace('/v1', '')}/api/embeddings"
        payload = {"model": self.model, "prompt": text}
        try:
            resp = requests.post(url, json=payload, timeout=60)
            resp.raise_for_status()
            return resp.json().get("embedding")
        except Exception as e:
            print(f"[Embedding] Ollama failed: {e}")
            return None

    def _embed_openai(self, texts: List[str]) -> List[List[float] | None]:
        """OpenAI-compatible API: POST /v1/embeddings with {model, input}."""
        url = f"{self.base_url}/embeddings"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {"model": self.model, "input": texts}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            results: List[List[float] | None] = [None] * len(texts)
            for item in data.get("data", []):
                idx = item.get("index", 0)
                results[idx] = item.get("embedding")
            return results
        except Exception as e:
            print(f"[Embedding] OpenAI batch failed: {e}")
            return [None] * len(texts)

    def embed_batch(self, texts: List[str]) -> List[List[float] | None]:
        """Get embedding vectors for multiple texts."""
        if self._is_ollama:
            results = []
            for t in texts:
                results.append(self._embed_ollama(t))
            return results
        return self._embed_openai(texts)


# ── LanceDB Vector Store ───────────────────────────────────────────────

class VectorStore:
    """LanceDB-backed vector store for wiki page chunks."""

    TABLE_NAME = "wiki_chunks"

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.db_path = self.project_path / ".llm-wiki" / "vectordb"
        self._db = None
        self._table = None

    def _get_db(self):
        if self._db is None:
            import lancedb
            self._db = lancedb.connect(str(self.db_path))
        return self._db

    def _get_table(self):
        if self._table is None:
            db = self._get_db()
            try:
                self._table = db.open_table(self.TABLE_NAME)
            except Exception:
                self._table = None
        return self._table

    def upsert_chunks(self, page_id: str, chunks: List[dict]) -> None:
        """Insert or replace chunks for a page.

        Each chunk dict: {chunk_index, chunk_text, heading_path, embedding}
        """
        db = self._get_db()
        records = []
        for c in chunks:
            records.append({
                "page_id": page_id,
                "chunk_index": c["chunk_index"],
                "chunk_text": c["chunk_text"],
                "heading_path": c.get("heading_path", ""),
                "embedding": c["embedding"],
            })

        try:
            table = db.open_table(self.TABLE_NAME)
            table.delete(f'page_id = "{page_id}"')
            table.add(records)
        except Exception:
            if records:
                db.create_table(self.TABLE_NAME, records)
        self._table = None

    def search(self, query_embedding: List[float], top_k: int = 30) -> List[dict]:
        """Search for similar chunks. Returns list of {page_id, chunk_text, heading_path, score}."""
        table = self._get_table()
        if table is None:
            return []
        try:
            results = table.search(query_embedding).limit(top_k).to_list()
            out = []
            for r in results:
                out.append({
                    "page_id": r.get("page_id", ""),
                    "chunk_text": r.get("chunk_text", ""),
                    "heading_path": r.get("heading_path", ""),
                    "score": float(r.get("_distance", 1.0)),
                })
            return out
        except Exception as e:
            print(f"[VectorStore] Search failed: {e}")
            return []

    def delete_page(self, page_id: str) -> None:
        """Remove all chunks for a page."""
        table = self._get_table()
        if table is None:
            return
        try:
            table.delete(f'page_id = "{page_id}"')
        except Exception:
            pass

    def count(self) -> int:
        """Total number of chunks."""
        table = self._get_table()
        if table is None:
            return 0
        try:
            return len(table)
        except Exception:
            return 0


# ── Public API ─────────────────────────────────────────────────────────

def embed_page(
    project_path: str,
    page_id: str,
    title: str,
    content: str,
    embed_client: EmbeddingClient,
    store: VectorStore,
    max_chunk_chars: int = 1000,
    overlap_chars: int = 200,
) -> int:
    """Embed a wiki page: chunk → embed → upsert. Returns number of chunks indexed."""
    chunks = chunk_markdown(content, target_chars=max_chunk_chars, overlap_chars=overlap_chars)
    if not chunks:
        return 0

    rows = []
    texts = [f"{title}\n{c.heading_path}\n{c.text}" for c in chunks]
    vectors = embed_client.embed_batch(texts)

    indexed = 0
    for i, chunk in enumerate(chunks):
        vec = vectors[i] if i < len(vectors) else None
        if vec:
            rows.append({
                "chunk_index": chunk.index,
                "chunk_text": chunk.text,
                "heading_path": chunk.heading_path,
                "embedding": vec,
            })
            indexed += 1

    if rows:
        store.upsert_chunks(page_id, rows)
    return indexed


def embed_all_pages(
    project_path: str,
    embed_client: EmbeddingClient,
    store: VectorStore,
    max_chunk_chars: int = 1000,
    overlap_chars: int = 200,
) -> int:
    """Embed all wiki pages. Returns total pages processed."""
    from wiki_cli.core.wiki import WikiManager
    manager = WikiManager(project_path)
    pages = manager.list_pages()
    skip = {"index", "log", "overview", "purpose", "schema"}
    count = 0
    for page in pages:
        slug = page.get("slug", "")
        if slug in skip:
            continue
        page_data = manager.read_page(slug)
        if not page_data:
            continue
        title = page_data.get("frontmatter", {}).get("title", slug)
        content = page_data.get("content", "")
        embed_page(project_path, slug, title, content, embed_client, store, max_chunk_chars, overlap_chars)
        count += 1
    return count


def search_by_embedding(
    query: str,
    embed_client: EmbeddingClient,
    store: VectorStore,
    top_k: int = 10,
) -> List[Dict[str, Any]]:
    """Vector search: embed query → search → group by page → rank. Returns [{slug, score, matched_chunks}]."""
    query_vec = embed_client.embed(query)
    if not query_vec:
        return []

    raw = store.search(query_vec, top_k=top_k * 3)
    if not raw:
        return []

    by_page: Dict[str, List[dict]] = {}
    for r in raw:
        pid = r["page_id"]
        by_page.setdefault(pid, []).append(r)

    ranked = []
    for page_id, chunks in by_page.items():
        chunks.sort(key=lambda x: x["score"])
        top_score = chunks[0]["score"]
        tail_score = sum(c["score"] for c in chunks[1:]) * 0.3
        blended = top_score + min(tail_score, max(0, 1 - top_score))
        ranked.append({
            "slug": page_id,
            "score": blended,
            "matched_chunks": [
                {"text": c["chunk_text"][:200], "heading_path": c["heading_path"], "score": c["score"]}
                for c in chunks[:3]
            ],
        })

    ranked.sort(key=lambda x: x["score"])
    return ranked[:top_k]
