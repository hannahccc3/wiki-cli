---
type: concept
title: "Context Window"
tags: ["LLM architecture", "token limit", "context length", "capabilities"]
related: ["many-shot-jailbreaking", "in-context-learning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Context Window

## Overview

The context window refers to the maximum input length (measured in tokens) that a large language model can process in a single forward pass. Recent expansions have created new attack surfaces for jailbreaking techniques.

## Definition

Context window is the maximum number of tokens that can be included in a single prompt, encompassing all input tokens before the model's response begins.

## Evolution

| Period | Approximate Size | Analogy |
|--------|------------------|---------|
| 2022 | ~4,000 tokens | Long essay |
| 2024 | 10M tokens | Multiple novels or codebases |

## Implications for Many-shot Jailbreaking

1. **Enables MSJ**: The expansion made many-shot attacks feasible
2. **Attack Surface**: Longer contexts present new opportunities for manipulation
3. **Power Law Scaling**: Effectiveness follows predictable patterns up to hundreds of shots
4. **Model Differences**: Different models have different maximum context lengths (e.g., Llama 2 70B limited to 4,096 tokens)

## Mitigation Considerations

Simply constraining context length is undesirable as it impacts model usefulness. Effective solutions must address the underlying vulnerability without limiting legitimate use cases.

## Related Concepts

- [[many-shot-jailbreaking]] - Attack that exploits context windows
- [[in-context-learning]] - Capability enhanced by larger contexts