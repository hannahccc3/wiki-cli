---
type: entity
title: "Vicuna"
tags: ["LLM", "model", "Open-Source", "Chatbot"]
related: ["cold-attack", "llama-2", "mistral", "guanaco", "gpt-3.5", "gpt-4", "white-box-attacks", "jailbreakbench", "mixtral"]
sources: ["Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md", "Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# Vicuna

## Überblick

Vicuna-13B-v1.5 ist ein Open-Source-Chatbot-Modell, das in JailbreakBench als eines der Zielmodelle für die Evaluierung von Jailbreaking-Angriffen und -Verteidigungen verwendet wird.

## Evaluierungsergebnisse

### Angriffs-Erfolgsraten
- PAIR: 69%
- GCG: 80%
- JB-Chat: 90%
- Prompt with RS: 89%

### Ablehnungsrate ohne Verteidigung
- Vicuna 13B: 10% (selten verweigernd)

## Verwandte Seiten

- [[jailbreakbench]]
- [[llama-2]]
- [[gpt-3.5]]
- [[gpt-4]]
- [[mixtral]]