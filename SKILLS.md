# wiki-cli — Agent Skill Guide

> Agent 克隆项目后，请先阅读此文件。它告诉你 wiki-cli 能做什么，以及什么时候该用什么功能。

## 快速安装

```bash
pip install -e .
pip install -e ".[mcp]"     # MCP 支持（可选）
wiki --help                  # 验证安装
```

配置 API Key（二选一）：
```bash
echo 'MINIMAX_CN_API_KEY=<key>' > .env    # MiniMax（默认）
echo 'OPENAI_API_KEY=<key>' > .env        # OpenAI 兼容
```

---

## 场景 → 功能选择

### 🟢 用户想创建知识库

**用户会说：**
- "帮我建一个知识库"
- "我想整理我的研究资料"
- "我想做一个 wiki"

**你应该做：**
1. 询问用户：知识库建在哪里？什么类型？叫什么名字？
2. 运行 `wiki init --template <类型> --name "<名称>" --path <路径>`
3. 告诉用户可以开始导入文档了

**类型选项：** `research`（学术研究）/ `reading`（阅读笔记）/ `personal`（个人成长）/ `business`（商业团队）/ `general`（通用）

---

### 📄 用户想导入文档

**用户会说：**
- "把这个文件加到知识库里"
- "帮我分析这篇论文"
- "导入这些资料"

**你应该做：**
- 单个文件：`wiki ingest <文件路径>`
- 整个目录：`wiki ingest-batch <目录路径> --recursive`

**导入后自动完成：**
- LLM 分析文档内容
- 提取实体、概念、来源
- 生成结构化 wiki 页面
- 图片自动提取 + 视觉模型描述（如有）
- 低置信度内容自动进入审核队列

**导入后建议做：**
```bash
wiki lint               # 检查生成质量
wiki review --list      # 查看需要人工确认的项
```

---

### 🔍 用户想搜索/查询

**用户会说：**
- "知识库里有什么关于 X 的？"
- "X 是什么？"
- "帮我查一下 X"

**你应该做：**
- 简单搜索：`wiki search "<关键词>"` 或 MCP `wiki_search(query="...")`
- 自然语言问答：`wiki query "<问题>"` 或 MCP `wiki_query(question="...", llm=true)`
  - `llm=true` 会基于检索结果综合回答，适合复杂问题
  - 不带 `llm` 只返回相关页面列表

**如果启用了向量搜索（embedding）：**
- `wiki query` 自动使用混合搜索（关键词 + 语义向量），效果更好

---

### 📊 用户想看知识库全貌

**用户会说：**
- "知识库现在有什么？"
- "帮我看看整体情况"
- "知识库的统计"

**你应该做：**
```bash
wiki list               # 所有页面列表
wiki stats              # 统计信息（页面数、标签分布）
wiki graph              # 知识图谱（节点、边、社区）
```

MCP 工具：`wiki_list()` / `wiki_stats()` / `wiki_graph()`

---

### 💡 用户想发现知识空白 / 获得洞察

**用户会说：**
- "知识库还有什么缺失的？"
- "帮我看看有没有什么有趣的发现"
- "哪些知识点之间有联系？"

**你应该做：**
- `wiki_get_insights()` 或 `wiki graph` + 分析结果
- 返回内容包括：
  - **Hub 页面** — 被引用最多的核心实体
  - **知识空白** — 只有 0-1 个连接的孤立页面
  - **惊奇连接** — 共享来源但无直接链接的页面对（可能遗漏了重要关系）
  - **Deep Research 建议** — 基于知识空白自动生成的研究方向

---

### 🔬 用户想深入研究某个主题

**用户会说：**
- "帮我深入调研 X"
- "我想了解 X 的最新进展"
- "帮我搜索一下 X"

**你应该做：**
```bash
wiki research "<研究问题>" --topics 3
```

**自动完成：**
1. LLM 生成 3 个搜索角度
2. DuckDuckGo 搜索每个角度
3. 抓取网页内容
4. LLM 综合分析
5. 结果自动摄入为 wiki 页面

