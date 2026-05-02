"""Multi-provider LLM client.

Supported providers:
  - openai     : OpenAI Chat Completions API (also: GPT-4o, o3, o1)
  - anthropic  : Anthropic Messages API (Claude)
  - google     : Google Generative Language API (Gemini)
  - deepseek   : DeepSeek API (deepseek-chat, deepseek-reasoner)
  - groq       : Groq Cloud (llama, mixtral, etc.)
  - xai        : xAI (Grok)
  - kimi       : Kimi / Moonshot
  - zhipu      : 智谱 GLM (Zhipu BigModel)
  - minimax    : MiniMax (Anthropic-compatible wire)
  - bailian    : 阿里百炼 Coding Plan
  - volcengine : 火山引擎 Ark
  - xiaomi     : 小米 MiMo
  - ollama     : Ollama / llama.cpp / LM Studio / vLLM (local)
  - custom     : Any OpenAI- or Anthropic-compatible endpoint
"""

import os
import json
import requests


PROVIDER_PRESETS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "wire": "openai",
        "default_model": "gpt-4o",
        "suggested_models": ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "o3", "o3-mini"],
        "context_size": 128000,
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com",
        "wire": "anthropic",
        "default_model": "claude-sonnet-4-5-20250929",
        "suggested_models": ["claude-sonnet-4-5-20250929", "claude-haiku-4-5-20251001", "claude-opus-4-5-20251101", "claude-sonnet-4-20250514"],
        "context_size": 200000,
    },
    "google": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "wire": "google",
        "default_model": "gemini-2.5-flash",
        "suggested_models": ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"],
        "context_size": 1000000,
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "wire": "openai",
        "default_model": "deepseek-chat",
        "suggested_models": ["deepseek-chat", "deepseek-reasoner"],
        "context_size": 64000,
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "wire": "openai",
        "default_model": "llama-3.3-70b-versatile",
        "suggested_models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        "context_size": 128000,
    },
    "xai": {
        "base_url": "https://api.x.ai/v1",
        "wire": "openai",
        "default_model": "grok-3",
        "suggested_models": ["grok-4-latest", "grok-3", "grok-3-mini", "grok-3-fast"],
        "context_size": 131072,
    },
    "kimi": {
        "base_url": "https://api.moonshot.ai/v1",
        "wire": "openai",
        "default_model": "kimi-k2.6",
        "suggested_models": ["kimi-k2.6", "kimi-k2.5", "kimi-for-coding"],
        "context_size": 256000,
    },
    "kimi-cn": {
        "base_url": "https://api.moonshot.cn/v1",
        "wire": "openai",
        "default_model": "kimi-k2.6",
        "suggested_models": ["kimi-k2.6", "kimi-k2.5", "kimi-for-coding"],
        "context_size": 256000,
    },
    "zhipu": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "wire": "openai",
        "default_model": "glm-4.6",
        "suggested_models": ["glm-4.6", "glm-4.5", "glm-4.5-flash", "glm-4-plus", "glm-4-flash"],
        "context_size": 128000,
    },
    "minimax": {
        "base_url": "https://api.minimaxi.com/anthropic",
        "wire": "anthropic",
        "default_model": "MiniMax-M2.7-highspeed",
        "suggested_models": ["MiniMax-M2.7", "MiniMax-M2.7-highspeed", "MiniMax-M2.5"],
        "context_size": 200000,
    },
    "minimax-global": {
        "base_url": "https://api.minimax.io/anthropic",
        "wire": "anthropic",
        "default_model": "MiniMax-M2.7",
        "suggested_models": ["MiniMax-M2.7", "MiniMax-M2.5"],
        "context_size": 200000,
    },
    "bailian": {
        "base_url": "https://coding.dashscope.aliyuncs.com/v1",
        "wire": "openai",
        "default_model": "qwen3.6-plus",
        "suggested_models": ["qwen3.6-plus", "qwen3.5-plus", "qwen3-coder-plus"],
        "context_size": 131072,
    },
    "volcengine": {
        "base_url": "https://ark.cn-beijing.volces.com/api/coding/v3",
        "wire": "openai",
        "default_model": "Doubao-Seed-2.0-Code",
        "suggested_models": ["Doubao-Seed-2.0-Code", "Doubao-Seed-2.0-pro", "Doubao-Seed-2.0-lite"],
        "context_size": 128000,
    },
    "xiaomi": {
        "base_url": "https://api.xiaomimimo.com/v1",
        "wire": "openai",
        "default_model": "mimo-v2-pro",
        "suggested_models": ["mimo-v2-pro", "mimo-v2-omni", "mimo-v2-flash"],
        "context_size": 131072,
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "wire": "openai",
        "default_model": "",
        "suggested_models": [],
        "context_size": 32768,
    },
    "custom": {
        "base_url": "",
        "wire": "openai",
        "default_model": "",
        "suggested_models": [],
        "context_size": 128000,
    },
}


