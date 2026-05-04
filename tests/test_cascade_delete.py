"""Tests for cascade_delete module."""

import pytest
from pathlib import Path
import tempfile
import shutil
import os
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from wiki_cli.core.cascade_delete import (
    _normalize_key,
    _slug_from_path,
    _strip_wikilinks_in_body,
    _rewrite_frontmatter_related,
    _strip_index_entries,
    cascade_delete_page,
)


class TestNormalizeKey:
    def test_basic(self):
        assert _normalize_key("alice-chen") == _normalize_key("alicechen")
        assert _normalize_key("alice-chen") == _normalize_key("AliceChen")
        assert _normalize_key("gpt-4o") == _normalize_key("gpt4o")
        assert _normalize_key("hello_world") == _normalize_key("hello-world")


class TestSlugFromPath:
    def test_entities(self):
        p = Path("wiki/entities/gpt-4.md")
        assert _slug_from_path(p) == "gpt-4"

    def test_concepts(self):
        p = Path("wiki/concepts/chain-of-thought.md")
        assert _slug_from_path(p) == "chain-of-thought"


class TestStripWikilinksInBody:
    def test_simple_wikilink_deleted(self):
        keys = {_normalize_key("gpt-4")}
        content = "See [[gpt-4]] for details."
        result = _strip_wikilinks_in_body(content, keys)
        assert result == "See gpt-4 for details."

    def test_wikilink_with_alias_deleted(self):
        keys = {_normalize_key("gpt-4")}
        content = "Check [[gpt-4|the model]] here."
        result = _strip_wikilinks_in_body(content, keys)
        assert result == "Check the model here."

    def test_wikilink_kept(self):
        keys = {_normalize_key("gpt-4")}
        content = "See [[gpt-4]] and [[gpt-3.5]]."
        result = _strip_wikilinks_in_body(content, keys)
        assert result == "See gpt-4 and [[gpt-3.5]]."

    def test_alias_kept_when_not_deleted(self):
        keys = set()
        content = "Check [[gpt-4|the model]] here."
        result = _strip_wikilinks_in_body(content, keys)
        assert result == "Check [[gpt-4|the model]] here."


class TestRewriteFrontmatterRelated:
    def test_inline_array_removes_deleted(self):
        raw = '---\nrelated: [[gpt-4]], [[gpt-3.5]], [[claude-2]]\n---\n# Body'
        keys = {_normalize_key("gpt-4"), _normalize_key("claude-2")}
        result = _rewrite_frontmatter_related(raw, keys)
        assert "gpt-4" not in result
        assert "claude-2" not in result
        assert "gpt-3.5" in result

    def test_preserves_non_deleted(self):
        raw = '---\nrelated: [[gpt-3.5]]\n---\n# Body'
        keys = {_normalize_key("gpt-4")}
        result = _rewrite_frontmatter_related(raw, keys)
        assert "gpt-3.5" in result


class TestStripIndexEntries:
    def test_removes_deleted_entry(self):
        content = """# Wiki Index
## Entities
- [[gpt-4]] — GPT-4
- [[gpt-3.5]] — GPT-3.5
"""
        keys = {_normalize_key("gpt-4")}
        result = _strip_index_entries(content, keys)
        assert "gpt-4" not in result
        assert "gpt-3.5" in result

    def test_keeps_non_deleted(self):
        content = "# Wiki Index\n- [[gpt-3.5]] — GPT-3.5\n"
        keys = {_normalize_key("gpt-4")}
        result = _strip_index_entries(content, keys)
        assert result == content


class TestCascadeDeletePage:
    def test_deletes_file_and_cleans_references(self, tmp_path):
        """Integration test: create a mini wiki, delete one page, verify refs cleaned."""
        wiki_root = tmp_path / "wiki"
        wiki_root.mkdir()
        (wiki_root / "entities").mkdir()
        (wiki_root / "concepts").mkdir()

        # Page to be deleted
        victim = wiki_root / "entities" / "gpt-4.md"
        victim.write_text("---\ntitle: GPT-4\nrelated: [[gpt-3.5]]\nsources: []\n---\n# GPT-4\nSee [[gpt-4]] or [[claude-2]].\n")

        # Referencing page
        ref = wiki_root / "concepts" / "llms.md"
        ref.write_text("---\nrelated: [[gpt-4]], [[gpt-3.5]]\n---\n# LLMs\n[[gpt-4]] is a model. Also see [[gpt-4|our model]].\n")

        # Index
        index = wiki_root / "index.md"
        index.write_text("# Wiki Index\n- [[gpt-4]] — GPT-4\n- [[gpt-3.5]] — GPT-3.5\n")

        result = cascade_delete_page(tmp_path, victim)

        assert not victim.exists(), "gpt-4.md should be deleted"
        assert "gpt-4" not in index.read_text(), "index.md entry should be removed"

        ref_content = ref.read_text()
        assert "[[gpt-4]]" not in ref_content, "wikilink in body should be stripped"
        assert "gpt-3.5" in ref_content, "gpt-3.5 reference should remain"
        # Alias should be preserved as plain text
        assert "our model" in ref_content
