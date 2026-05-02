# 研究模板模式 (Research Template Schema)

## 概述

本文档定义了 `wiki-cli` 研究模板的页面结构和规范。

## 页面类型

| 类型 | 目录 | 用途 | 示例 |
|------|------|------|------|
| `entity` | `wiki/entities/` | 命名实体：人物、组织、产品 | 研究者、实验室、公司 |
| `concept` | `wiki/concepts/` | 抽象概念：理论、方法、技术 | 注意力机制、强化学习 |
| `source` | `wiki/sources/` | 文献来源：论文、书籍、文章 | 学术论文、技术博客 |
| `query` | `wiki/queries/` | 研究问题 | "Transformer 能否用于时序预测？" |
| `comparison` | `wiki/comparisons/` | 对比分析 | GPT-4 vs Claude 对比 |
| `synthesis` | `wiki/synthesis/` | 综合洞察 | 多篇论文的综合分析 |
| `overview` | `wiki/` | 全局概览 | 项目概述、Wiki 索引 |

## 前置元数据 (Frontmatter)

所有页面必须包含 YAML 格式的前置元数据，以 `---` 分隔。

### 通用字段

```yaml
---
type: entity          # 页面类型（必填）
title: 页面标题       # 页面标题（必填）
tags: [tag1, tag2]    # 标签列表
related: [slug1, slug2]  # 相关页面 slug 列表
created: 2025-01-01   # 创建日期
updated: 2025-01-01   # 更新日期
---
```

### Source 类型附加字段

```yaml
---
type: source
title: 论文标题
tags: [attention, transformer]
related: [attention-mechanism]
created: 2025-01-01
updated: 2025-01-01
authors: [作者1, 作者2]    # 作者列表
year: "2024"               # 发表年份
url: https://arxiv.org/... # 链接
venue: NeurIPS 2024        # 发表场所
---
```

## 内容结构规范

### Entity 页面

```markdown
---
type: entity
title: OpenAI
tags: [ai-company, llm]
related: [gpt-4, chatgpt]
created: 2025-01-01
updated: 2025-01-01
---

# OpenAI

## 概述

OpenAI 是一家人工智能研究实验室...

## 关键信息

- **成立时间**: 2015 年
- **总部**: 旧金山
- **主要产品**: GPT 系列、DALL-E、ChatGPT

## 相关页面

- [[GPT-4]] — 旗舰语言模型
- [[ChatGPT]] — 对话应用
```

### Concept 页面

```markdown
---
type: concept
title: 注意力机制
tags: [deep-learning, nlp]
related: [transformer, self-attention]
created: 2025-01-01
updated: 2025-01-01
---

# 注意力机制

## 定义

注意力机制是一种让模型在处理输入时...

## 核心原理

1. Query、Key、Value 三元组
2. 缩放点积注意力公式
3. 多头注意力

## 变体

- 自注意力 (Self-Attention)
- 交叉注意力 (Cross-Attention)
- 稀疏注意力 (Sparse Attention)
```

### Source 页面

```markdown
---
type: source
title: "Attention Is All You Need"
tags: [attention, transformer, nlp]
related: [attention-mechanism, transformer]
created: 2025-01-01
updated: 2025-01-01
authors: [Vaswani, Shazeer, Parmar]
year: "2017"
url: https://arxiv.org/abs/1706.03762
venue: NeurIPS 2017
---

# Attention Is All You Need

## 摘要

本文提出了 Transformer 架构...

## 主要贡献

1. 提出全新的注意力架构
2. 证明无需循环和卷积即可实现 SOTA
3. 引入位置编码

## 关键发现

- 自注意力可以并行计算
- 多头注意力捕获不同子空间的信息
```

## Wiki 链接

使用 `[[页面标题]]` 语法创建页面间的链接。链接目标应为页面的 slug：

```markdown
参见 [[attention-mechanism]] 了解基本概念。
相关论文: [[attention-is-all-you-need]]
```

## 目录结构

```
project/
├── .llm-wiki/
│   ├── project.json      # 项目元数据
│   ├── ingest-cache.json # 摄入缓存
│   └── assets/           # 媒体资源
├── wiki/
│   ├── entities/         # 实体页面
│   ├── concepts/         # 概念页面
│   ├── sources/          # 来源页面
│   ├── queries/          # 问题页面
│   ├── comparisons/      # 对比页面
│   ├── synthesis/        # 综合页面
│   ├── media/            # 媒体文件
│   ├── index.md          # 索引页
│   ├── log.md            # 活动日志
│   └── overview.md       # 概览页
├── schema.md             # 模式定义
└── purpose.md            # 项目目标
```

## 最佳实践

1. **保持链接完整性**: 每个页面至少链接到一个其他页面
2. **使用标签**: 为页面添加相关标签以便搜索和分类
3. **定期更新**: 使用 `wiki index --update` 保持索引同步
4. **先源后分析**: 先录入 `source`，再创建分析性的 `synthesis` 和 `comparison`
5. **避免孤立页面**: 使用 `wiki lint` 检查断链和孤立页面
