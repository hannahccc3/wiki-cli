---
type: entity
title: "Qwen2.5-7B"
tags: [target-model, open-source, alibaba, base-model]
related: [qwen-2.5-1.5b-instruct, llama-2-7b-chat, vicuna-7b, llama-3-8b-chat, gpt-3.5, gpt-4o, claude-3.5-sonnet, gemini-2.0-flash, harmbench, jailbreak-r1]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Qwen2.5-7B

## Overview

**Qwen2.5-7B** (Qwen2.5-7B-Instruct) is an open-source large language model by Alibaba, used both as a target model and as the base model for JAILBREAK-R1.

## As Base Model for JAILBREAK-R1

JAILBREAK-R1 uses Qwen2.5-7B-Instruct as its base model, fine-tuned through:
1. Cold start with 2K high-quality samples
2. Warm-up on 1K attack targets
3. Training on 5K attack targets
4. Curriculum learning with 3 degraded intermediate models

## Performance as Target Model

| Method | ASR | Diversity |
|--------|-----|-----------|
| JAILBREAK-R1 | 87.50% | 0.974 |
| JAILBREAK-R1-Zero | 76.00% | 0.861 |
| AutoDAN-Turbo | 82.50% | 0.928 |
| TAP | 72.50% | 0.797 |
| PAIR | 65.50% | 0.764 |
| GPO | 62.00% | 0.857 |

## Targeted Training Results

After targeted training on Qwen2.5-7B:
- ASR improved from 84% to 88% (+4%)
- Cross-model effects: minimal impact on other models

## Key Findings

- Qwen2.5-7B showed highest vulnerability among all tested models
- JAILBREAK-R1 achieved the highest ASR (87.50%) and best diversity (0.974)

## Related Pages

- [[jailbreak-r1]] - Method using this as base model
- [[qwen-2.5-1.5b-instruct]] - Teacher model for classification
- [[harmbench]] - Evaluation benchmark
- [[alibaba]] - Organization