---
type: concept
title: "Adaptive Angriffe"
tags: ["Adaptive Angriffe", "Jailbreaking", "LLM-Sicherheit", "Verteidigungsumbgehung"]
related: ["jailbreaking", "test-time-defenses", "jailbreakbench", "weisskasten-angriffe", "schwarzkasten-angriffe"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Adaptive Angriffe

## Definition

Adaptive Angriffe sind [[jailbreaking|Jailbreak]]-Angriffe, die speziell auf eine bestimmte Verteidigung zugeschnitten sind. Sie zielen darauf ab, die spezifischen Schwächen einer Verteidigungsstrategie auszunutzen.

## Bedeutung

> Die korrekte Evaluierung von Test-Time Defenses sollte auf adaptiven Angriffen basieren, d.h. Angriffen, die auf die spezifische Verteidigung zugeschnitten sind.

## Übertragungsangriffe als Untergrenze

Im [[jailbreakbench]] werden Transfer-Angriffe verwendet:
- Jailbreak-Strings von unverteidigten Modellen werden auf verteidigte Modelle angewendet
- Dies liefert eine **untere Schranke** für die worst-case Angriffserfolgsrate
- Adaptive Angriffe können diese Rate potenziell übertreffen

## Strategien für Adaptive Angriffe

1. **Analyse der Verteidigung** – Identifizierung von Schwachstellen
2. **Spezialisierte Optimierung** – Anpassung der Angriffsparameter
3. **Umgehung von Filtern** – Entwicklung von Prompts, die Perplexity-Filter umgehen
4. **Anti-SmoothLLM** – Prompts, die trotz Perturbationen funktionieren

## Evaluationsergebnisse

| Angriff | SmoothLLM (Vicuna) | Perplexity Filter (Vicuna) |
|---------|-------------------|---------------------------|
| PAIR | 55% | 69% |
| GCG | 4% | 3% |
| JB-Chat | 73% | 90% |
| Prompt mit RS | 68% | 88% |

## Verwandte Seiten

- [[jailbreaking]] – Jailbreaking Konzept
- [[test-time-defenses]] – Test-Time Defenses
- [[jailbreakbench]] – JailbreakBench Benchmark
- [[weisskasten-angriffe]] – Weißkasten-Angriffe
- [[schwarzkasten-angriffe]] – Schwarzkasten-Angriffe
- [[smoothllm]] – SmoothLLM
- [[perplexity-filter]] – Perplexity Filter