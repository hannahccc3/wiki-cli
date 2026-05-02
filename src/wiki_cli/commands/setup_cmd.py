"""`wiki setup` — Interactive setup wizard for wiki knowledge base."""

import json
import sys
from pathlib import Path

import click

from wiki_cli.core.wiki import WikiManager


TEMPLATES = {
    "research": {
        "label": "Research (学术研究)",
        "desc": "论文、研究报告、学术知识库",
    },
    "reading": {
        "label": "Reading (阅读笔记)",
        "desc": "书籍、文章、个人阅读笔记",
    },
    "personal": {
        "label": "Personal (个人成长)",
        "desc": "目标追踪、习惯养成、个人反思",
    },
    "business": {
        "label": "Business (商业/团队)",
        "desc": "会议记录、决策文档、项目追踪",
    },
    "general": {
        "label": "General (通用)",
        "desc": "通用知识库，无特定主题限制",
    },
}


def setup_wizard() -> None:
    click.echo("╔══════════════════════════════════════════════════════╗")
    click.echo("║        Wiki Knowledge Base Setup Wizard              ║")
    click.echo("║        Wiki 知识库构建向导                            ║")
    click.echo("╚══════════════════════════════════════════════════════╝")
    click.echo()

    existing = _find_existing_wikis()
    if existing:
        click.echo("📋 检测到已有的 wiki 知识库：")
        for i, p in enumerate(existing, 1):
            proj = p / ".llm-wiki" / "project.json"
            proj_name = ""
            if proj.exists():
                try:
                    proj_name = json.loads(proj.read_text()).get("name", "")
                except Exception:
                    pass
            label = f" ({proj_name})" if proj_name else ""
            click.echo(f"  {i}. {p}{label}")
        click.echo(f"  0. 创建新的知识库")
        click.echo()

        choice = click.prompt("请选择", type=int, default=0)
        if 1 <= choice <= len(existing):
            selected = existing[choice - 1]
            click.echo(f"\n📂 已选择: {selected}")
            _manage_existing(str(selected))
            return

    click.echo("🆕 创建新的 Wiki 知识库")
    click.echo("─" * 50)

    wiki_path = _ask_path()
    template = _ask_template()
    name = _ask_name(template)
    description = _ask_description()

    click.echo()
    click.echo("━" * 50)
    click.echo("📝 确认信息：")
    click.echo(f"   存放路径: {wiki_path}")
    click.echo(f"   模板类型: {TEMPLATES[template]['label']}")
    click.echo(f"   项目名称: {name}")
    if description:
        click.echo(f"   项目描述: {description[:60]}")
    click.echo()

    if not click.confirm("确认创建？", default=True):
        click.echo("已取消。")
        return

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

    click.echo()
    click.echo(f"✅ Wiki 知识库创建成功！")
    click.echo(f"   Project ID: {result['project_id']}")
    click.echo(f"   创建了 {len(result['created'])} 个文件/目录")
    click.echo()
    click.echo("🚀 下一步：")
    click.echo(f"   cd {path}")
    click.echo(f"   wiki ingest <文件路径>        # 导入文档")
    click.echo(f"   wiki ingest-batch <目录>      # 批量导入")
    click.echo(f"   wiki query <问题>             # 查询知识库")


def _ask_path() -> str:
    click.echo()
    click.echo("📂 第 1 步：选择知识库存放路径")
    click.echo("   知识库将在此目录下创建 wiki/、raw/、schema.md 等文件结构")
    default_path = str(Path.cwd() / "my-wiki")
    path = click.prompt("   存放路径", default=default_path)
    resolved = Path(path).resolve()
    if resolved.exists() and (resolved / ".llm-wiki" / "project.json").exists():
        click.echo(f"   ⚠  检测到 {path} 已有 wiki 项目")
        if not click.confirm("   是否覆盖？（不会删除已有页面）", default=False):
            return _ask_path()
    return path


def _ask_template() -> str:
    click.echo()
    click.echo("📋 第 2 步：选择知识库模板")
    click.echo("   不同模板提供不同的页面类型和目录结构")
    click.echo()
    keys = list(TEMPLATES.keys())
    for i, key in enumerate(keys, 1):
        t = TEMPLATES[key]
        click.echo(f"   {i}. {t['label']}")
        click.echo(f"      {t['desc']}")
    click.echo()

    choice = click.prompt("   请选择模板", type=int, default=1)
    if 1 <= choice <= len(keys):
        selected = keys[choice - 1]
        click.echo(f"   ✅ 已选择: {TEMPLATES[selected]['label']}")
        return selected
    click.echo("   ⚠  无效选择，默认使用 research")
    return "research"


