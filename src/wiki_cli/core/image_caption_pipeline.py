"""
Caption-the-images pipeline + persistent cache.

Discovers every `![](path)` reference in markdown, generates factual
captions using a vision model (with SHA-256 dedup across the whole project),
and rewrites markdown so each `![](path)` becomes `![<caption>](path)`.

Cache key = SHA-256 of image bytes. This makes duplicate images across PDFs
(logos, page headers, recurring chart templates) a single LLM call across
the whole project.

Cache file: `<project>/.llm-wiki/image-caption-cache.json`
Keyed: `{ "<sha256>": { caption, mimeType, model, capturedAt } }`

Reference: nashsu/llm_wiki/src/lib/image-caption-pipeline.ts
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .vision import VisionClient


# ── Cache ────────────────────────────────────────────────────────────────

CACHE_REL_PATH = ".llm-wiki/image-caption-cache.json"

# Window size for context-aware captioning (chars before/after image).
CONTEXT_CHARS = 150


@dataclass
class CaptionEntry:
    caption: str
    mime_type: str
    model: str
    captured_at: str


def load_caption_cache(project_path: str) -> dict[str, str]:
    """Load the caption cache. Returns SHA-256 → caption dict."""
    cache_path = Path(project_path) / CACHE_REL_PATH
    if not cache_path.exists():
        return {}
    try:
        raw = cache_path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return {}
        return {k: v["caption"] for k, v in data.items() if isinstance(v, dict)}
    except (json.JSONDecodeError, OSError):
        return {}


def _load_full_cache(project_path: str) -> dict[str, CaptionEntry]:
    """Load the full caption cache with metadata."""
    cache_path = Path(project_path) / CACHE_REL_PATH
    if not cache_path.exists():
        return {}
    try:
        raw = cache_path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return {}
        out = {}
        for k, v in data.items():
            if isinstance(v, dict) and "caption" in v:
                out[k] = CaptionEntry(
                    caption=v["caption"],
                    mime_type=v.get("mimeType", "image/png"),
                    model=v.get("model", ""),
                    captured_at=v.get("capturedAt", ""),
                )
        return out
    except (json.JSONDecodeError, OSError):
        return {}


def _write_cache(project_path: str, cache: dict[str, CaptionEntry]) -> None:
    """Persist the caption cache to disk atomically."""
    cache_path = Path(project_path) / CACHE_REL_PATH
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        k: {
            "caption": v.caption,
            "mimeType": v.mime_type,
            "model": v.model,
            "capturedAt": v.captured_at,
        }
        for k, v in cache.items()
    }
    cache_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ── SHA-256 ─────────────────────────────────────────────────────────────

def sha256_of_bytes(data: bytes) -> str:
    """Compute SHA-256 hex digest of raw bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_of_base64(b64: str) -> str:
    """Compute SHA-256 of a base64 string by decoding to bytes first.

    The cache key is the hash of the IMAGE BYTES, not the base64 string —
    the same image encoded with different base64 line-wrap settings would
    otherwise miss the cache.
    """
    # Handle both standard base64 and data URI formats
    if b64.startswith("data:"):
        b64 = b64.split(",", 1)[1] if "," in b64 else b64[5:]
    binary = base64.b64decode(b64 + "==")
    return sha256_of_bytes(binary)


# ── Image reference discovery ───────────────────────────────────────────

# Matches standard markdown image syntax: `![alt](url)`
MD_IMAGE_RE = re.compile(r"(!\[)([^\]]*)(\]\()([^)\s]+)(\))")


@dataclass
class ImageRef:
    full: str    # entire `![alt](url)` substring
    alt: str
    url: str
    index: int   # 0-based offset in source markdown
    length: int  # length of entire match


def find_image_references(markdown: str) -> list[ImageRef]:
    """Find every `![alt](url)` reference in markdown."""
    refs: list[ImageRef] = []
    for m in MD_IMAGE_RE.finditer(markdown):
        refs.append(ImageRef(
            full=m.group(0),
            alt=m.group(2),
            url=m.group(4),
            index=m.start(),
            length=len(m.group(0)),
        ))
    return refs


def slice_context(markdown: str, ref: ImageRef, window_chars: int = CONTEXT_CHARS) -> tuple[str, str]:
    """Slice chars before and after an image match in source markdown.

    Returns (before, after) — each clamped to document edges.
    """
    before_start = max(0, ref.index - window_chars)
    before = markdown[before_start:ref.index]
    after_start = ref.index + ref.length
    after = markdown[after_start:after_start + window_chars]
    return before, after


