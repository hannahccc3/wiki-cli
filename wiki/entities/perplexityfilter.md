---
type: entity
title: "PerplexityFilter"
tags: ["Verteidigung", "Test-Time", "Perplexität", "Jailbreaking"]
related: ["jailbreakbench", "smoothllm", "erase-and-check", "test-time-verteidigungen", "jailbreaking"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# PerplexityFilter

## Überblick

PerplexityFilter ist eine Test-Time-Verteidigung gegen Jailbreaking-Angriffe, die von Jain et al. (2023) entwickelt wurde. Die Verteidigung nutzt Perplexität als Metrik, um potenzielle Jailbreak-Prompts zu erkennen.

## Methode

Der Filter berechnet die Perplexität von Eingaben unter Verwendung des Llama-2-7B-Modells und lehnt Eingaben ab, die eine bestimmte Perplexitätsschwelle überschreiten.

## Evaluierungsergebnisse (JailbreakBench)

| Angriff | Vicuna | Llama-2 | GPT-3.5 | GPT-4 |
|---------|--------|---------|---------|-------|
| PAIR | 69% | 0% | 17% | 30% |
| GCG | 3% | 1% | 0% | 0% |
| JB-Chat | 90% | 0% | 0% | 0% |
| Prompt with RS | 88% | 73% | 61% | 70% |

## Effektivität

PerplexityFilter zeigt unterschiedliche Ergebnisse:
- Sehr effektiv gegen GCG-Angriffe
- Weniger effektiv gegen Prompt with RS
- Begrenzte Auswirkung auf JB-Chat

## Verwandte Seiten

- [[jailbreakbench]]
- [[smoothllm]]
- [[erase-and-check]]
- [[test-time-verteidigungen]]
- [[jailbreaking]]