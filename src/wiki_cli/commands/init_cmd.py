"""`wiki init` — Initialize a new wiki project."""

import json
import sys
from pathlib import Path

import click

from wiki_cli.core.wiki import WikiManager


def init(template: str = "research", name: str | None = None, project_path: str = ".") -> None:
    """Initialize a new wiki project in the target directory."""
    path = Path(project_path).resolve()

    if not path.exists():
        click.echo(f"Creating directory: {path}")
        path.mkdir(parents=True, exist_ok=True)

    # Check if already initialized
    llm_dir = path / ".llm-wiki"
    if llm_dir.exists() and (llm_dir / "project.json").exists():
        click.echo(f"⚠  Wiki already initialized at {path}")
        if not click.confirm("Re-initialize? This will NOT overwrite existing pages."):
            click.echo("Aborted.")
            sys.exit(0)

    manager = WikiManager(str(path))
    result = manager.init_wiki(template=template)

    # If a name was provided, update project.json and purpose.md
    if name:
        proj_file = path / ".llm-wiki" / "project.json"
        proj_data = json.loads(proj_file.read_text(encoding="utf-8"))
        proj_data["name"] = name
        proj_file.write_text(json.dumps(proj_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        purpose_file = path / "purpose.md"
        if purpose_file.exists():
            raw = purpose_file.read_text(encoding="utf-8")
            if "project_name" not in raw:
                raw = raw.rstrip() + f"\n\n**Project Name:** {name}\n"
                purpose_file.write_text(raw, encoding="utf-8")

    click.echo(f"✅ Wiki initialized (template={template})")
    click.echo(f"   Project ID: {result['project_id']}")
    click.echo(f"   Created {len(result['created'])} items:")
    for item in result["created"]:
        click.echo(f"     • {item}")
    if name:
        click.echo(f"   Project name: {name}")
    click.echo(f"\nNext steps:")
    click.echo(f"  cd {path}")
    click.echo(f"  wiki ingest <file>         # Add documents")
    click.echo(f"  wiki query <question>      # Search the wiki")
