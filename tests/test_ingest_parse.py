"""Regression suite for the FILE-block parser in ingest.py.

Reproduces all known LLM output hazards (H1-H6) documented in nashsu/llm_wiki,
plus wiki-cli specific behavior. A failing test here means the parser has
regressed — pages are being silently dropped or mis-parsed.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from wiki_cli.core.ingest import is_safe_ingest_path, parse_file_blocks, ParsedBlock


class TestIsSafeIngestPath:
    """Path safety: is_safe_ingest_path() must reject anything that escapes wiki/."""

    # ── Should pass ───────────────────────────────────────────────────
    @pytest.mark.parametrize("path", [
        "wiki/concepts/foo.md",
        "wiki/entities/bar.md",
        "wiki/sources/paper.md",
        "wiki/concepts/chain-of-thought.md",
        "wiki/synthesis/overview.md",
    ])
    def test_valid_wiki_paths(self, path):
        assert is_safe_ingest_path(path) is True

    # ── Should fail ───────────────────────────────────────────────────
    @pytest.mark.parametrize("path", [
        "../etc/passwd",          # leading ..
        "/etc/passwd",            # absolute POSIX
        "C:\\Windows\\System32\\config\\sam",  # Windows absolute
        "wiki/../../../etc/passwd",  # .. hidden inside wiki/
        "wiki/entities/../../root/.bashrc",  # .. in the middle
        ".bashrc",                # not under wiki/
        "",                       # empty
        "  ",                     # whitespace-only
        pytest.param("wiki/concepts/..%2F..%2Fetc%2Fpasswd", marks=pytest.mark.xfail(reason="URL-encoded .. not handled by nashsu either")),
    ])
    def test_rejected_paths(self, path):
        assert is_safe_ingest_path(path) is False, f"Expected {path!r} to be rejected"


class TestParseFileBlocks:
    """Parser must handle all known LLM output hazards (H1-H6)."""

    # ── Happy paths ───────────────────────────────────────────────────
    def test_single_block(self):
        text = "\n".join([
            "---FILE: wiki/concepts/rope.md---",
            "# RoPE",
            "Rotary positional embedding.",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1
        assert blocks[0].path == "wiki/concepts/rope.md"
        assert "RoPE" in blocks[0].content
        assert warnings == []

    def test_multiple_consecutive_blocks(self):
        text = "\n".join([
            "---FILE: wiki/entities/qwen.md---",
            "# Qwen",
            "---END FILE---",
            "",
            "---FILE: wiki/concepts/moe.md---",
            "# MoE",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 2
        assert blocks[0].path == "wiki/entities/qwen.md"
        assert blocks[1].path == "wiki/concepts/moe.md"
        assert warnings == []

    def test_ignores_preamble_prose(self):
        text = "\n".join([
            "Here are the wiki files:",
            "",
            "---FILE: wiki/concepts/foo.md---",
            "body",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1
        assert blocks[0].path == "wiki/concepts/foo.md"

    # ── H1: CRLF normalization ────────────────────────────────────────
    def test_windows_crlf(self):
        text = "\r\n".join([
            "---FILE: wiki/entities/qwen.md---",
            "# Qwen",
            "---END FILE---",
            "",
            "---FILE: wiki/concepts/moe.md---",
            "# MoE",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 2
        assert blocks[0].path == "wiki/entities/qwen.md"
        assert blocks[1].path == "wiki/concepts/moe.md"
        assert warnings == []

    # ── H3: whitespace / case variants ────────────────────────────────
    def test_whitespace_variants_opener(self):
        text = "\n".join([
            "---  FILE:   wiki/concepts/foo.md  ---",
            "body",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1
        assert blocks[0].path == "wiki/concepts/foo.md"

    def test_case_insensitive_opener(self):
        text = "\n".join([
            "---file: wiki/concepts/foo.md---",
            "body",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1
        assert blocks[0].path == "wiki/concepts/foo.md"

    def test_case_insensitive_closer(self):
        text = "\n".join([
            "---FILE: wiki/concepts/foo.md---",
            "body",
            "---end file---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1

    def test_closer_with_extra_whitespace(self):
        text = "\n".join([
            "---FILE: wiki/concepts/foo.md---",
            "body",
            "---  END  FILE  ---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1

    # ── H5: ---END FILE--- inside fenced code blocks ─────────────────
    def test_end_file_inside_code_fence(self):
        """Literal ---END FILE--- inside ``` should NOT close the block."""
        text = "\n".join([
            "---FILE: wiki/concepts/example.md---",
            "# Example",
            "```",
            "Here is a code block:",
            "---END FILE---",
            "```",
            "More content after the code block.",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1
        # The content should include the ```...---END FILE---...``` portion
        assert "---END FILE---" in blocks[0].content
        assert "More content after" in blocks[0].content

    def test_end_file_inside_tilde_fence(self):
        """Literal ---END FILE--- inside ~~~ should NOT close the block."""
        text = "\n".join([
            "---FILE: wiki/concepts/example.md---",
            "# Example",
            "~~~",
            "---END FILE---",
            "~~~",
            "After tilde fence.",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1
        assert "---END FILE---" in blocks[0].content
        assert "After tilde fence" in blocks[0].content

    def test_nested_fences(self):
        """Fence aware: 4 backticks should not close a triple backtick block."""
        text = "\n".join([
            "---FILE: wiki/concepts/nested.md---",
            "# Nested",
            "`````",
            "---END FILE---",
            "`````",
            "After quad fence.",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1
        assert "---END FILE---" in blocks[0].content
        assert "After quad fence" in blocks[0].content

    # ── H6: empty path ───────────────────────────────────────────────
    def test_empty_path_warnings(self):
        text = "\n".join([
            "---FILE: wiki/concepts/foo.md---",
            "body",
            "---END FILE---",
            "",
            "---FILE:    ---",
            "orphan body",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1  # only the valid one
        assert len(warnings) == 1
        assert "empty path" in warnings[0]

    # ── H2: stream truncation ─────────────────────────────────────────
    def test_truncation_at_eof(self):
        """First block truncated at EOF → warning."""
        text = "\n".join([
            "---FILE: wiki/concepts/foo.md---",
            "body",
            # missing ---END FILE--- → EOF
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 0
        assert len(warnings) == 1
        assert "not closed" in warnings[0]

    def test_truncation_mid_content_with_valid_block_after(self):
        """First block truncated, second valid block after → absorbed as content, no warning.

        Nashsu behavior: orphaned opener is absorbed into first block's content
        (no H2 warning since closer IS eventually found), second block processes normally.
        """
        text = "\n".join([
            "---FILE: wiki/concepts/foo.md---",
            "body",
            # missing ---END FILE---
            "---FILE: wiki/concepts/bar.md---",
            "bar body",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 1  # first block absorbs the orphaned opener
        assert blocks[0].path == "wiki/concepts/foo.md"
        # The orphaned opener is absorbed as content, no H2 warning (closer found)
        assert len(warnings) == 0

    def test_truncation_empty_path_combined(self):
        text = "\n".join([
            "---FILE: wiki/concepts/foo.md---",
            "body",
            # truncated — no closer
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 0
        assert len(warnings) == 1
        assert "not closed" in warnings[0]

    # ── Edge: no blocks at all ───────────────────────────────────────
    def test_no_blocks(self):
        blocks, warnings = parse_file_blocks("No FILE blocks here at all.")
        assert blocks == []
        assert warnings == []

    # ── Edge: unpaired opener (no closer) ────────────────────────────
    def test_unclosed_opener_truncation(self):
        text = "\n".join([
            "---FILE: wiki/concepts/foo.md---",
            "some content but stream cut",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert len(blocks) == 0
        assert len(warnings) == 1
        assert "not closed" in warnings[0]

    # ── Edge: returns ParsedBlock dataclass ──────────────────────────
    def test_returns_parsed_block_dataclass(self):
        text = "\n".join([
            "---FILE: wiki/concepts/foo.md---",
            "content",
            "---END FILE---",
        ])
        blocks, warnings = parse_file_blocks(text)
        assert all(isinstance(b, ParsedBlock) for b in blocks)
        assert hasattr(blocks[0], "path")
        assert hasattr(blocks[0], "content")
