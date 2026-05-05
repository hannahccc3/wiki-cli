---
type: concept
title: "Angriffserfolgsrate (ASR)"
tags: ["Metriken", "Jailbreaking", "LLM-Sicherheit", "Evaluierung"]
related: ["jailbreaking", "jailbreakbench", "jailbreak-judge", "gcg", "pair"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Angriffserfolgsrate (ASR)

## Definition

Die Angriffserfolgsrate (Attack Success Rate, ASR) ist eine Metrik zur Messung des Prozentsatzes erfolgreicher Jailbreak-Angriffe auf ein Large Language Model.

## Berechnung

```
ASR = (Anzahl erfolgreicher Jailbreaks / Gesamtzahl der Versuche) × 100%
```

## Bedeutung

Die ASR ist die zentrale Metrik im [[jailbreakbench]] Benchmark für die Bewertung von:
- Jailbreaking-Angriffen
- Effektivität von Verteidigungsmechanismen
- Robustheit von LLMs

## Beispielwerte aus JailbreakBench

| Angriff | Vicuna-13B | Llama-2-7B | GPT-3.5 | GPT-4 |
|---------|------------|------------|---------|-------|
| PAIR | 69% | 0% | 71% | 34% |
| GCG | 80% | 3% | 47% | 4% |
| JB-Chat | 90% | 0% | 0% | 0% |
| Prompt mit RS | 89% | 90% | 93% | 78% |

## Einflussfaktoren

Die ASR kann durch verschiedene Faktoren beeinflusst werden:
- **Wahl des [[jailbreak-judge]]** – Unterschiedliche Richter führen zu unterschiedlichen ASR-Werten
- **Angriffsart** – Schwarzkasten- vs. Weißkasten-Angriffe
- **Zielmodell** – Unterschiedliche LLMs zeigen unterschiedliche Robustheit
- **Verteidigungsmechanismen** – SmoothLLM, Perplexity Filter etc.

## Verwandte Seiten

- [[jailbreaking]] – Jailbreaking Konzept
- [[jailbreakbench]] – JailbreakBench Benchmark
- [[jailbreak-judge]] – Jailbreak-Richter
- [[gcg]] – GCG Angriff
- [[pair]] – PAIR Angriff
- [[smoothllm]] – SmoothLLM Verteidigung
- [[perplexity-filter]] – Perplexity Filter
- [[erase-and-check]] – Erase-and-Check