# wiki-cli

> Agent 驱动的本地知识库管理工具（基于 [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) 重构）

`wiki-cli` 源自 [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)，但在功能、架构和 Agent 集成方面都有显著增强。它是一个命令行工具，让 AI Agent 能够像人类一样构建和管理结构化的本地知识库（Wiki）。

## ✨ 功能亮点

- 📄 **两步思维链摄入** — LLM 先分析文档再生成 Wiki 页面，来源可追溯，支持增量缓存
- 🖼️ **多模态图片摄入** — 自动提取 PDF 内嵌图片，调用视觉模型（Ollama minicpm-v / llava）生成事实性描述
- 🔗 **四信号知识图谱** — 直接链接、来源重叠、Adamic-Adar、类型亲和度四维关联度模型
- 🔮 **Louvain 社区检测** — 自动发现知识聚类，计算内聚度
- 💡 **图谱洞察** — 惊奇连接与知识空白检测，自动生成 Deep Research 建议
- 🔢 **向量语义搜索** — 基于 Ollama 本地 Embedding 模型 + LanceDB，支持任意 OpenAI 兼容端点
- 📋 **持久化摄入队列** — 串行处理，崩溃恢复，取消/重试，进度可视化
- 📂 **文件夹导入** — 递归导入保留目录结构，文件夹路径作为 LLM 分类上下文
- 🔬 **深度研究** — LLM 智能生成搜索主题，DuckDuckGo 网络搜索，研究结果自动摄入 Wiki
- 🔍 **异步审核系统** — LLM 在摄入时标记低置信度/歧义实体，预生成搜索查询，预定义操作
- 🤖 **16 个 LLM Provider** — OpenAI / Anthropic / Google Gemini / DeepSeek / Groq / xAI / Kimi / 智谱 / MiniMax / 阿里百炼 / 火山引擎 / 小米 MiMo / Ollama / 自定义
- 🧙 **交互向导** — `wiki setup` 引导式创建知识库，人类和 Agent 都能用
- 📂 **Obsidian 兼容** — 自动生成 `.obsidian/` 配置，支持图谱视图和反向链接

---

## 🌟 与 nashsu/llm_wiki 的区别

`wiki-cli` 是从 [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) fork 并大幅重构的项目，保留了原有的核心摄入管线（两步思维链、多模态图片处理、四信号知识图谱），但进行了以下核心增强：

### 1. Agent-First 设计（核心差异）

| 特性 | llm_wiki | wiki-cli |
|------|----------|----------|
| **Agent 接入方式** | 主要通过 Web 界面 | **CLI + MCP 双轨接入**，14 个 MCP 工具即插即用 |
| **Agent 指导文档** | 分散在各处 | **独立的 `SKILLS.md`**（按场景指导）+ **独立的 `AGENTS.md`**（操作规范），Agent 克隆后直接读文档 |
| **交互向导** | 无 | **`wiki setup` 交互向导**，支持 `MCP wiki_setup` 工具，Agent 可向用户提问获取配置 |

**示例场景**：当用户说"帮我建一个知识库"时，Agent 可以：
1. 调用 `wiki_setup(action="questions")` 获取需要收集的信息
2. 向用户提问：知识库名称、路径、模板类型
3. 用户回答后，调用 `wiki_setup(action="create", ...)` 完成创建

### 2. 新增功能模块

| 模块 | 说明 | llm_wiki |
|------|------|----------|
| **Deep Research** | LLM 生成搜索主题 → DuckDuckGo 搜索 → 内容摄入，形成完整研究闭环 | ❌ 无 |
| **Review 审核系统** | 摄入时自动标记低置信度内容，支持 approve/reject/merge/verify 操作 | ❌ 无 |
| **Embedding 向量搜索** | Ollama 本地 embedding + LanceDB，混合搜索效果更好 | ❌ 无 |
| **持久化摄入队列** | 队列持久化到 JSON，崩溃后自动恢复，支持取消/重试 | ❌ 无（仅内存队列） |
| **Setup 向导** | 交互式创建知识库，人类和 Agent 都可用 | ❌ 无 |

### 3. 更完善的 Provider 支持

| Provider 数量 | llm_wiki | wiki-cli |
|--------------|----------|----------|
| LLM Provider | 约 5-6 个 | **16 个**（含 MiniMax、智谱、火山引擎、小米等国产 Provider） |
| Embedding | 仅 OpenAI | **Ollama 本地 + 任意 OpenAI 兼容端点** |

### 4. 专为 Agent 优化的工程细节

- **Frontmatter 顺序规范**：严格按 `type → title → created/updated → tags → related → sources` 排列，LLM 生成时不会混淆
- **Source 页面额外字段**：自动提取 `authors`、`year`、`url`、`venue`，便于溯源
- **增量缓存**：基于文件 hash 的增量摄入，大型知识库无需全量重建
- **远程操作**：`wiki --path <path>` 支持同时管理多个知识库

