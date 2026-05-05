---
type: entity
title: "Gemini-2.0"
tags: [target-model, closed-source, google]
related: [gpt-3.5, gpt-4o, claude-3.5-sonnet, llama-2-7b-chat, vicuna-7b, qwen-2.5-7b-instruct, llama-3-8b-chat, harmbench, jailbreak-r1]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Gemini-2.0

## Overview

**Gemini-2.0** (Gemini 2.0 Flash) is a closed-source large language model by Google, included as one of eight target models in the JAILBREAK-R1 evaluation.

## Performance in JAILBREAK-R1

| Method | ASR | Diversity |
|--------|-----|-----------|
| JAILBREAK-R1 | 47.00% | 0.987 |
| JAILBREAK-R1-Zero | 30.50% | 0.870 |
| AutoDAN-Turbo | 31.50% | 0.914 |
| TAP | 26.00% | 0.788 |
| PAIR | 25.50% | 0.725 |
| GPO | 23.00% | 0.900 |

## Key Findings

- JAILBREAK-R1 significantly outperformed other methods with 47.00% ASR
- The gap between JAILBREAK-R1 and JAILBREAK-R1-Zero (16.5%) is notable
- High diversity (0.987) demonstrates varied attack strategies

## Related Pages

- [[jailbreak-r1]] - Method that achieved best results
- [[harmbench]] - Evaluation benchmark
- [[google]] - Organization