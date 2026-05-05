---
type: entity
title: "SmoothLLM"
tags: ["Verteidigung", "Semantische Glättung", "Testzeit-Verteidigung", "Perturbation", "méthode de défense", "robustesse", "piratage LLM", "Test-Time", "Semantic Smoothing", "Jailbreaking"]
related: ["jailbreakbench", "perplexity-filter", "erase-and-check", "jailbreaking", "verteidigungen", "pandora", "rlhf", "piratage-llm", "sécurité-llm", "perplexityfilter", "test-time-verteidigungen"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md", "Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md"]
created: 2024-12-10
updated: 2024-12-10
---
# SmoothLLM

## Überblick

SmoothLLM ist eine Test-Time-Verteidigung gegen Jailbreaking-Angriffe, die von Robey et al. (2023) entwickelt wurde. Die Verteidigung nutzt semantische Glättung, um potenzielle Jailbreak-Prompts zu erkennen und zu neutralisieren.

## Methode

SmoothLLM verwendet Swapping-Störungen mit folgenden Parametern:
- **N**: 10 perturbierte Samples
- **Perturbationsprozentsatz**: q = 10%

## Evaluierungsergebnisse (JailbreakBench)

| Angriff | Vicuna | Llama-2 | GPT-3.5 | GPT-4 |
|---------|--------|---------|---------|-------|
| PAIR | 55% | 0% | 5% | 19% |
| GCG | 4% | 0% | 0% | 4% |
| JB-Chat | 73% | 0% | 0% | 0% |
| Prompt with RS | 68% | 0% | 4% | 56% |

## Effektivität

SmoothLLM zeigt gemischte Ergebnisse:
- Sehr effektiv gegen GCG-Angriffe
- Weniger effektiv gegen JB-Chat und Prompt with RS
- Geringe Auswirkung auf die Ablehnungsrate bei harmlosen Anfragen

## Verwandte Seiten

- [[jailbreakbench]]
- [[perplexityfilter]]
- [[erase-and-check]]
- [[test-time-verteidigungen]]
- [[jailbreaking]]