---

### ✏️ 用户想修改/整理知识库

**用户会说：**
- "把 X 页面加上 Y 标签"
- "把 A 页面重命名为 B"
- "删除这个页面"
- "这两个概念应该关联起来"

**你应该做：**

| 意图 | 命令 / MCP |
|------|-----------|
| 补充标签/关联 | `wiki_update_page(slug="...", tags=["新标签"], related=["其他页面"])` |
| 重命名 | `wiki move <旧slug> <新slug>` |
| 删除 | `wiki delete <slug> -y` |
| 创建新页面 | `wiki_write(title="...", page_type="concept", content="...")` |

**重要：** `wiki_update_page` 是增量合并（不会覆盖已有标签/关联），可以放心使用。

---

### 🔧 用户想做健康检查

**用户会说：**
- "帮我检查知识库有没有问题"
- "有没有断链？"
- "知识库健康吗？"

**你应该做：**
```bash
wiki lint               # 检查 6 类问题
wiki lint --fix         # 自动修复可修复的问题
```

检查项：断链、孤立页面、缺失 frontmatter 字段、过期内容、重复实体、空页面

---

### 🔢 用户想启用向量搜索

**用户会说：**
- "能不能语义搜索？"
- "帮我建立向量索引"
- "embedding 怎么用？"

**你应该做：**
1. 确认 Ollama 已安装：`ollama list | grep embed`
2. 如无模型：`ollama pull qwen3-embedding:8b`
3. 在 `wiki-cli.yaml` 中添加：
   ```yaml
   embeddings:
     enabled: true
   ```
4. 建立索引：`wiki embed --all`
5. 之后 `wiki query` 自动使用混合搜索

---

### 🔍 用户想审核低质量内容

**用户会说：**
- "有没有需要我确认的内容？"
- "哪些内容不确定？"

**你应该做：**
```bash
wiki review --list          # 查看待审核项
wiki review --stats         # 审核统计
wiki review --resolve <id> --action approve   # 确认通过
wiki review --resolve <id> --action reject    # 拒绝
```

审核项来源：ingest 时 LLM 自动标记的低置信度提取（< 0.5）、歧义实体、潜在矛盾。

---

### 🌐 用户想浏览知识库

**用户会说：**
- "我想看看知识库"
- "有没有可视化界面？"

**你应该做：**
```bash
wiki serve --port 8080      # 启动 Web 界面
```
或告诉用户可以用 Obsidian 打开知识库目录（自动生成 `.obsidian/` 配置）。

---

## MCP 连接（推荐）

如果 Agent 支持 MCP 协议，添加到配置中：

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

14 个 MCP 工具：`wiki_setup` / `wiki_ingest` / `wiki_query` / `wiki_read` / `wiki_write` / `wiki_update_page` / `wiki_delete_page` / `wiki_move_page` / `wiki_search` / `wiki_list` / `wiki_stats` / `wiki_lint` / `wiki_graph` / `wiki_get_insights`

---

## 多 Provider 支持

通过环境变量切换 LLM：

```bash
export WIKI_CLI_LLM_PROVIDER=deepseek    # 或 openai / anthropic / ollama / ...
export WIKI_CLI_LLM_API_KEY=your-key
```

或 `wiki-cli.yaml`：
```yaml
llm:
  provider: ollama
  base_url: http://localhost:11434/v1
  model: qwen3:8b
```

支持：openai / anthropic / google / deepseek / groq / xai / kimi / zhipu / minimax / bailian / volcengine / xiaomi / ollama / custom

---

## ⚠️ 注意事项

1. **不要直接编辑 `wiki/` 下的文件** — 所有操作必须通过 wiki-cli 工具
2. **不要修改 `raw/` 目录** — 原始文档不可变
3. **创建页面前先搜索** — 用 `wiki_search` 检查是否已存在，避免重复
4. **每个页面必须有 sources** — 追溯到来源文档
5. **所有命令支持 `--path`** — 可以远程操作任意位置的知识库
