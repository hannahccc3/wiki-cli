"""Vision-based image description for multimodal ingest.

Uses Ollama's vision model (e.g. llava, minicpm-v) or any OpenAI-compatible
vision endpoint to generate factual descriptions of extracted images.
"""

import base64
import json
from pathlib import Path
from typing import Optional

import requests


class VisionClient:
    """Generate factual descriptions for images using a vision model."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "minicpm-v:latest"):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._is_ollama = "localhost:11434" in base_url or "127.0.0.1:11434" in base_url

    def describe_image(self, image_path: str, context: str = "") -> Optional[str]:
        """Generate a factual description of an image.

        Args:
            image_path: Path to the image file.
            context: Optional surrounding text context for better description.

        Returns:
            Factual description string, or None on failure.
        """
        p = Path(image_path)
        if not p.exists():
            return None

        image_b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif"}.get(
            p.suffix.lstrip("."), "image/png"
        )

        prompt = "Describe this image factually. Focus on visible content: text, diagrams, charts, figures, tables. Be concise (2-3 sentences)."
        if context:
            prompt += f"\n\nContext from the document:\n{context[:500]}"

        if self._is_ollama:
            return self._ollama_describe(prompt, image_b64, mime)
        return self._openai_describe(prompt, image_b64, mime)

    def _ollama_describe(self, prompt: str, image_b64: str, mime: str) -> Optional[str]:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
        }
        try:
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception as e:
            print(f"[Vision] Ollama failed: {e}")
            return None

    def _openai_describe(self, prompt: str, image_b64: str, mime: str) -> Optional[str]:
        url = f"{self.base_url}/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                    ],
                }
            ],
            "max_tokens": 300,
        }
        try:
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[Vision] OpenAI failed: {e}")
            return None


def describe_images(images: list[str], context: str = "", model: str = "minicpm-v:latest") -> dict[str, str]:
    """Describe multiple images. Returns {image_name: description}."""
    client = VisionClient(model=model)
    results = {}
    for img_path in images:
        desc = client.describe_image(img_path, context)
        if desc:
            results[Path(img_path).name] = desc
    return results