# ── Caption pipeline ─────────────────────────────────────────────────────

@dataclass
class CaptionPipelineResult:
    enriched_markdown: str
    fresh_captions: int
    cached_captions: int
    failed: int


def caption_markdown_images(
    project_path: str,
    markdown: str,
    vision_client: Optional[VisionClient] = None,
    concurrency: int = 1,
    should_caption: Optional[callable] = None,
    on_progress: Optional[callable] = None,
) -> CaptionPipelineResult:
    """Caption every distinct image referenced in markdown.

    - Distinct = same SHA-256. Duplicate image content captions once.
    - Failures during a single caption call do NOT abort the batch.
    - Returns rewritten markdown with captions embedded as alt text.

    Args:
        project_path: Wiki project root (for cache file location).
        markdown: Source markdown with `![](path)` references.
        vision_client: Vision model client. Defaults to VisionClient().
        concurrency: Max parallel caption requests. Default 1 (sequential).
        should_caption: Optional URL filter predicate.
        on_progress: Optional callback(done, total) fired after each image.
    """
    refs = find_image_references(markdown)
    if not refs:
        return CaptionPipelineResult(markdown, 0, 0, 0)

    # Apply optional URL filter.
    if should_caption:
        target_refs = [r for r in refs if should_caption(r.url)]
    else:
        target_refs = refs

    if not target_refs:
        return CaptionPipelineResult(markdown, 0, 0, 0)

    # De-dupe by URL, keeping first occurrence (richer context).
    seen_urls: set[str] = set()
    unique_refs: list[ImageRef] = []
    for r in target_refs:
        if r.url in seen_urls:
            continue
        seen_urls.add(r.url)
        unique_refs.append(r)

    cache = _load_full_cache(project_path)
    fresh_captions = 0
    cached_captions = 0
    failed = 0
    caption_by_url: dict[str, str] = {}
    client = vision_client or VisionClient()
    total = len(unique_refs)

    for i, ref in enumerate(unique_refs):
        # Resolve path.
        if ref.url.startswith("/"):
            abs_path = ref.url
        else:
            abs_path = str(Path(project_path) / "wiki" / ref.url)

        img_bytes: Optional[bytes] = None
        mime = "image/png"
        try:
            p = Path(abs_path)
            if p.exists():
                img_bytes = p.read_bytes()
                mime = _mime_from_path(p)
        except OSError:
            pass

        if img_bytes is None:
            failed += 1
            continue

        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
        file_hash = sha256_of_bytes(img_bytes)

        # Cache hit.
        if file_hash in cache:
            caption_by_url[ref.url] = cache[file_hash].caption
            cached_captions += 1
            on_progress and on_progress(i + 1, total)
            continue

        # Cache miss — call vision model.
        before, after = slice_context(markdown, ref)
        ctx = f"Before: {before}\nAfter: {after}" if (before or after) else ""

        try:
            caption = client.describe_image(abs_path, context=ctx) or ""
        except Exception:
            caption = ""

        if caption:
            cache[file_hash] = CaptionEntry(
                caption=caption,
                mime_type=mime,
                model=getattr(client, "model", "unknown"),
                captured_at=_iso_now(),
            )
            caption_by_url[ref.url] = caption
            fresh_captions += 1
        else:
            failed += 1

        on_progress and on_progress(i + 1, total)

    # Persist cache on exit if any fresh captions were added.
    if fresh_captions > 0:
        try:
            _write_cache(project_path, cache)
        except OSError as e:
            print(f"[caption-pipeline] failed to persist cache: {e}")

    # Rewrite markdown: replace every image ref's alt text with caption.
    def replace_ref(m: re.Match) -> str:
        url = m.group(4)
        caption = caption_by_url.get(url, "")
        if not caption:
            return m.group(0)
        # Sanitize caption: no newlines, no ']' characters.
        safe = (
            caption.replace("\r\n", " ")
                   .replace("\n", " ")
                   .replace("]", ")")
                   .strip()
        )
        return f"![{safe}]({url})"

    enriched = MD_IMAGE_RE.sub(replace_ref, markdown)
    return CaptionPipelineResult(enriched, fresh_captions, cached_captions, failed)


# ── Utilities ──────────────────────────────────────────────────────────

_MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".svg": "image/svg+xml",
}


def _mime_from_path(p: Path) -> str:
    return _MIME_MAP.get(p.suffix.lower(), "image/png")


def _iso_now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
