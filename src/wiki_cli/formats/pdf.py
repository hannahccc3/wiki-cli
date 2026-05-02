"""PDF format handler for wiki-cli.

Strategy (in order of preference):
  1. MinerU — high-quality structured markdown extraction
  2. pdfplumber — pure-Python fallback for text + table extraction

Provides a single public entry-point:

    extract(pdf_path, output_dir, config) -> ExtractionResult
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .mineru import MinerURunner


# ── Result container ────────────────────────────────────────────────────

@dataclass
class ExtractionResult:
    """Result of a PDF extraction."""
    source: str                         # original PDF filename
    method: str                         # 'mineru' | 'pdfplumber'
    markdown: str                       # extracted markdown content
    images: List[Path] = field(default_factory=list)  # extracted image paths
    tables: List[str] = field(default_factory=list)    # markdown tables
    metadata: Dict[str, Any] = field(default_factory=dict)
    output_path: Optional[Path] = None  # path to written output file

    def write(self, dest: Path) -> Path:
        """Write the extracted markdown to *dest*."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(self.markdown, encoding="utf-8")
        self.output_path = dest
        return dest


# ── Public API ──────────────────────────────────────────────────────────

def extract(
    pdf_path: str | Path,
    output_dir: str | Path | None = None,
    config: Optional[Dict[str, Any]] = None,
) -> ExtractionResult:
    """Extract content from a PDF file.

    Parameters
    ----------
    pdf_path : path
        Path to the input PDF.
    output_dir : path, optional
        Directory for MinerU intermediate output.  If *None*, a temporary
        directory is used.
    config : dict, optional
        MinerU configuration (``Config.mineru``).  If *None*, defaults
        are used.

    Returns
    -------
    ExtractionResult
        Structured extraction result.
    """
    pdf_path = Path(pdf_path).resolve()
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    config = config or {}
    force_method = config.get("method", "auto")

    # Try MinerU first (unless explicitly forced to pdfplumber)
    if force_method != "pdfplumber":
        try:
            return _extract_mineru(pdf_path, output_dir, config)
        except Exception:
            # MinerU unavailable or failed → fall through to pdfplumber
            if force_method == "mineru":
                raise  # user explicitly asked for MinerU

    # Fallback: pdfplumber
    return _extract_pdfplumber(pdf_path)


# ── MinerU extraction ──────────────────────────────────────────────────

def _extract_mineru(
    pdf_path: Path,
    output_dir: str | Path | None,
    config: Dict[str, Any],
) -> ExtractionResult:
    """Use MinerU to convert a PDF to structured markdown."""
    import tempfile

    runner = MinerURunner(config)
    if not runner.is_available():
        raise RuntimeError("MinerU is not available")

    out = Path(output_dir) if output_dir else Path(tempfile.mkdtemp(prefix="wiki-pdf-"))
    out.mkdir(parents=True, exist_ok=True)

    md_path = runner.convert(pdf_path, out)
    markdown = md_path.read_text(encoding="utf-8")

    # Collect any images MinerU extracted
    images = sorted(
        p for p in out.rglob("*")
        if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
    )

    # Collect embedded tables (MinerU renders them as markdown tables)
    tables = _extract_tables_from_markdown(markdown)

    return ExtractionResult(
        source=pdf_path.name,
        method="mineru",
        markdown=markdown,
        images=images,
        tables=tables,
        metadata={"runner": repr(runner)},
    )


# ── pdfplumber extraction ──────────────────────────────────────────────

def _extract_pdfplumber(pdf_path: Path) -> ExtractionResult:
    """Use pdfplumber as a pure-Python fallback."""
    try:
        import pdfplumber  # type: ignore[import-untyped]
    except ImportError:
        raise ImportError(
            "pdfplumber is not installed. "
            "Install it with: pip install pdfplumber"
        ) from None

    pages_text: List[str] = []
    tables: List[str] = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            # Extract text
            text = page.extract_text() or ""
            if text.strip():
                pages_text.append(f"<!-- Page {i} -->\n\n{text}")

            # Extract tables
            page_tables = page.extract_tables()
            for tbl in page_tables:
                if not tbl:
                    continue
                md_tbl = _table_to_markdown(tbl)
                if md_tbl:
                    tables.append(md_tbl)

        metadata = {
            "pages": len(pdf.pages),
        }
        # PDF metadata
        if pdf.metadata:
            metadata.update({k: str(v) for k, v in pdf.metadata.items() if v})

    markdown = "\n\n---\n\n".join(pages_text)

    # Prepend a title from PDF metadata if available
    title = pdf_path.stem.replace("-", " ").replace("_", " ").title()
    header = f"# {title}\n\n"
    markdown = header + markdown

    return ExtractionResult(
        source=pdf_path.name,
        method="pdfplumber",
        markdown=markdown,
        images=[],
        tables=tables,
        metadata=metadata,
    )


# ── Helpers ─────────────────────────────────────────────────────────────

def _extract_tables_from_markdown(text: str) -> List[str]:
    """Find markdown table blocks in *text*."""
    # A markdown table is a sequence of lines starting with |
    tables: List[str] = []
    lines = text.split("\n")
    current: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            current.append(stripped)
        else:
            if len(current) >= 2:
                tables.append("\n".join(current))
            current = []
    if len(current) >= 2:
        tables.append("\n".join(current))
    return tables


def _table_to_markdown(rows: List[List[Any]]) -> str:
    """Convert a list-of-lists (from pdfplumber) to a markdown table."""
    if not rows or not rows[0]:
        return ""

    # Normalise: ensure all rows have the same number of columns
    max_cols = max(len(r) for r in rows)
    normalised: List[List[str]] = []
    for row in rows:
        cells = [(c if c is not None else "").replace("\n", " ").strip() for c in row]
        cells += [""] * (max_cols - len(cells))
        normalised.append(cells)

    header = normalised[0]
    separator = ["---"] * max_cols
    body = normalised[1:]

    def _fmt(row: List[str]) -> str:
        return "| " + " | ".join(row) + " |"

    lines = [_fmt(header), _fmt(separator)]
    lines.extend(_fmt(r) for r in body)
    return "\n".join(lines)