def _resolve_wire(provider: str, config: dict) -> str:
    """Determine the wire protocol (openai / anthropic / google)."""
    wire = config.get("wire")
    if wire:
        return wire
    preset = PROVIDER_PRESETS.get(provider, {})
    return preset.get("wire", "openai")


class LLMClient:
    """Multi-provider LLM client."""

    def __init__(self, config: dict | None = None, provider: str | None = None):
        provider = provider or os.environ.get("WIKI_CLI_LLM_PROVIDER", "minimax")
        preset = PROVIDER_PRESETS.get(provider, {})

        self.provider = provider
        self.wire = _resolve_wire(provider, config or {})

        self.config = {
            "base_url": preset.get("base_url", ""),
            "model": preset.get("default_model", ""),
            "max_tokens": 4096,
            "temperature": 0.7,
        }
        if config:
            self.config.update(config)

        self.api_key = (
            os.environ.get("WIKI_CLI_LLM_API_KEY")
            or os.environ.get("MINIMAX_CN_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("LLM_API_KEY")
            or ""
        )
        if not self.api_key:
            raise ValueError(
                "No API key found. Set one of: WIKI_CLI_LLM_API_KEY, "
                "MINIMAX_CN_API_KEY, OPENAI_API_KEY, LLM_API_KEY"
            )

        self.base_url = self.config["base_url"].rstrip("/")

    # ── Public API ────────────────────────────────────────────────────

    def generate(self, prompt: str, system: str = "", max_tokens: int | None = None) -> str:
        """Generate a completion (non-streaming)."""
        if self.wire == "openai":
            return self._generate_openai(prompt, system, max_tokens)
        elif self.wire == "anthropic":
            return self._generate_anthropic(prompt, system, max_tokens)
        elif self.wire == "google":
            return self._generate_google(prompt, system, max_tokens)
        else:
            return self._generate_openai(prompt, system, max_tokens)

    def generate_stream(self, prompt: str, system: str = "", max_tokens: int | None = None):
        """Generate a streaming completion (yields text tokens)."""
        if self.wire == "openai":
            yield from self._stream_openai(prompt, system, max_tokens)
        elif self.wire == "anthropic":
            yield from self._stream_anthropic(prompt, system, max_tokens)
        elif self.wire == "google":
            yield from self._stream_google(prompt, system, max_tokens)
        else:
            yield from self._stream_openai(prompt, system, max_tokens)

    # ── OpenAI Chat Completions wire ──────────────────────────────────

    def _openai_url(self) -> str:
        base = self.base_url
        if base.endswith("/v1") or base.endswith("/v1/"):
            return f"{base.rstrip('/')}/chat/completions"
        if "/chat/completions" in base:
            return base
        return f"{base}/chat/completions"

    def _openai_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _openai_body(self, prompt: str, system: str, max_tokens: int | None, stream: bool) -> dict:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        body = {
            "model": self.config["model"],
            "messages": messages,
            "max_tokens": max_tokens or self.config["max_tokens"],
            "stream": stream,
        }
        if self.config.get("temperature") is not None:
            body["temperature"] = self.config["temperature"]
        return body

    def _generate_openai(self, prompt: str, system: str, max_tokens: int | None) -> str:
        url = self._openai_url()
        payload = self._openai_body(prompt, system, max_tokens, stream=False)
        resp = requests.post(url, headers=self._openai_headers(), json=payload, timeout=600, proxies=self._get_proxies())
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

    def _stream_openai(self, prompt: str, system: str, max_tokens: int | None):
        url = self._openai_url()
        payload = self._openai_body(prompt, system, max_tokens, stream=True)
        resp = requests.post(url, headers=self._openai_headers(), json=payload, stream=True, timeout=600, proxies=self._get_proxies())
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            if line.startswith(b"data: "):
                data_str = line[6:].decode("utf-8")
                if data_str.strip() == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    delta = data.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield content
                except json.JSONDecodeError:
                    continue

    # ── Anthropic Messages wire ───────────────────────────────────────

    def _anthropic_url(self) -> str:
        base = self.base_url
        if base.endswith("/v1/messages"):
            return base
        if base.endswith("/v1"):
            return f"{base}/messages"
        return f"{base}/v1/messages"

    def _anthropic_headers(self) -> dict:
        headers = {
            "Content-Type": "application/json",
        }
        requires_bearer = (
            "minimax" in self.base_url.lower()
            or "dashscope" in self.base_url.lower()
        )
        if requires_bearer:
            headers["Authorization"] = f"Bearer {self.api_key}"
        else:
            headers["x-api-key"] = self.api_key
            headers["anthropic-version"] = "2023-06-01"
        return headers

    def _anthropic_body(self, prompt: str, system: str, max_tokens: int | None, stream: bool) -> dict:
        payload = {
            "model": self.config["model"],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens or self.config["max_tokens"],
            "stream": stream,
        }
        if self.config.get("temperature") is not None:
            payload["temperature"] = self.config["temperature"]
        if system:
            payload["system"] = system
        return payload

    def _generate_anthropic(self, prompt: str, system: str, max_tokens: int | None) -> str:
        url = self._anthropic_url()
        payload = self._anthropic_body(prompt, system, max_tokens, stream=False)
        resp = requests.post(url, headers=self._anthropic_headers(), json=payload, timeout=600, proxies=self._get_proxies())
        resp.raise_for_status()
        data = resp.json()
        content = data.get("content", [])
        if isinstance(content, list):
            for block in content:
                if block.get("type") == "text":
                    return block.get("text", "").strip()
        return str(content)

    def _stream_anthropic(self, prompt: str, system: str, max_tokens: int | None):
        url = self._anthropic_url()
        payload = self._anthropic_body(prompt, system, max_tokens, stream=True)
        resp = requests.post(url, headers=self._anthropic_headers(), json=payload, stream=True, timeout=600, proxies=self._get_proxies())
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            if line.startswith(b"data: "):
                data_str = line[6:].decode("utf-8")
                if data_str.strip() == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    delta = data.get("delta", {})
                    if delta.get("type") == "text_delta":
                        text = delta.get("text", "")
                        if text:
                            yield text
                except json.JSONDecodeError:
                    continue

    # ── Google Gemini wire ────────────────────────────────────────────

    def _google_url(self, stream: bool = False) -> str:
        model = self.config["model"]
        base = self.base_url.rstrip("/")
        url = f"{base}/models/{model}:streamGenerateContent" if stream else f"{base}/models/{model}:generateContent"
        if stream:
            url += "?alt=sse"
        return url

    def _google_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }

    def _google_body(self, prompt: str, system: str, max_tokens: int | None) -> dict:
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        body = {"contents": contents}
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        gen_config = {}
        if self.config.get("temperature") is not None:
            gen_config["temperature"] = self.config["temperature"]
        if max_tokens or self.config.get("max_tokens"):
            gen_config["maxOutputTokens"] = max_tokens or self.config["max_tokens"]
        if gen_config:
            body["generationConfig"] = gen_config
        return body

    def _generate_google(self, prompt: str, system: str, max_tokens: int | None) -> str:
        url = self._google_url(stream=False)
        payload = self._google_body(prompt, system, max_tokens)
        resp = requests.post(url, headers=self._google_headers(), json=payload, timeout=600, proxies=self._get_proxies())
        resp.raise_for_status()
        data = resp.json()
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        texts = [p.get("text", "") for p in parts if not p.get("thought") and "text" in p]
        return "".join(texts).strip()

    def _stream_google(self, prompt: str, system: str, max_tokens: int | None):
        url = self._google_url(stream=True)
        payload = self._google_body(prompt, system, max_tokens)
        resp = requests.post(url, headers=self._google_headers(), json=payload, stream=True, timeout=600, proxies=self._get_proxies())
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            if line.startswith(b"data: "):
                data_str = line[6:].decode("utf-8")
                try:
                    data = json.loads(data_str)
                    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                    for p in parts:
                        if not p.get("thought") and "text" in p:
                            yield p["text"]
                except json.JSONDecodeError:
                    continue

    # ── Helpers ───────────────────────────────────────────────────────

    def _get_proxies(self) -> dict:
        proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
        if proxy:
            return {"http": proxy, "https": proxy}
        return {}


def create_llm_client(wiki_path: str = ".") -> LLMClient:
    """Create an LLMClient from project config (wiki-cli.yaml + .env + env vars)."""
    from wiki_cli.core.config import Config
    cfg = Config.load(wiki_path)
    llm_cfg = cfg.llm
    provider = llm_cfg.get("provider", "minimax")
    preset = PROVIDER_PRESETS.get(provider, {})

    config = {}
    for key in ("max_tokens", "temperature"):
        val = llm_cfg.get(key)
        if val:
            config[key] = val

    base_url = llm_cfg.get("base_url", "")
    default_base = PROVIDER_PRESETS.get("minimax", {}).get("base_url", "")
    if base_url and base_url != default_base:
        config["base_url"] = base_url
    elif preset.get("base_url"):
        config["base_url"] = preset["base_url"]

    model = llm_cfg.get("model", "")
    default_model = PROVIDER_PRESETS.get("minimax", {}).get("default_model", "")
    preset_model = preset.get("default_model", "")
    if model and model != default_model:
        config["model"] = model
    elif preset_model:
        config["model"] = preset_model

    wire = llm_cfg.get("wire", "")
    if wire:
        config["wire"] = wire

    return LLMClient(config=config, provider=provider)
