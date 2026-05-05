---
type: entity
title: "Vicuna-7B"
tags: [target-model, open-source]
related: [llama-2-7b-chat, llama-3-8b-chat, qwen-2.5-7b-instruct, gpt-3.5, gpt-4o, claude-3.5-sonnet, gemini-2.0-flash, harmbench, jailbreak-r1]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Vicuna-7B

## Overview

**Vicuna-7B** is an open-source large language model, included as one of eight target models in the JAILBREAK-R1 evaluation.

## Performance in JAILBREAK-R1

| Method | ASR | Diversity |
|--------|-----|-----------|
| JAILBREAK-R1 | 89.50% | 0.968 |
| JAILBREAK-R1-Zero | 91.50% | 0.871 |
| AutoDAN-Turbo | 88.50% | 0.921 |
| TAP | 82.00% | 0.763 |
| PAIR | 79.00% | 0.785 |
| GPO | 84.50% | 0.872 |

## Key Findings

- Vicuna-7B showed high vulnerability across all methods
- JAILBREAK-R1-Zero paradoxically achieved the highest ASR (91.50%) on this model
- This suggests the model's vulnerabilities are easily exploitable without specialized training

## Related Pages

- [[jailbreak-r1]] - Method
- [[jailbreak-r1-zero]] - Variant achieving highest ASR
- [[harmbench]] - Evaluation benchmark