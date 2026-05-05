---
type: entity
title: "Vicuna-13B-v1.5"
tags: ["Sprachmodell", "Open-Source", "Chatbot", "Fine-Tuned"]
related: ["jailbreakbench", "llama-2", "gpt-4", "gpt-3.5", "jailbreaking"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Vicuna-13B-v1.5

## Überblick

**Vicuna-13B-v1.5** ist ein Open-Source-Sprachmodell, das in JailbreakBench als eines der primären Testzielmodelle verwendet wird.

## Benchmark-Performance

### Ohne Verteidigung

| Angriff | Erfolgsrate |
|---------|-------------|
| PAIR | 69% |
| GCG | 80% |
| JB-Chat | 90% |
| Prompt mit RS | 89% |

### Mit SmoothLLM

| Angriff | Erfolgsrate |
|---------|-------------|
| PAIR | 55% |
| GCG | 4% |
| JB-Chat | 73% |
| Prompt mit RS | 68% |

### Mit Perplexity-Filter

| Angriff | Erfolgsrate |
|---------|-------------|
| PAIR | 69% |
| GCG | 3% |
| JB-Chat | 90% |
| Prompt mit RS | 88% |

### Mit Erase-and-Check

| Angriff | Erfolgsrate |
|---------|-------------|
| PAIR | 0% |
| GCG | 17% |
| JB-Chat | 1% |
| Prompt mit RS | 24% |

## Bewertung

Vicuna-13B zeigt sich als **hochanfällig für Jailbreak-Angriffe** ohne Verteidigung (80-90% Erfolgsrate für GCG und JB-Chat). Mit Erase-and-Check werden diese auf 0-24% reduziert.

## Verwandte Seiten

- [[jailbreakbench]]
- [[llama-2]]
- [[gpt-4]]
- [[gpt-3.5]]
- [[jailbreaking]]