### 5. 配套的 Agent Skill

`wiki-cli` 附带完整的 Agent 使用指南，存放在项目内：

```
src/wiki_cli/references/
├── AGENTS.md              # Agent 操作规范（绝对禁止项、命名规则、工作流）
└── research_schema.md     # 页面结构规范（7 种页面类型、frontmatter 格式示例）
```

Agent 克隆项目后，只需要：
1. 读 `SKILLS.md` 了解功能
2. 读 `AGENTS.md` 了解规则
3. 直接开始工作

---

---

## 👤 人类使用指南

### 第 1 步：克隆并安装

```bash
git clone https://github.com/hannahccc3/wiki-cli.git /tmp/wiki-cli
cd /tmp/wiki-cli && pip install -e . && pip install -e ".[mcp]"
wiki --help
```

### 第 2 步：配置 API Key

在 wiki 项目目录下创建 `.env` 文件：

```bash
# MiniMax（默认）
echo 'MINIMAX_CN_API_KEY=your-key-here' > .env

# 或 OpenAI 兼容接口
echo 'OPENAI_API_KEY=your-key-here' > .env

# 或切换到其他 provider（通过环境变量）
export WIKI_CLI_LLM_PROVIDER=deepseek
export WIKI_CLI_LLM_API_KEY=your-key-here
```

### 第 3 步：创建知识库

```bash
# 交互式向导（推荐新手）
wiki setup

# 或命令行一步到位
wiki init --template research --name "我的 NLP 研究" --path ~/Documents/my-wiki
```

### 第 4 步：导入文档

```bash
wiki ingest ~/Downloads/paper.pdf
wiki ingest-batch ~/Documents/papers/ --recursive
```

### 第 5 步：建立向量索引（可选，需要 Ollama）

```bash
# 确保 Ollama 已安装，然后拉取 embedding 模型
ollama pull qwen3-embedding:8b

# 在 wiki-cli.yaml 中启用
echo 'embeddings:
  enabled: true
  model: qwen3-embedding:8b' > wiki-cli.yaml

# 建立索引
wiki embed --all
```

### 第 6 步：查询和管理

```bash
wiki query "什么是 Chain-of-Thought？"     # 混合搜索（关键词 + 向量）
wiki list                                  # 列出所有页面
wiki stats                                 # 查看统计
wiki lint                                  # 健康检查
wiki graph --output graph.json             # 知识图谱
wiki research "最新的大模型安全研究进展"     # 深度研究
wiki review --list                         # 查看待审核项
```

### 远程操作

```bash
wiki --path ~/Documents/my-wiki list
wiki --path ~/Documents/my-wiki ingest paper.pdf
wiki --path ~/Documents/my-wiki query "注意力机制"
```

### 浏览知识库

```bash
wiki serve --port 8080                     # Web 界面
# 或用 Obsidian 打开知识库目录（自动生成 .obsidian/ 配置）
```

---

## 🤖 Agent 使用指南

### 第 1 步：安装 wiki-cli

```bash
git clone https://github.com/hannahccc3/wiki-cli.git /tmp/wiki-cli
cd /tmp/wiki-cli && pip install -e . && pip install -e ".[mcp]"
wiki --help
```

> 📖 **安装后请先阅读 [`SKILLS.md`](SKILLS.md)** — 它按场景告诉你什么时候该用什么功能，比本指南更实用。

### 第 2 步：配置

```bash
# 创建 .env
echo 'MINIMAX_CN_API_KEY=<user-provided-key>' > .env

# 配置 MCP 服务器（推荐）
# 在 Agent 的 MCP 配置中添加：
```

```json
{
  "mcpServers": {
    "wiki": {
      "command": "wiki",
      "args": ["mcp"]
    }
  }
}
```

### 第 3 步：创建知识库

```
① wiki_setup(action="questions")    → 获取问题列表
② 向用户提问：路径、模板、名称、描述
③ wiki_setup(action="create", ...)  → 创建知识库
```

### 第 4 步：导入文档

```
wiki_ingest(source="/path/to/file.pdf")
wiki_lint()                    → 检查生成页面
wiki_get_insights()            → 发现孤立页面、覆盖缺口
wiki_update_page(slug="...", related=["..."])  → 补充交叉引用
```

### 第 5 步：查询知识库

```
wiki_query(question="问题", llm=true)
```

### Agent 操作规范

