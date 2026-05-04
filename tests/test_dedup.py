"""Tests for dedup module."""

import pytest
from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from wiki_cli.core.dedup import (
    _normalize_key,
    _normalize_group_key,
    _parse_detector_response,
    _extract_first_json_object,
    _build_detector_user_message,
    _rewrite_cross_references,
    _parse_frontmatter,
    _merge_array_fields,
    EntitySummary,
    DuplicateGroup,
)


class TestNormalizeKey:
    def test_basic(self):
        assert _normalize_key("alice-chen") == _normalize_key("AliceChen")
        assert _normalize_key("gpt-4") == _normalize_key("gpt4")


class TestNormalizeGroupKey:
    def test_sorted_key(self):
        assert _normalize_group_key(["b", "a", "c"]) == _normalize_group_key(["c", "b", "a"])


class TestExtractFirstJsonObject:
    def test_basic(self):
        text = '{"groups": [{"slugs": ["a", "b"]}]} and some prose'
        assert _extract_first_json_object(text) == '{"groups": [{"slugs": ["a", "b"]}]}'

    def test_with_code_fence(self):
        text = '```json\n{"groups": []}\n```'
        assert _extract_first_json_object(text) == '{"groups": []}'

    def test_no_json(self):
        assert _extract_first_json_object("no json here") is None


class TestParseDetectorResponse:
    def test_valid_groups(self):
        raw = '{"groups": [{"slugs": ["gpt-4", "gpt4"], "reason": "same model", "confidence": "high"}]}'
        result = _parse_detector_response(raw)
        assert len(result) == 1
        assert result[0].slugs == ["gpt-4", "gpt4"]
        assert result[0].confidence == "high"

    def test_filters_single_element(self):
        raw = '{"groups": [{"slugs": ["only-one"]}]}'
        result = _parse_detector_response(raw)
        assert len(result) == 0

    def test_empty_groups(self):
        raw = '{"groups": []}'
        result = _parse_detector_response(raw)
        assert len(result) == 0


class TestBuildDetectorUserMessage:
    def test_format(self):
        summaries = [
            EntitySummary(slug="gpt-4", path="wiki/entities/gpt-4.md", ptype="entity",
                         title="GPT-4", tags=["llm", "model"]),
            EntitySummary(slug="gpt-3.5", path="wiki/entities/gpt-3.5.md", ptype="entity",
                         title="GPT-3.5", description="Language model"),
        ]
        msg = _build_detector_user_message(summaries)
        assert "gpt-4" in msg
        assert "gpt-3.5" in msg
        assert "llm, model" in msg
        assert "Language model" in msg


class TestRewriteCrossReferences:
    def test_rewrites_simple_wikilink(self):
        content = "See [[gpt-4]] for details."
        result = _rewrite_cross_references(content, {"gpt-4": "gpt-4o"})
        assert result == "See [[gpt-4o]] for details."

    def test_rewrites_alias_wikilink(self):
        content = "Check [[gpt-4|the model]] here."
        result = _rewrite_cross_references(content, {"gpt-4": "gpt-4o"})
        assert result == "Check [[gpt-4o|the model]] here."

    def test_preserves_non_redirected(self):
        content = "See [[gpt-3.5]]."
        result = _rewrite_cross_references(content, {"gpt-4": "gpt-4o"})
        assert result == content

    def test_related_array(self):
        content = "---\nrelated: [[gpt-4]], [[gpt-3.5]]\n---\nBody"
        result = _rewrite_cross_references(content, {"gpt-4": "gpt-4o"})
        assert "gpt-4o" in result
        assert "[[gpt-4o]]" in result
        assert "[[gpt-3.5]]" in result


class TestParseFrontmatter:
    def test_basic(self):
        raw = "---\ntype: entity\ntitle: GPT-4\n---\n# Body"
        fm, body = _parse_frontmatter(raw)
        assert fm["type"] == "entity"
        assert fm["title"] == "GPT-4"
        assert body == "# Body"

    def test_array_field(self):
        raw = "---\nrelated: [\"a\", \"b\"]\n---\n# Body"
        fm, body = _parse_frontmatter(raw)
        assert fm["related"] == ["a", "b"]


class TestMergeArrayFields:
    def test_union(self):
        merged = "---\nrelated: [\"a\"]\n---\n# Body"
        original = "---\nrelated: [\"b\", \"a\"]\n---\n# Body"
        result = _merge_array_fields(merged, original, ["related"])
        # Should have both "a" and "b"
        assert "a" in result
        assert "b" in result
