---
type: entity
title: "Llama3-8B"
tags: [target-model, open-source, meta]
related: [llama-2-7b-chat, vicuna-7b, qwen-2.5-7b-instruct, gpt-3.5, gpt-4o, claude-3.5-sonnet, gemini-2.0-flash, harmbench, jailbreak-r1]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Llama3-8B

## Overview

**Llama3-8B** (Llama3-8B-Chat) is an open-source large language model by Meta, included as one of eight target models in the JAILBREAK-R1 evaluation.

## Performance in JAILBREAK-R1

| Method | ASR | Diversity |
|--------|-----|-----------|
| JAILBREAK-R1 | 58.50% | 0.956 |
| JAILBREAK-R1-Zero | 42.00% | 0.882 |
| AutoDAN-Turbo | 34.50% | 0.921 |
| TAP | 36.00% | 0.800 |
| PAIR | 32.50% | 0.734 |
| GPO | 34.50% | 0.875 |

## Key Findings

- JAILBREAK-R1 achieved the highest ASR (58.50%) among all methods
- The diversity score (0.956) indicates effective varied attack generation
- Notably, when targeting Llama-2-7B with targeted training, Llama3-8B showed decreased vulnerability

## Related Pages

- [[llama-2-7b-chat]] - Another Meta model tested
- [[jailbreak-r1]] - Method that achieved best results
- [[harmbench]] - Evaluation benchmark
- [[meta]] - Organization