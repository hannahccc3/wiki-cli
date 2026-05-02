"""`wiki serve` — Simple HTTP server to browse the wiki."""

import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import click

from wiki_cli.core.wiki import WikiManager


class WikiHTTPHandler(SimpleHTTPRequestHandler):
    """HTTP handler for browsing the wiki."""

    def do_GET(self):
        manager = WikiManager(".")
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/" or path == "/index":
            self._serve_index(manager)
        elif path == "/api/pages":
            self._serve_api_pages(manager, query)
        elif path == "/api/stats":
            self._serve_api_stats(manager)
        elif path == "/api/graph":
            self._serve_api_graph(manager)
        elif path.startswith("/api/page/"):
            slug = path[len("/api/page/"):]
            self._serve_api_page(manager, slug)
        elif path.startswith("/page/"):
            slug = path[len("/page/"):]
            self._serve_page(manager, slug)
        elif path.startswith("/static/"):
            self._serve_static(path)
        else:
            self.send_error(404, "Not Found")

    def _html_header(self, title: str = "Wiki") -> str:
        return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>{title} — Wiki CLI</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       max-width: 900px; margin: 40px auto; padding: 0 20px; color: #333; }}
h1 {{ border-bottom: 2px solid #4a9eff; padding-bottom: 10px; }}
a {{ color: #4a9eff; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.page-type {{ display: inline-block; padding: 2px 8px; border-radius: 4px;
              font-size: 0.8em; margin-right: 8px; }}
.type-entity {{ background: #e3f2fd; }}
.type-concept {{ background: #f3e5f5; }}
.type-source {{ background: #e8f5e9; }}
.type-query {{ background: #fff3e0; }}
.type-comparison {{ background: #fce4ec; }}
.type-synthesis {{ background: #e0f7fa; }}
pre {{ background: #f5f5f5; padding: 16px; border-radius: 4px; overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #4a9eff; color: white; }}
tr:nth-child(even) {{ background: #f9f9f9; }}
nav {{ margin-bottom: 20px; padding: 10px; background: #f5f5f5; border-radius: 4px; }}
nav a {{ margin-right: 16px; }}
</style>
</head><body>"""

    def _html_footer(self) -> str:
        return "<hr><footer><small>Powered by wiki-cli</small></footer></body></html>"

    def _serve_index(self, manager: WikiManager):
        pages = manager.list_pages()
        stats = manager.get_stats()

        html = self._html_header("Index")
        html += "<h1>📚 Wiki Index</h1>"
        html += "<nav><a href='/'>Index</a> <a href='/api/stats'>Stats</a> <a href='/api/graph'>Graph</a></nav>"
        html += f"<p>Total: <strong>{stats.get('total', 0)}</strong> pages</p>"

        for ptype in ["source", "entity", "concept", "query", "comparison", "synthesis"]:
            type_pages = [p for p in pages if p["type"] == ptype]
            if not type_pages:
                continue
            html += f"<h2>{ptype.title()}s ({len(type_pages)})</h2><ul>"
            for p in type_pages:
                html += f"<li><span class='page-type type-{p['type']}'>{p['type']}</span>"
                html += f"<a href='/page/{p['slug']}'>{p['title']}</a></li>"
            html += "</ul>"

        html += self._html_footer()
        self._respond_html(html)

    def _serve_page(self, manager: WikiManager, slug: str):
        page_data = manager.read_page(slug)
        if not page_data:
            self.send_error(404, f"Page not found: {slug}")
            return

        fm = page_data["frontmatter"]
        content = page_data["content"]
        title = fm.get("title", slug)

        # Simple markdown-to-html (basic)
        import re
        html_content = content
        html_content = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html_content)
        html_content = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html_content)
        html_content = re.sub(r"`(.+?)`", r"<code>\1</code>", html_content)
        html_content = re.sub(
            r"\[\[([^\]]+)\]\]",
            r"<a href='/page/\1'>\1</a>",
            html_content,
        )
        html_content = html_content.replace("\n\n", "</p><p>")
        html_content = f"<p>{html_content}</p>"

        html = self._html_header(title)
        html += f"<nav><a href='/'>← Index</a></nav>"
        html += f"<h1>{title}</h1>"
        html += f"<p><span class='page-type type-{fm.get('type', 'entity')}'>{fm.get('type', '?')}</span>"
        tags = fm.get("tags", [])
        if isinstance(tags, list) and tags:
            html += f" Tags: {', '.join(str(t) for t in tags)}"
        html += "</p>"
        html += html_content
        html += self._html_footer()
        self._respond_html(html)

    def _serve_api_pages(self, manager: WikiManager, query_params: dict):
        page_type = query_params.get("type", [None])[0]
        pages = manager.list_pages(type=page_type)
        self._respond_json(pages)

    def _serve_api_page(self, manager: WikiManager, slug: str):
        page_data = manager.read_page(slug)
        if not page_data:
            self.send_error(404, f"Page not found: {slug}")
            return
        self._respond_json(page_data)

    def _serve_api_stats(self, manager: WikiManager):
        stats = manager.get_stats()
        self._respond_json(stats)

    def _serve_api_graph(self, manager: WikiManager):
        from wiki_cli.commands.graph_cmd import _build_graph
        graph_data = _build_graph(manager)
        self._respond_json(graph_data)

    def _serve_static(self, path: str):
        # Basic static file serving
        static_dir = Path(".") / "wiki" / "media"
        file_path = static_dir / path.lstrip("/static/")
        if file_path.exists() and file_path.is_file():
            self.send_response(200)
            if file_path.suffix == ".css":
                self.send_header("Content-Type", "text/css")
            elif file_path.suffix == ".js":
                self.send_header("Content-Type", "application/javascript")
            else:
                self.send_header("Content-Type", "application/octet-stream")
            self.end_headers()
            self.wfile.write(file_path.read_bytes())
        else:
            self.send_error(404, "Static file not found")

    def _respond_html(self, html: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _respond_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress default logging for cleaner output
        pass


def serve(host: str, port: int) -> None:
    """Start a local HTTP server to browse the wiki.

    Provides a web interface at http://host:port with page browsing,
    search, and a JSON API.
    """
    manager = WikiManager(".")
    if not (manager.project_path / "wiki").exists():
        click.echo("⚠  No wiki found. Run `wiki init` first.")
        sys.exit(1)

    pages = manager.list_pages()
    click.echo(f"🌐 Starting wiki server at http://{host}:{port}")
    click.echo(f"   Serving {len(pages)} pages")
    click.echo(f"   Press Ctrl+C to stop\n")

    try:
        server = HTTPServer((host, port), WikiHTTPHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        click.echo("\n🛑 Server stopped.")
