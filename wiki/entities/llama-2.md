---
type: entity
title: "Llama 2 (70B)"
tags: ["Sprachmodell", "Open-Source", "Meta", "Chat-Modell", "大型语言模型", "开源模型", "越狱攻击目标", "LLM", "model"]
related: ["jailbreakbench", "llama-3-70b", "vicuna-13b-v1.5", "llama-guard", "jailbreaking", "renellm", "gpt-3.5", "gpt-4", "越狱提示", "安全对齐", "cold-attack", "mistral", "vicuna", "guanaco", "white-box-attacks", "mixtral", "claude-2.0", "mistral-7b"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md", "Ding 等 - 2023 - A Wolf in Sheep’s Clothing Generalized Nested Jailbreak Prompts can Fool Large Language Models Easi.md", "Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md", "Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Llama 2 (70B)

## Overview

Llama 2 (70B) is Meta's 70-billion parameter language model, evaluated in the Many-shot Jailbreaking research. It was found to be susceptible to many-shot jailbreaking attacks.

## Key Findings from Research

### Susceptibility

Llama 2 (70B) showed vulnerability to many-shot jailbreaking:
- Maximum context length of 4096 tokens limited the number of shots
- Attack effectiveness follows predictable power laws
- Similar scaling behavior to other models

## Model Specifications

| Attribute | Value |
|-----------|-------|
| Parameters | 70 Billion |
| Developer | Meta |
| Max Context | 4096 tokens |

## Related Pages

- [[claude-2.0]]
- [[gpt-4]]
- [[mistral-7b]]
- [[many-shot-jailbreaking]]