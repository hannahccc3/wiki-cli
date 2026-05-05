---
type: concept
title: "Test-Time Defenses"
tags: ["Verteidigungsmechanismen", "LLM-Sicherheit", "Jailbreaking", "Inferenzzeit"]
related: ["jailbreaking", "smoothllm", "perplexity-filter", "erase-and-check", "jailbreakbench"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Test-Time Defenses

## Definition

Test-Time Defenses sind Verteidigungsmechanismen, die zur Inferenzzeit um Large Language Models herum implementiert werden, um [[jailbreaking|Jailbreaks]] zu erkennen und zu blockieren.

## Übersicht der implementierten Verteidigungen

### SmoothLLM
- **Methode**: Semantische Glättung durch perturbierte Abfragen
- **Parameter**: N = 10 perturbierte Samples, q = 10% Perturbationsrate
- **Effektivität**: Reduziert GCG-ASR von 80% auf 4% bei Vicuna

### Perplexity Filter
- **Methode**: Berechnung der Perplexität über Llama-2-7B
- **Funktion**: Erkennung anomaler Eingabemuster
- **Effektivität**: Besonders effektiv gegen GCG (Reduktion auf 3%)

### Erase-and-Check
- **Methode**: Entfernung von verdächtigen Tokens vor Verarbeitung
- **Erase-Länge**: 20 Tokens
- **Effektivität**: Solide Verteidigung gegen verschiedene Angriffe

### Synonym-Substitution
- **Methode**: Ersetzung von Wörtern mit Synonymen (5% Wahrscheinlichkeit)

### Non-Dictionary Removal
- **Methode**: Entfernung von Wörtern, die nicht im Wörterbuch sind

## Evaluationsergebnisse

| Angriff | SmoothLLM | Perplexity Filter | Erase-and-Check |
|---------|-----------|-------------------|-----------------|
| PAIR (Vicuna) | 55% | 69% | 0% |
| GCG (Vicuna) | 4% | 3% | 17% |
| JB-Chat (Vicuna) | 73% | 90% | 1% |
| Prompt mit RS (Vicuna) | 68% | 88% | 24% |

## Wichtige Überlegungen

### Adaptive Angriffe
> Die korrekte Evaluierung von Test-Time Defenses sollte auf adaptiven Angriffen basieren, d.h. Angriffen, die auf die spezifische Verteidigung zugeschnitten sind.

### Trade-offs
- **Inference-Zeit**: SmoothLLM erhöht die Inferenzzeit erheblich
- **False Positives**: Übermäßig konservative Verteidigungen können legitime Anfragen ablehnen
- **Refusal Rates**: 测试zeit-Vertidigungen sollten die Ablehnungsrate für gutartige Anfragen nicht zu stark erhöhen

## Verwandte Seiten

- [[jailbreaking]] – Jailbreaking Konzept
- [[smoothllm]] – SmoothLLM Verteidigung
- [[perplexity-filter]] – Perplexity Filter
- [[erase-and-check]] – Erase-and-Check
- [[jailbreakbench]] – JailbreakBench Benchmark
- [[adaptive-angriffe]] – Adaptive Angriffe