| 规则 | 说明 |
|------|------|
| ✅ 必须用工具操作 | 所有 wiki 操作必须通过 wiki-cli 的 MCP 工具或 CLI 命令完成 |
| ❌ 不要直接写文件 | 不要自己创建或编辑 `wiki/` 下的 markdown 文件 |
| ❌ 不要改 raw/ | `raw/` 目录存放原始文档，不可修改 |
| ❌ 不要手写 frontmatter | `wiki_write` 和 `wiki_ingest` 会自动生成正确格式 |
| ❌ 不要创建重复实体 | 先用 `wiki_search` 检查是否已存在 |
| ✅ 每个页面必须有 sources | 追溯到来源文档 |

### MCP 工具列表（14 个）

| 工具 | 说明 |
|------|------|
| `wiki_setup` ⭐ | **入口工具** — 引导式创建/管理 wiki，返回结构化问题列表 |
| `wiki_ingest` | 摄入文档，2 步 LLM 管线自动生成页面 |
| `wiki_query` | 自然语言查询，支持 LLM 综合回答（`llm: true`） |
| `wiki_read` | 读取页面的 frontmatter 和内容 |
| `wiki_write` | 创建页面（frontmatter 自动生成） |
| `wiki_update_page` | 增量更新（合并 tags/related/sources） |
| `wiki_delete_page` | 删除页面 |
| `wiki_move_page` | 重命名页面 |
| `wiki_search` | 关键词或正则搜索 |
| `wiki_list` | 列出页面，可按类型过滤 |
| `wiki_stats` | 统计信息 |
| `wiki_lint` | 健康检查（断链、孤立页面等） |
| `wiki_graph` | 知识图谱（节点、边、社区） |
| `wiki_get_insights` | 分析洞察（Hub 页面、覆盖缺口、惊奇连接、Deep Research 建议） |

### 给 Agent 的 Prompt 模板

> 我想构建一个 wiki 知识库来管理我的研究资料。项目中有一个工具叫 `wiki-cli`，它是专门为 agent 设计的 wiki 知识库管理工具。
>
> **安装：**
> 1. `git clone https://github.com/hannahccc3/wiki-cli.git /tmp/wiki-cli`
> 2. `cd /tmp/wiki-cli && pip install -e . && pip install -e ".[mcp]"`
> 3. `wiki --help` 确认安装成功
>
> **必读：**
> - 读取 `SKILLS.md`（`/tmp/wiki-cli/SKILLS.md`）了解所有功能和适用场景
> - 读取 `AGENTS.md`（`/tmp/wiki-cli/src/wiki_cli/references/AGENTS.md`）了解操作规则
>
> **配置：**
> - 创建 `.env`，写入 `MINIMAX_CN_API_KEY=<key>`（向我要 key）
> - 如果支持 MCP，添加 wiki MCP 服务器：`{"command":"wiki","args":["mcp"]}`
>
> **创建知识库：**
> 1. 调用 `wiki_setup(action="questions")` 或 `wiki setup` 向我提问
> 2. 收集信息后创建知识库
>
> **重要：所有 wiki 操作必须通过 wiki-cli 的工具完成，不要直接写文件。**

---

## � 命令参考

| 命令 | 说明 |
|------|------|
| `wiki setup` | 交互式创建向导 |
| `wiki init` | 初始化 wiki 项目 |
| `wiki ingest <file>` | 导入单个文档 |
| `wiki ingest-batch <dir>` | 批量导入文档 |
| `wiki query <question>` | 查询知识库（混合：关键词 + 向量） |
| `wiki list` | 列出所有页面 |
| `wiki stats` | 查看统计信息 |
| `wiki index` | 管理索引 |
| `wiki lint` | 健康检查 |
| `wiki graph` | 知识图谱 |
| `wiki delete <slug>` | 删除页面 |
| `wiki move <old> <new>` | 重命名页面 |
| `wiki embed --all` | 建立向量索引 |
| `wiki embed --slug <name>` | 对单个页面建立索引 |
| `wiki embed --status` | 查看 embedding 状态 |
| `wiki research <question>` | 深度研究（网络搜索 + 自动摄入） |
| `wiki review --list` | 查看待审核项 |
| `wiki review --stats` | 审核统计 |
| `wiki review --resolve <id>` | 解决审核项 |
| `wiki review --retry-failed` | 重试失败的摄入 |
| `wiki serve` | 启动 Web 界面 |
| `wiki mcp` | 启动 MCP 服务器 |

所有命令支持全局 `--path` 参数：`wiki --path /path/to/wiki <command>`

---

## 🤖 LLM Provider 配置

支持 16 个 Provider，3 种线协议：

