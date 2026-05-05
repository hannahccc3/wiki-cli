---
type: entity
title: "Llama-2"
tags: ["Sprachmodell", "Open-Source", "Meta", "Chat-Modell", "大型语言模型", "开源模型", "越狱攻击目标", "LLM", "model"]
related: ["jailbreakbench", "llama-3-70b", "vicuna-13b-v1.5", "llama-guard", "jailbreaking", "renellm", "gpt-3.5", "gpt-4", "越狱提示", "安全对齐", "cold-attack", "mistral", "vicuna", "guanaco", "white-box-attacks", "mixtral"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md", "Ding 等 - 2023 - A Wolf in Sheep’s Clothing Generalized Nested Jailbreak Prompts can Fool Large Language Models Easi.md", "Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md"]
created: 2024-12-10
updated: 2024-12-10
---
# Llama-2

## Überblick

Llama-2 ist eine Familie von Open-Source-Sprachmodellen, entwickelt von Meta. In JailbreakBench werden verschiedene Versionen (7B, 13B) als Zielmodelle für die Evaluierung verwendet.

## Evaluierungsergebnisse

### Angriffs-Erfolgsraten
- PAIR: 0%
- GCG: 3%
- JB-Chat: 0%
- Prompt with RS: 90%

### Ablehnungsrate ohne Verteidigung
- Llama-2 7B: 65% (oft verweigernd)

## Besonderheiten

Llama-2 zeigt eine deutlich höhere Basis-Ablehnungsrate als Vicuna und ist resistenter gegen einige Angriffsmethoden wie PAIR und JB-Chat.

## Verwandte Seiten

- [[jailbreakbench]]
- [[vicuna]]
- [[gpt-3.5]]
- [[gpt-4]]
- [[mixtral]]