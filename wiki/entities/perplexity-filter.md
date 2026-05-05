---
type: entity
title: "Perplexity-Filter"
tags: ["Verteidigung", "Perplexität", "Anomalieerkennung", "Testzeit-Verteidigung"]
related: ["jailbreakbench", "smoothllm", "erase-and-check", "jailbreaking", "verteidigungen"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Perplexity-Filter

## Überblick

Der **Perplexity-Filter** ist eine **Testzeit-Verteidigungsmethode** gegen Jailbreak-Angriffe. Die Methode analysiert die Perplexität von Eingaben, um potenzielle Jailbreaks zu erkennen und zu blockieren.

## Methode

Die Perplexität einer Eingabe wird mittels **Llama-2-7B** berechnet. Hohe Perplexitätswerte deuten auf potenziell adversarial manipulierte Eingaben hin, die dann abgelehnt oder markiert werden.

## Leistung gegen Angriffe

| Angriff | Vicuna | Llama-2 | GPT-3.5 | GPT-4 |
|---------|--------|---------|---------|-------|
| PAIR | 69% | 0% | 17% | 30% |
| GCG | 3% | 1% | 0% | 0% |
| JB-Chat | 90% | 0% | 0% | 0% |
| Prompt mit RS | 88% | 73% | 61% | 70% |

## Bewertung

Der Perplexity-Filter zeigt **selektive Wirksamkeit**:
- **Besonders wirksam gegen**: GCG (reduziert auf 1-3%)
- **Wenig wirksam gegen**: Prompt mit RS und JB-Chat

## Verwandte Seiten

- [[jailbreakbench]]
- [[smoothllm]]
- [[erase-and-check]]
- [[jailbreaking]]
- [[verteidigungen]]