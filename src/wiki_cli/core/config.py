"""Configuration loader for wiki-cli.

Priority (lowest → highest):
  1. Built-in defaults
  2. wiki-cli.yaml  (project-level config file)
  3. .env file       (dotenv, for secrets)
  4. Environment variables

Supported environment variable overrides:
  WIKI_CLI_LLM_BASE_URL        → llm.base_url
  WIKI_CLI_LLM_API_KEY         → llm.api_key
  WIKI_CLI_LLM_MODEL           → llm.model
  WIKI_CLI_EMBEDDINGS_BASE_URL → embeddings.base_url
  WIKI_CLI_EMBEDDINGS_MODEL    → embeddings.model
  WIKI_CLI_MINERU_PYTHON       → mineru.python_path
  WIKI_CLI_MINERU_CLI          → mineru.cli_path
  WIKI_CLI_ZOTERO_API_KEY      → zotero.api_key
  WIKI_CLI_ZOTERO_USER_ID      → zotero.user_id
  WIKI_CLI_WIKI_PATH           → wiki.path
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    yaml = None  # graceful fallback — YAML config section will be skipped

try:
    from dotenv import load_dotenv  # type: ignore[import-untyped]
except ImportError:
    load_dotenv = None  # type: ignore[assignment]

# ── Defaults ────────────────────────────────────────────────────────────

_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "llm": {
        "provider": "minimax",
        "base_url": "https://api.minimaxi.com/anthropic",
        "api_key": "",
        "model": "MiniMax-M2.7-highspeed",
        "max_tokens": 8192,
        "temperature": 0.7,
        "wire": "",
    },
    "embeddings": {
        "base_url": "http://localhost:11434/v1",
        "api_key": "",
        "model": "qwen3-embedding:8b",
        "dimensions": 4096,
    },
    "mineru": {
        "python_path": "python",
        "cli_path": "magic-pdf",
        "method": "auto",
        "output_format": "markdown",
    },
    "zotero": {
        "api_key": "",
        "user_id": "",
        "library_type": "user",
    },
    "wiki": {
        "path": ".",
        "template": "research",
        "stale_days": 90,
        "min_outbound_links": 2,
    },
}

# Env-var → config path mapping
_ENV_MAP: Dict[str, tuple[str, str]] = {
    "WIKI_CLI_LLM_PROVIDER":       ("llm", "provider"),
    "WIKI_CLI_LLM_BASE_URL":       ("llm", "base_url"),
    "WIKI_CLI_LLM_API_KEY":        ("llm", "api_key"),
    "WIKI_CLI_LLM_MODEL":          ("llm", "model"),
    "WIKI_CLI_LLM_WIRE":           ("llm", "wire"),
    "WIKI_CLI_EMBEDDINGS_BASE_URL": ("embeddings", "base_url"),
    "WIKI_CLI_EMBEDDINGS_MODEL":    ("embeddings", "model"),
    "WIKI_CLI_MINERU_PYTHON":       ("mineru", "python_path"),
    "WIKI_CLI_MINERU_CLI":          ("mineru", "cli_path"),
    "WIKI_CLI_ZOTERO_API_KEY":      ("zotero", "api_key"),
    "WIKI_CLI_ZOTERO_USER_ID":      ("zotero", "user_id"),
    "WIKI_CLI_WIKI_PATH":           ("wiki", "path"),
}


class Config:
    """Immutable, merged configuration for wiki-cli.

    Usage::

        cfg = Config.load()                        # auto-detect .env & YAML
        cfg = Config.load(project_dir="/path/to")  # explicit project dir

        cfg.llm           # dict[str, Any]
        cfg.embeddings    # dict[str, Any]
        cfg.mineru        # dict[str, Any]
        cfg.zotero        # dict[str, Any]
        cfg.wiki          # dict[str, Any]
        cfg.get("llm", "model")  # shortcut
    """

    def __init__(self, data: Dict[str, Dict[str, Any]]) -> None:
        self._data = data

    # ── Sections (as plain dicts) ───────────────────────────────────────

    @property
    def llm(self) -> Dict[str, Any]:
        return self._data.get("llm", {})

    @property
    def embeddings(self) -> Dict[str, Any]:
        return self._data.get("embeddings", {})

    @property
    def mineru(self) -> Dict[str, Any]:
        return self._data.get("mineru", {})

    @property
    def zotero(self) -> Dict[str, Any]:
        return self._data.get("zotero", {})

    @property
    def wiki(self) -> Dict[str, Any]:
        return self._data.get("wiki", {})

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Shortcut: cfg.get('llm', 'model') → 'gpt-4o-mini'."""
        return self._data.get(section, {}).get(key, default)

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Return a plain dict copy of the full config."""
        import copy
        return copy.deepcopy(self._data)

    # ── Loader ──────────────────────────────────────────────────────────

    @classmethod
    def load(cls, project_dir: Optional[str] = None) -> "Config":
        """Build a Config by merging defaults ← YAML ← .env ← env vars."""
        project_path = Path(project_dir) if project_dir else Path.cwd()

        # Layer 1: deep-copy defaults
        import copy
        data: Dict[str, Dict[str, Any]] = copy.deepcopy(_DEFAULTS)

        # Layer 2: YAML file
        yaml_path = project_path / "wiki-cli.yaml"
        if yaml_path.exists() and yaml is not None:
            try:
                raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    _deep_merge(data, raw)
            except Exception:
                pass  # corrupt YAML → ignore silently

        # Layer 3: .env file
        env_path = project_path / ".env"
        if env_path.exists() and load_dotenv is not None:
            load_dotenv(env_path, override=False)

        # Also try the current working directory .env if different
        cwd_env = Path.cwd() / ".env"
        if cwd_env.exists() and cwd_env != env_path and load_dotenv is not None:
            load_dotenv(cwd_env, override=False)

        # Layer 4: Environment variable overrides
        for env_var, (section, key) in _ENV_MAP.items():
            val = os.environ.get(env_var)
            if val is not None:
                data.setdefault(section, {})[key] = val

        # Also honour some common env vars as fallbacks for API keys
        if not data["llm"].get("api_key"):
            for fallback in ("MINIMAX_CN_API_KEY", "OPENAI_API_KEY", "LLM_API_KEY"):
                key_val = os.environ.get(fallback)
                if key_val:
                    data["llm"]["api_key"] = key_val
                    break

        if not data["embeddings"].get("api_key"):
            data["embeddings"]["api_key"] = data["llm"].get("api_key", "")

        return cls(data)

    def __repr__(self) -> str:
        sections = ", ".join(self._data.keys())
        return f"<Config sections=[{sections}]>"


# ── Helpers ─────────────────────────────────────────────────────────────

def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge *override* into *base* (mutates base)."""
    for key, val in override.items():
        if (
            key in base
            and isinstance(base[key], dict)
            and isinstance(val, dict)
        ):
            _deep_merge(base[key], val)
        else:
            base[key] = val
    return base
