"""MCP (Model Context Protocol) server for wiki-cli.

Provides tools for AI assistants to interact with the wiki:
- wiki_ingest: Ingest documents into the wiki
- wiki_query: Query the wiki with natural language
- wiki_lint: Check wiki pages for issues
- wiki_graph: Generate the knowledge graph
- wiki_list: List wiki pages
- wiki_stats: Get wiki statistics
- wiki_read: Read a specific wiki page
- wiki_write: Create or update a wiki page
- wiki_search: Search across wiki pages
- wiki_get_insights: Get insights and analysis of the wiki
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from wiki_cli.core.wiki import WikiManager


def _get_manager() -> WikiManager:
    """Get a WikiManager for the current directory."""
    return WikiManager(".")


async def _tool_wiki_ingest(params: dict[str, Any]) -> dict[str, Any]:
    """Ingest a document into the wiki."""
    source = params.get("source", "")
    collection = params.get("collection")

    if not source:
        return {"error": "Missing required parameter: source"}

    try:
        from wiki_cli.core.llm import create_llm_client
        from wiki_cli.core.ingest import IngestEngine

        manager = _get_manager()
        llm = create_llm_client()
        engine = IngestEngine(manager, llm)
        result = engine.ingest(source, collection=collection)
        return {"result": result}
    except FileNotFoundError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Ingest failed: {e}"}


async def _tool_wiki_query(params: dict[str, Any]) -> dict[str, Any]:
    """Query the wiki with natural language."""
    question = params.get("question", "")
    limit = params.get("limit", 10)
    use_llm = params.get("llm", False)

    if not question:
        return {"error": "Missing required parameter: question"}

    manager = _get_manager()
    pages = manager.list_pages()

    if not pages:
        return {"results": [], "message": "Wiki is empty"}

    terms = question.lower().split()
    results = []
    for page in pages:
        page_data = manager.read_page(page["slug"])
        if not page_data:
            continue

        text = (
            page_data.get("content", "").lower()
            + " "
            + page_data.get("frontmatter", {}).get("title", "").lower()
            + " "
            + " ".join(str(t) for t in page_data.get("frontmatter", {}).get("tags", [])).lower()
        )

        score = sum(1 for t in terms if t in text)
        if score > 0:
            results.append({
                "slug": page["slug"],
                "type": page["type"],
                "title": page["title"],
                "score": score,
                "snippet": page_data.get("content", "")[:300],
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    keyword_results = results[:limit]

    if not use_llm:
        return {"results": keyword_results, "total_pages_searched": len(pages)}

    try:
        from wiki_cli.core.llm import create_llm_client

        context_parts = []
        for hit in keyword_results[:5]:
            page_data = manager.read_page(hit["slug"])
            if page_data:
                context_parts.append(
                    f"## {hit['title']} (type: {hit['type']}, slug: {hit['slug']})\n"
                    f"{page_data.get('content', '')[:2000]}"
                )

        context = "\n\n---\n\n".join(context_parts) if context_parts else "(no relevant pages found)"

        prompt = (
            f"You are a wiki assistant. Answer the following question using ONLY the wiki content provided below.\n\n"
            f"Question: {question}\n\n"
            f"Wiki Content:\n{context}\n\n"
            f"Provide a concise answer. If the wiki doesn't contain enough information, say so. "
            f"List which wiki pages are most relevant (by slug)."
        )

        llm = create_llm_client()
        answer = llm.generate(prompt, system="You are a helpful wiki knowledge base assistant.")

        return {
            "results": keyword_results,
            "answer": answer,
            "total_pages_searched": len(pages),
        }
    except Exception as e:
        return {
            "results": keyword_results,
            "llm_error": str(e),
            "total_pages_searched": len(pages),
        }


async def _tool_wiki_lint(params: dict[str, Any]) -> dict[str, Any]:
    """Lint wiki pages for common issues."""
    manager = _get_manager()
    pages = manager.list_pages()

    if not pages:
        return {"issues": [], "message": "No pages to lint"}

    issues = []
    for page in pages:
        path = Path(page["path"])
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError:
            issues.append({"file": str(path), "severity": "error", "code": "E001", "message": "Cannot read file"})
            continue

        if not raw.startswith("---"):
            issues.append({"file": str(path), "line": 1, "severity": "error", "code": "E100", "message": "Missing frontmatter"})
            continue

        fm, content = manager._parse_frontmatter(raw)

        if not fm.get("type"):
            issues.append({"file": str(path), "line": 1, "severity": "error", "code": "E101", "message": "Missing 'type' field"})
        if not fm.get("title"):
            issues.append({"file": str(path), "line": 1, "severity": "warning", "code": "W102", "message": "Missing 'title' field"})

        # Check broken links
        for link_text in re.findall(r"\[\[([^\]]+)\]\]", raw):
            target_slug = manager.slugify(link_text)
            if not manager._find_page(target_slug):
                issues.append({"file": str(path), "severity": "warning", "code": "W300", "message": f"Broken link: [[{link_text}]]"})

    return {"issues": issues, "pages_scanned": len(pages)}


async def _tool_wiki_graph(params: dict[str, Any]) -> dict[str, Any]:
    """Generate a link graph of wiki documents."""
    from wiki_cli.commands.graph_cmd import _build_graph

    manager = _get_manager()
    graph_data = _build_graph(manager)
    return graph_data


async def _tool_wiki_list(params: dict[str, Any]) -> dict[str, Any]:
    """List all wiki pages."""
    page_type = params.get("type")
    manager = _get_manager()
    pages = manager.list_pages(type=page_type)
    return {"pages": pages, "total": len(pages)}


async def _tool_wiki_stats(params: dict[str, Any]) -> dict[str, Any]:
    """Get wiki statistics."""
    manager = _get_manager()
    page_stats = manager.get_stats()

    # Additional computed stats
    pages = manager.list_pages()
    all_tags = set()
    for p in pages:
        page_data = manager.read_page(p["slug"])
        if page_data:
            tags = page_data.get("frontmatter", {}).get("tags", [])
            if isinstance(tags, list):
                all_tags.update(tags)

    return {
        "page_counts": page_stats,
        "unique_tags": len(all_tags),
        "tags": sorted(all_tags),
    }


async def _tool_wiki_read(params: dict[str, Any]) -> dict[str, Any]:
    """Read a specific wiki page by slug."""
    slug = params.get("slug", "")

    if not slug:
        return {"error": "Missing required parameter: slug"}

    manager = _get_manager()
    page_data = manager.read_page(slug)

    if not page_data:
        return {"error": f"Page not found: {slug}"}

    return page_data


async def _tool_wiki_write(params: dict[str, Any]) -> dict[str, Any]:
    """Create or update a wiki page."""
    slug = params.get("slug", "")
    page_type = params.get("type", "entity")
    title = params.get("title", "")
    content = params.get("content", "")

    if not slug:
        return {"error": "Missing required parameter: slug"}
    if not content:
        return {"error": "Missing required parameter: content"}

    tags = params.get("tags", [])
    related = params.get("related", [])

    manager = _get_manager()
    try:
        path = manager.write_page(
            slug=slug,
            page_type=page_type,
            title=title or slug,
            content=content,
            tags=tags,
            related=related,
        )
        return {"status": "written", "path": path, "slug": slug}
    except ValueError as e:
        return {"error": str(e)}


async def _tool_wiki_search(params: dict[str, Any]) -> dict[str, Any]:
    """Search across wiki pages by keyword or regex pattern."""
    pattern = params.get("pattern", "")
    use_regex = params.get("regex", False)
    page_type = params.get("type")

    if not pattern:
        return {"error": "Missing required parameter: pattern"}

    manager = _get_manager()
    pages = manager.list_pages(type=page_type)

    results = []
    for page in pages:
        page_data = manager.read_page(page["slug"])
        if not page_data:
            continue

        content = page_data.get("content", "")
        title = page_data.get("frontmatter", {}).get("title", "")

        matches = []
        if use_regex:
            try:
                for m in re.finditer(pattern, content, re.IGNORECASE):
                    start = max(0, m.start() - 50)
                    end = min(len(content), m.end() + 50)
                    matches.append({
                        "match": m.group(),
                        "context": content[start:end],
                    })
            except re.error as e:
                return {"error": f"Invalid regex: {e}"}
        else:
            text = content.lower()
            search_term = pattern.lower()
            idx = 0
            while True:
                idx = text.find(search_term, idx)
                if idx == -1:
                    break
                start = max(0, idx - 50)
                end = min(len(content), idx + len(search_term) + 50)
                matches.append({
                    "match": content[idx:idx + len(search_term)],
                    "context": content[start:end],
                })
                idx += 1

        if matches:
            results.append({
                "slug": page["slug"],
                "type": page["type"],
                "title": page.get("title", title),
                "match_count": len(matches),
                "matches": matches[:5],  # Limit matches per page
            })

    results.sort(key=lambda x: x["match_count"], reverse=True)
    return {"results": results, "total_matches": sum(r["match_count"] for r in results)}


async def _tool_wiki_get_insights(params: dict[str, Any]) -> dict[str, Any]:
    """Get insights and analysis of the wiki corpus."""
    manager = _get_manager()
    pages = manager.list_pages()

    if not pages:
        return {"insights": [], "message": "Wiki is empty"}

    insights = []

    # 1. Orphan pages (no outgoing or incoming links)
    all_slugs = {p["slug"] for p in pages}
    pages_with_links = set()
    pages_linked_to = set()

    for page in pages:
        page_data = manager.read_page(page["slug"])
        if not page_data:
            continue
        content = page_data.get("content", "")
        links = re.findall(r"\[\[([^\]]+)\]\]", content)
        for link in links:
            target = manager.slugify(link)
            pages_with_links.add(page["slug"])
            if target in all_slugs:
                pages_linked_to.add(target)

    orphan_slugs = all_slugs - pages_linked_to - pages_with_links
    if orphan_slugs:
        insights.append({
            "type": "orphan_pages",
            "severity": "warning",
            "description": f"{len(orphan_slugs)} pages have no incoming or outgoing links",
            "pages": sorted(orphan_slugs),
        })

    # 2. Hub pages (most linked to)
    link_counts = {}
    for page in pages:
        page_data = manager.read_page(page["slug"])
        if not page_data:
            continue
        content = page_data.get("content", "")
        for link in re.findall(r"\[\[([^\]]+)\]\]", content):
            target = manager.slugify(link)
            link_counts[target] = link_counts.get(target, 0) + 1

    if link_counts:
        top_hubs = sorted(link_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        insights.append({
            "type": "hub_pages",
            "severity": "info",
            "description": "Most referenced pages",
            "pages": [{"slug": s, "inbound_links": c} for s, c in top_hubs],
        })

    # 3. Tag analysis
    tag_counts = {}
    for page in pages:
        page_data = manager.read_page(page["slug"])
        if not page_data:
            continue
        tags = page_data.get("frontmatter", {}).get("tags", [])
        if isinstance(tags, list):
            for tag in tags:
                tag_counts[str(tag)] = tag_counts.get(str(tag), 0) + 1

    if tag_counts:
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        insights.append({
            "type": "top_tags",
            "severity": "info",
            "description": "Most common tags",
            "tags": [{"tag": t, "count": c} for t, c in top_tags],
        })

    # 4. Coverage gaps
    type_counts = {}
    for p in pages:
        type_counts[p["type"]] = type_counts.get(p["type"], 0) + 1

    missing_types = set(manager.VALID_TYPES) - {"overview"} - set(type_counts.keys())
    if missing_types:
        insights.append({
            "type": "missing_types",
            "severity": "info",
            "description": f"No pages found for types: {', '.join(sorted(missing_types))}",
            "missing": sorted(missing_types),
        })

    # 5. Short pages
    short_pages = []
    for page in pages:
        page_data = manager.read_page(page["slug"])
        if page_data:
            word_count = len(page_data.get("content", "").split())
            if 0 < word_count < 30:
                short_pages.append({"slug": page["slug"], "words": word_count})

    if short_pages:
        insights.append({
            "type": "short_pages",
            "severity": "warning",
            "description": f"{len(short_pages)} pages have very little content",
            "pages": short_pages,
        })

    return {
        "insights": insights,
        "total_pages": len(pages),
        "total_types": len(type_counts),
    }


async def _tool_wiki_update_page(params: dict[str, Any]) -> dict[str, Any]:
    """Incrementally update an existing wiki page."""
    slug = params.get("slug", "")
    if not slug:
        return {"error": "Missing required parameter: slug"}

    manager = _get_manager()
    page_data = manager.read_page(slug)
    if not page_data:
        return {"error": f"Page not found: {slug}"}

    fm_updates = {}
    if "tags" in params:
        fm_updates["tags"] = params["tags"]
    if "related" in params:
        fm_updates["related"] = params["related"]
    if "title" in params:
        fm_updates["title"] = params["title"]
    if "sources" in params:
        fm_updates["sources"] = params["sources"]

    content = params.get("content")

    path = manager.update_page(slug, content=content, **fm_updates)
    if path:
        return {"status": "updated", "slug": slug, "path": path}
    return {"error": f"Failed to update page: {slug}"}


async def _tool_wiki_delete_page(params: dict[str, Any]) -> dict[str, Any]:
    """Delete a wiki page by slug."""
    slug = params.get("slug", "")
    if not slug:
        return {"error": "Missing required parameter: slug"}

    manager = _get_manager()
    deleted = manager.delete_page(slug)
    if deleted:
        manager.update_index()
        return {"status": "deleted", "slug": slug}
    return {"error": f"Page not found: {slug}"}


async def _tool_wiki_move_page(params: dict[str, Any]) -> dict[str, Any]:
    """Rename a wiki page (change its slug)."""
    old_slug = params.get("old_slug", "")
    new_slug = params.get("new_slug", "")
    if not old_slug or not new_slug:
        return {"error": "Missing required parameters: old_slug and new_slug"}

    manager = _get_manager()
    new_path = manager.move_page(old_slug, new_slug)
    if new_path:
        manager.update_index()
        return {"status": "moved", "old_slug": old_slug, "new_slug": new_slug, "path": new_path}
    return {"error": f"Page not found: {old_slug}"}


async def _tool_wiki_setup(params: dict[str, Any]) -> dict[str, Any]:
    """Guided setup for creating or updating a wiki knowledge base.

    This tool provides a structured interview flow for agents.
    Returns a list of questions to ask the user, then based on
    the answers, creates or updates the wiki.

    Steps:
    1. If action="questions", returns the list of setup questions
    2. If action="create", uses provided answers to create the wiki
    3. If action="status", returns current wiki status
    """
    action = params.get("action", "questions")

    if action == "questions":
        return {
            "step": "questions",
            "questions": [
                {
                    "id": "action_type",
                    "question": "What would you like to do?",
                    "options": [
                        {"value": "create", "label": "Create a new wiki knowledge base"},
                        {"value": "update", "label": "Add documents to an existing wiki"},
                        {"value": "status", "label": "Check current wiki status"},
                    ],
                    "required": True,
                },
                {
                    "id": "wiki_path",
                    "question": "Where should the wiki be stored? (absolute or relative path)",
                    "default": "./my-wiki",
                    "required": True,
                    "when": "action_type=create",
                },
                {
                    "id": "template",
                    "question": "What type of wiki do you want?",
                    "options": [
                        {"value": "research", "label": "Research — papers, academic knowledge"},
                        {"value": "reading", "label": "Reading — books, articles, notes"},
                        {"value": "personal", "label": "Personal — goals, habits, reflections"},
                        {"value": "business", "label": "Business — meetings, decisions, projects"},
                        {"value": "general", "label": "General — flexible, no specific theme"},
                    ],
                    "default": "research",
                    "required": True,
                    "when": "action_type=create",
                },
                {
                    "id": "name",
                    "question": "What is the name of your wiki project?",
                    "default": "My Wiki",
                    "required": True,
                    "when": "action_type=create",
                },
                {
                    "id": "description",
                    "question": "Briefly describe what this wiki covers (optional)",
                    "default": "",
                    "when": "action_type=create",
                },
                {
                    "id": "source_path",
                    "question": "Path to the document or directory to ingest",
                    "when": "action_type=update",
                },
            ],
        }

    if action == "status":
        wiki_path = params.get("wiki_path", ".")
        manager = WikiManager(wiki_path)
        if not (manager.project_path / ".llm-wiki" / "project.json").exists():
            return {"status": "not_initialized", "path": str(manager.project_path)}
        stats = manager.get_stats()
        pages = manager.list_pages()
        proj_file = manager.project_path / ".llm-wiki" / "project.json"
        proj_data = {}
        try:
            proj_data = json.loads(proj_file.read_text(encoding="utf-8"))
        except Exception:
            pass
        return {
            "status": "initialized",
            "path": str(manager.project_path),
            "name": proj_data.get("name", ""),
            "project_id": proj_data.get("id", ""),
            "page_counts": stats,
            "total_pages": len(pages),
        }

    if action == "create":
        wiki_path = params.get("wiki_path", "./my-wiki")
        template = params.get("template", "research")
        name = params.get("name", "My Wiki")
        description = params.get("description", "")

        path = Path(wiki_path).resolve()
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        manager = WikiManager(str(path))
        result = manager.init_wiki(template=template)

        proj_file = path / ".llm-wiki" / "project.json"
        if proj_file.exists():
            proj_data = json.loads(proj_file.read_text(encoding="utf-8"))
            proj_data["name"] = name
            if description:
                proj_data["description"] = description
            proj_file.write_text(json.dumps(proj_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        if description:
            purpose_file = path / "purpose.md"
            if purpose_file.exists():
                raw = purpose_file.read_text(encoding="utf-8")
                raw = raw.rstrip() + f"\n\n**Project Name:** {name}\n**Description:** {description}\n"
                purpose_file.write_text(raw, encoding="utf-8")

        return {
            "status": "created",
            "project_id": result["project_id"],
            "path": str(path),
            "template": template,
            "name": name,
            "created_items": result["created"],
            "next_steps": [
                "Use wiki_ingest to add documents",
                "Use wiki_query to search the wiki",
                "Use wiki_lint to check for issues",
            ],
        }

    return {"error": f"Unknown action: {action}. Use 'questions', 'create', or 'status'."}


# ── MCP Server Entry Point ────────────────────────────────────────────

# Tool definitions for MCP
TOOLS = [
    {
        "name": "wiki_ingest",
        "description": "Ingest a source document into the wiki. Runs a 2-step LLM pipeline: Step 1 analyzes the document, Step 2 generates entity/concept/source pages with correct frontmatter, then updates index and overview. IMPORTANT: Always prefer this over manually creating pages — it ensures correct frontmatter format and cross-references.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Path to the source file or directory"},
                "collection": {"type": "string", "description": "Optional collection/category label"},
            },
            "required": ["source"],
        },
    },
    {
        "name": "wiki_query",
        "description": "Query the wiki with a natural language question. Returns matching pages ranked by relevance. Optionally uses LLM to synthesize an answer.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "Natural language question"},
                "limit": {"type": "integer", "description": "Max results (default 10)"},
                "llm": {"type": "boolean", "description": "Use LLM to synthesize an answer from relevant pages (default false)"},
            },
            "required": ["question"],
        },
    },
    {
        "name": "wiki_lint",
        "description": "Lint wiki pages for common issues like missing frontmatter, broken links, etc.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "wiki_graph",
        "description": "Generate a knowledge graph showing links between wiki pages.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "wiki_list",
        "description": "List all wiki pages, optionally filtered by type.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": "Page type filter (entity, concept, source, query, comparison, synthesis)",
                },
            },
        },
    },
    {
        "name": "wiki_stats",
        "description": "Get statistics about the wiki corpus including page counts, tags, and type distribution.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "wiki_read",
        "description": "Read a specific wiki page by its slug. Returns frontmatter and content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Page slug identifier"},
            },
            "required": ["slug"],
        },
    },
    {
        "name": "wiki_write",
        "description": "Create or overwrite a wiki page. Frontmatter (type, title, created, updated, tags, related, sources) is generated AUTOMATICALLY in the correct format — do NOT include frontmatter in the content parameter. Use wiki_update_page instead if you want to merge tags/related without overwriting.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Page slug identifier (kebab-case, e.g. 'gpt-4o', 'safety-alignment')"},
                "type": {"type": "string", "description": "Page type (entity, concept, source, query, comparison, synthesis)"},
                "title": {"type": "string", "description": "Human-readable page title"},
                "content": {"type": "string", "description": "Page body content in markdown (WITHOUT frontmatter — it is auto-generated)"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "List of tags"},
                "related": {"type": "array", "items": {"type": "string"}, "description": "List of related page slugs"},
            },
            "required": ["slug", "content"],
        },
    },
    {
        "name": "wiki_search",
        "description": "Search wiki pages by keyword or regex pattern. Returns matching contexts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Search term or regex pattern"},
                "regex": {"type": "boolean", "description": "Whether to use regex matching (default false)"},
                "type": {"type": "string", "description": "Optional page type filter"},
            },
            "required": ["pattern"],
        },
    },
    {
        "name": "wiki_get_insights",
        "description": "Get analytical insights about the wiki: orphan pages, hub pages, coverage gaps, tag analysis, etc.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "wiki_update_page",
        "description": "Incrementally update an existing wiki page. List fields (tags, related, sources) are MERGED (union) — existing values are preserved and new ones added. Scalar fields (title) are overwritten. Only provided fields are changed. Frontmatter is regenerated automatically in the correct format. Prefer this over wiki_write for updating existing pages.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Page slug identifier"},
                "content": {"type": "string", "description": "New page content in markdown (optional, omit to keep existing)"},
                "title": {"type": "string", "description": "New title (optional)"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags to add (merged with existing)"},
                "related": {"type": "array", "items": {"type": "string"}, "description": "Related page slugs to add (merged with existing)"},
                "sources": {"type": "array", "items": {"type": "string"}, "description": "Sources to add (merged with existing)"},
            },
            "required": ["slug"],
        },
    },
    {
        "name": "wiki_delete_page",
        "description": "Delete a wiki page by slug. Also updates the index.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Page slug to delete"},
            },
            "required": ["slug"],
        },
    },
    {
        "name": "wiki_move_page",
        "description": "Rename a wiki page (change its slug). Also updates the index.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "old_slug": {"type": "string", "description": "Current slug of the page"},
                "new_slug": {"type": "string", "description": "New slug for the page"},
            },
            "required": ["old_slug", "new_slug"],
        },
    },
    {
        "name": "wiki_setup",
        "description": "Guided setup wizard for creating or managing wiki knowledge bases. START HERE for new users. Action flow: (1) action='questions' → returns structured questions to ask the user, (2) action='create' → creates wiki with user's answers, (3) action='status' → checks existing wiki status. Agents should first call with action='questions', present options to user, then call with action='create' using collected answers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "One of: 'questions' (get setup questions), 'create' (create wiki), 'status' (check existing wiki)",
                    "enum": ["questions", "create", "status"],
                },
                "wiki_path": {"type": "string", "description": "Path for wiki storage (used with create/status)"},
                "template": {"type": "string", "description": "Wiki template: research, reading, personal, business, general"},
                "name": {"type": "string", "description": "Project name"},
                "description": {"type": "string", "description": "Brief project description"},
            },
            "required": ["action"],
        },
    },
]

# Tool handler map
TOOL_HANDLERS = {
    "wiki_ingest": _tool_wiki_ingest,
    "wiki_query": _tool_wiki_query,
    "wiki_lint": _tool_wiki_lint,
    "wiki_graph": _tool_wiki_graph,
    "wiki_list": _tool_wiki_list,
    "wiki_stats": _tool_wiki_stats,
    "wiki_read": _tool_wiki_read,
    "wiki_write": _tool_wiki_write,
    "wiki_search": _tool_wiki_search,
    "wiki_get_insights": _tool_wiki_get_insights,
    "wiki_update_page": _tool_wiki_update_page,
    "wiki_delete_page": _tool_wiki_delete_page,
    "wiki_move_page": _tool_wiki_move_page,
    "wiki_setup": _tool_wiki_setup,
}


def run_mcp() -> None:
    """Start the MCP server using stdio transport."""
    # Auto-load .env from the wiki project directory so MINIMAX_CN_API_KEY
    # and other secrets are available without explicit env var passing.
    _wiki_env = os.environ.get("WIKI_ENV_PATH")
    if _wiki_env and Path(_wiki_env).exists():
        load_dotenv(_wiki_env)
    else:
        # Fall back to .env in the wiki root (cwd at startup)
        load_dotenv(Path.cwd() / ".env", override=False)

    try:
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        import mcp.types as types
        import asyncio
    except ImportError:
        print(
            "Error: MCP dependencies not installed.\n"
            "Install with: pip install wiki-cli[mcp]",
            file=sys.stderr,
        )
        sys.exit(1)

    server = Server("wiki-cli")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name=t["name"],
                description=t["description"],
                inputSchema=t["inputSchema"],
            )
            for t in TOOLS
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        handler = TOOL_HANDLERS.get(name)
        if not handler:
            return [types.TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

        try:
            result = await handler(arguments)
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        except Exception as e:
            return [types.TextContent(type="text", text=json.dumps({"error": str(e)}))]

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(main())