| Provider | 线协议 | 默认模型 |
|----------|--------|----------|
| `openai` | OpenAI Chat Completions | gpt-4o |
| `anthropic` | Anthropic Messages | claude-sonnet-4-5 |
| `google` | Gemini GenerateContent | gemini-2.5-flash |
| `deepseek` | OpenAI | deepseek-chat |
| `groq` | OpenAI | llama-3.3-70b |
| `xai` | OpenAI | grok-3 |
| `kimi` | OpenAI | kimi-k2.6 |
| `kimi-cn` | OpenAI | kimi-k2.6 |
| `zhipu` | OpenAI | glm-4.6 |
| `minimax` | Anthropic | MiniMax-M2.7 |
| `minimax-global` | Anthropic | MiniMax-M2.7 |
| `bailian` | OpenAI | qwen3.6-plus |
| `volcengine` | OpenAI | Doubao-Seed-2.0-Code |
| `xiaomi` | OpenAI | mimo-v2-pro |
| `ollama` | OpenAI | （用户自选） |
| `custom` | OpenAI/Anthropic | （用户自定义） |

**切换 Provider：**

```bash
# 方式 1：环境变量
export WIKI_CLI_LLM_PROVIDER=deepseek
export WIKI_CLI_LLM_API_KEY=your-key

# 方式 2：wiki-cli.yaml
echo 'llm:
  provider: ollama
  base_url: http://localhost:11434/v1
  model: qwen3:8b' > wiki-cli.yaml
```

---

## 🔢 Embedding 配置

支持本地 Ollama 或远程 OpenAI 兼容端点：

```yaml
# wiki-cli.yaml
embeddings:
  enabled: true
  base_url: http://localhost:11434/v1    # Ollama 本地
  model: qwen3-embedding:8b              # 或 nomic-embed-text
  dimensions: 4096
  max_chunk_chars: 1000
  overlap_chars: 200
```

```bash
ollama pull qwen3-embedding:8b           # 拉取模型
wiki embed --status                       # 检查连接
wiki embed --all                          # 建立索引
wiki query "问题"                          # 自动使用混合搜索
```

---

## ⚙️ 环境变量

| 变量 | 说明 |
|------|------|
| `WIKI_CLI_LLM_PROVIDER` | LLM Provider（默认 minimax） |
| `WIKI_CLI_LLM_API_KEY` | LLM API 密钥 |
| `WIKI_CLI_LLM_BASE_URL` | 自定义 LLM 端点 |
| `WIKI_CLI_LLM_MODEL` | 自定义模型名称 |
| `WIKI_CLI_LLM_WIRE` | 线协议（openai / anthropic / google） |
| `WIKI_CLI_EMBEDDINGS_BASE_URL` | Embedding 端点 |
| `WIKI_CLI_EMBEDDINGS_MODEL` | Embedding 模型 |
| `MINIMAX_CN_API_KEY` | MiniMax API 密钥（兼容） |
| `OPENAI_API_KEY` | OpenAI API 密钥（兼容） |

---

## �📁 项目结构

```
project/
├── AGENTS.md                # Agent 操作规则（init 时自动生成）
├── wiki-cli.yaml            # 项目配置（可选）
├── schema.md                # 模式定义
├── purpose.md               # 项目目标
├── raw/                     # 原始文档（不可变）
│   ├── sources/             # 来源文件
│   └── assets/              # 媒体资源
├── .llm-wiki/               # 内部数据
│   ├── project.json         # 项目元数据
│   ├── ingest-cache.json    # 摄入缓存
│   ├── ingest-queue.json    # 持久化摄入队列
│   ├── ingest-progress.json # 摄入进度
│   ├── review-queue.json    # 审核队列
│   ├── ingest-log.jsonl     # 摄入日志
│   ├── vectordb/            # LanceDB 向量索引
│   └── assets/
│       ├── images/          # 提取的图片
│       └── image-descriptions/  # 视觉模型生成的图片描述
├── wiki/                    # 所有 wiki 页面
│   ├── index.md             # 内容索引
│   ├── log.md               # 活动日志
│   ├── overview.md          # 项目概览
│   ├── entities/            # 实体页面
│   ├── concepts/            # 概念页面
│   ├── sources/             # 来源页面
│   ├── queries/             # 研究问题
│   ├── comparisons/         # 对比分析
│   └── synthesis/           # 综合洞察
└── .obsidian/               # Obsidian 配置（自动生成）
```

## 📝 页面格式

所有 wiki 页面使用 Markdown 格式，frontmatter 由工具自动生成：

**Entity/Concept/Query/Comparison/Synthesis 页面：**
```markdown
---
type: entity
title: 页面标题
created: 2025-01-01
updated: 2025-01-01
tags: [tag1, tag2]
related: [slug-1, slug-2]
sources: ["filename.md"]
---

# 页面标题

正文内容...使用 [[other-page]] 交叉引用其他页面
```

**Source 页面（额外字段）：**
```markdown
---
type: source
title: 论文标题
created: 2025-01-01
updated: 2025-01-01
tags: [tag1, tag2]
related: [concept-slug]
sources: ["filename.pdf"]
authors: [Author A, Author B]
year: 2024
url: "https://..."
venue: "NeurIPS 2024"
---
```

## 📄 许可证

MIT License
