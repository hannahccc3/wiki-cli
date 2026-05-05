---
type: entity
title: "Erase-and-Check"
tags: ["Verteidigung", "Testzeit-Verteidigung", "Sicherheitsmechanismus", "Test-Time", "Jailbreaking"]
related: ["jailbreakbench", "smoothllm", "perplexity-filter", "jailbreaking", "verteidigungen", "perplexityfilter", "test-time-verteidigungen"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# Erase-and-Check

## Überblick

Erase-and-Check ist eine Test-Time-Verteidigung gegen Jailbreaking-Angriffe, die von Kumar et al. (2023) entwickelt wurde. Die Verteidigung gilt als die solideste der im JailbreakBench evaluierten Baseline-Verteidigungen.

## Methode

Der Filter verwendet eine Löschlänge von 20 Tokens und analysiert die Reaktionen des Modells auf modifizierte Eingaben.

## Evaluierungsergebnisse (JailbreakBench)

| Angriff | Vicuna | Llama-2 | GPT-3.5 | GPT-4 |
|---------|--------|---------|---------|-------|
| PAIR | 0% | 0% | 2% | 1% |
| GCG | 17% | 1% | 3% | 2% |
| JB-Chat | 1% | 0% | 0% | 0% |
| Prompt with RS | 24% | 25% | 8% | 10% |

## Effektivität

Erase-and-Check zeigt durchgehend niedrige Angriffserfolgsraten:
- Sehr effektiv gegen PAIR, GCG und JB-Chat
- Mäßig effektiv gegen Prompt with RS
- Niedrigste durchschnittliche ASR unter allen Verteidigungen

## Verwandte Seiten

- [[jailbreakbench]]
- [[smoothllm]]
- [[perplexityfilter]]
- [[test-time-verteidigungen]]
- [[jailbreaking]]