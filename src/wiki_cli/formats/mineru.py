"""MinerU integration for wiki-cli.

MinerU (magic-pdf) is a high-quality document-to-markdown converter.
This module wraps the MinerU CLI, handling:
  - Detecting the correct Python interpreter in conda/venv environments
  - Nested output structures (论文名/hybrid_auto/论文名.md + images/)
  - Proper CLI invocation with configurable python / cli paths
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ── Default paths ───────────────────────────────────────────────────────

# Common locations where the MinerU conda env might live.
_CANDIDATE_PYTHONS = [
    "python",
    "python3",
    # Conda envs
    os.path.expanduser("~/miniconda3/envs/mineru/bin/python"),
    os.path.expanduser("~/anaconda3/envs/mineru/bin/python"),
    os.path.expanduser("~/.conda/envs/mineru/bin/python"),
    # Magic-PDF specific env name variants
    os.path.expanduser("~/miniconda3/envs/magic-pdf/bin/python"),
    os.path.expanduser("~/anaconda3/envs/magic-pdf/bin/python"),
]

_CANDIDATE_CLIS = [
    "magic-pdf",
]


class MinerURunner:
    """Wrapper around the MinerU (magic-pdf) command-line tool.

    Parameters
    ----------
    config : dict, optional
        Configuration dict (typically ``Config.mineru``).
        Recognised keys:
        - python_path : str   — Python interpreter path (default: auto-detect)
        - cli_path    : str   — magic-pdf CLI path (default: auto-detect)
        - method      : str   — extraction method: 'auto' | 'ocr' | 'txt'
        - output_format : str — 'markdown' | 'json'
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        cfg = config or {}
        self.python_path: str = cfg.get("python_path", "")
        self.cli_path: str = cfg.get("cli_path", "")
        self.method: str = cfg.get("method", "auto")
        self.output_format: str = cfg.get("output_format", "markdown")

        # Auto-detect if not explicitly set
        if not self.python_path:
            self.python_path = self._detect_python()
        if not self.cli_path:
            self.cli_path = self._detect_cli(self.python_path)

    # ── Public API ──────────────────────────────────────────────────────

    def convert(
        self,
        input_path: str | Path,
        output_dir: str | Path,
    ) -> Path:
        """Convert a document to markdown using MinerU.

        Parameters
        ----------
        input_path : path
            Path to the input file (PDF, etc.).
        output_dir : path
            Directory where MinerU output will be written.

        Returns
        -------
        Path
            Path to the generated markdown file.

        Raises
        ------
        FileNotFoundError
            If *input_path* doesn't exist.
        RuntimeError
            If the MinerU process fails.
        """
        input_path = Path(input_path).resolve()
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        cmd = self._build_command(input_path, output_dir)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 min timeout for large PDFs
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"MinerU failed (exit {result.returncode}):\n"
                f"CMD: {' '.join(cmd)}\n"
                f"STDOUT: {result.stdout[:2000]}\n"
                f"STDERR: {result.stderr[:2000]}"
            )

        # Locate the generated markdown in the (potentially nested) output
        md_path = self._find_output_markdown(output_dir, input_path.stem)
        return md_path

    def is_available(self) -> bool:
        """Return True if MinerU can be invoked."""
        try:
            cmd = [self.python_path, "-m", "magic_pdf.tools.common",
                   "--help"]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # Try direct CLI
            try:
                result = subprocess.run(
                    [self.cli_path, "--help"],
                    capture_output=True, text=True, timeout=30,
                )
                return result.returncode == 0
            except (FileNotFoundError, subprocess.TimeoutExpired):
                return False

    def version(self) -> Optional[str]:
        """Return the MinerU version string, or None if unavailable."""
        try:
            result = subprocess.run(
                [self.python_path, "-c", "import magic_pdf; print(magic_pdf.__version__)"],
                capture_output=True, text=True, timeout=15,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return None

    # ── Command construction ────────────────────────────────────────────

    def _build_command(self, input_path: Path, output_dir: Path) -> List[str]:
        """Build the CLI command list."""
        # MinerU v0.6+ uses: magic-pdf -p <input> -o <output_dir> -m <method>
        # Older versions:   python -m magic_pdf.tools.common ...
        # We prefer the direct CLI if available.
        if shutil.which(self.cli_path):
            cmd = [
                self.cli_path,
                "-p", str(input_path),
                "-o", str(output_dir),
                "-m", self.method,
            ]
        else:
            # Fall back to python -m invocation
            cmd = [
                self.python_path,
                "-m", "magic_pdf.tools.common",
                "-p", str(input_path),
                "-o", str(output_dir),
                "-m", self.method,
            ]
        return cmd

    # ── Output detection ────────────────────────────────────────────────

    @staticmethod
    def _find_output_markdown(output_dir: Path, stem: str) -> Path:
        """Locate the generated markdown inside MinerU's nested output.

        MinerU creates output like:
          output_dir/<stem>/auto/<stem>.md    (or hybrid_auto / ocr)
          output_dir/<stem>/<stem>.md         (newer versions)
          output_dir/<stem>.md                (flat output)
        """
        # Strategy 1: stem/stem.md or stem/hybrid_auto/stem.md etc.
        candidate = output_dir / stem / f"{stem}.md"
        if candidate.exists():
            return candidate

        # Search one level deeper for method subdirectory
        stem_dir = output_dir / stem
        if stem_dir.exists():
            for subdir in stem_dir.iterdir():
                if subdir.is_dir():
                    candidate = subdir / f"{stem}.md"
                    if candidate.exists():
                        return candidate
                    # Some versions use different names
                    for md in subdir.glob("*.md"):
                        return md

        # Strategy 2: flat output
        flat = output_dir / f"{stem}.md"
        if flat.exists():
            return flat

        # Strategy 3: recursive search
        candidates = list(output_dir.rglob(f"{stem}.md"))
        if candidates:
            return candidates[0]

        # Strategy 4: any markdown file at all
        any_md = list(output_dir.rglob("*.md"))
        if any_md:
            return any_md[0]

        raise FileNotFoundError(
            f"MinerU produced no markdown output in {output_dir}. "
            f"Searched for {stem}.md recursively."
        )

    # ── Auto-detection ──────────────────────────────────────────────────

    @staticmethod
    def _detect_python() -> str:
        """Find a Python interpreter that has magic_pdf installed."""
        for candidate in _CANDIDATE_PYTHONS:
            expanded = os.path.expanduser(candidate)
            # Check if it exists and has magic_pdf
            try:
                result = subprocess.run(
                    [expanded, "-c", "import magic_pdf"],
                    capture_output=True, text=True, timeout=10,
                )
                if result.returncode == 0:
                    return expanded
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        # Default to whatever python3 is on PATH
        return sys.executable or "python3"

    @staticmethod
    def _detect_cli(python_path: str) -> str:
        """Find the magic-pdf CLI binary."""
        # Try which
        found = shutil.which("magic-pdf")
        if found:
            return found
        # Try python -m invocation pattern
        return "magic-pdf"

    def __repr__(self) -> str:
        return (
            f"<MinerURunner python={self.python_path!r} "
            f"cli={self.cli_path!r} method={self.method!r}>"
        )