def _ask_name(template: str) -> str:
    click.echo()
    click.echo("📝 第 3 步：为知识库命名")
    click.echo("   这个名称会出现在 project.json 和 purpose.md 中")
    default_names = {
        "research": "My Research Wiki",
        "reading": "My Reading Notes",
        "personal": "My Personal Wiki",
        "business": "Team Knowledge Base",
        "general": "My Wiki",
    }
    default = default_names.get(template, "My Wiki")
    name = click.prompt("   项目名称", default=default)
    return name


def _ask_description() -> str:
    click.echo()
    click.echo("📝 第 4 步：简要描述知识库的用途（可选）")
    click.echo("   描述会写入 purpose.md，帮助 LLM 更好地理解知识库的上下文")
    description = click.prompt("   项目描述（留空跳过）", default="")
    return description.strip()


def _find_existing_wikis() -> list[Path]:
    found = []
    search_dirs = [
        Path.cwd(),
        Path.home() / "Documents",
        Path.home() / "Documents" / "Wiki",
    ]
    for base in search_dirs:
        if not base.exists():
            continue
        if (base / ".llm-wiki" / "project.json").exists():
            found.append(base)
        for child in base.iterdir():
            if child.is_dir() and (child / ".llm-wiki" / "project.json").exists():
                if child not in found:
                    found.append(child)
    return found[:10]


def _manage_existing(wiki_path: str) -> None:
    manager = WikiManager(wiki_path)
    stats = manager.get_stats()

    click.echo()
    click.echo("📊 知识库当前状态：")
    click.echo(f"   总页面数: {stats.get('total', 0)}")
    for ptype in ["source", "entity", "concept", "query", "comparison", "synthesis"]:
        count = stats.get(ptype, 0)
        if count > 0:
            click.echo(f"   {ptype}: {count}")
    click.echo()

    click.echo("可执行的操作：")
    click.echo("  1. 导入新文档 (ingest)")
    click.echo("  2. 批量导入 (ingest-batch)")
    click.echo("  3. 更新索引 (index --update)")
    click.echo("  4. 健康检查 (lint)")
    click.echo("  0. 退出")
    click.echo()

    choice = click.prompt("请选择操作", type=int, default=0)
    if choice == 1:
        _wizard_ingest(manager)
    elif choice == 2:
        _wizard_ingest_batch(manager)
    elif choice == 3:
        manager.update_index()
        manager.update_overview()
        click.echo("✅ 索引和概览已更新")
    elif choice == 4:
        from wiki_cli.commands.lint_cmd import lint as _lint
        _lint(fix=False, severity="info", output_format="text")


def _wizard_ingest(manager: WikiManager) -> None:
    click.echo()
    file_path = click.prompt("   请输入文件路径")
    if not Path(file_path).exists():
        click.echo(f"   ❌ 文件不存在: {file_path}")
        return
    collection = click.prompt("   集合标签（留空跳过）", default="")
    force = click.confirm("   强制重新导入？", default=False)

    from wiki_cli.core.llm import create_llm_client
    from wiki_cli.core.ingest import IngestEngine
    try:
        llm = create_llm_client()
        engine = IngestEngine(manager, llm)
        result = engine.ingest(file_path, collection=collection or None)
        if result["status"] == "cached":
            click.echo(f"   ⏭  已缓存，跳过")
        else:
            click.echo(f"   ✅ 导入成功，生成了 {len(result['output_paths'])} 个页面")
    except Exception as e:
        click.echo(f"   ❌ 导入失败: {e}")


def _wizard_ingest_batch(manager: WikiManager) -> None:
    click.echo()
    dir_path = click.prompt("   请输入目录路径")
    if not Path(dir_path).exists():
        click.echo(f"   ❌ 目录不存在: {dir_path}")
        return
    recursive = click.confirm("   递归扫描子目录？", default=False)
    md_only = click.confirm("   仅导入 .md 文件？", default=False)

    from wiki_cli.commands.ingest import ingest_batch as _ingest_batch
    _ingest_batch(
        directory=dir_path, recursive=recursive, md_only=md_only,
        collection=None, force=False,
    )
