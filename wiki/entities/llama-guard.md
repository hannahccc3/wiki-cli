---
type: entity
title: "Llama Guard"
tags: ["Sicherheitsmodell", "Schutzmodell", "Fine-Tuning", "Input-Output-Safeguard", "LLM-Schutz", "Eingabe-Ausgabe-Schutz"]
related: ["jailbreakbench", "llama-2", "llama-3-70b", "smoothllm", "jailbreaking", "llama-guard-2", "llama-3-70b-richter"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# Llama Guard

## Überblick

Llama Guard ist ein LLM-Schutzmodell, das von Inan et al. (2023) von Llama-2-7B feinabgestimmt wurde. Es dient als Eingabe-Ausgabe-Schutz für Mensch-KI-Konversationen.

## Verwendung in JailbreakBench

In der Evaluierung der Richter-Klassifikatoren erreichte Llama Guard:
- **Übereinstimmung**: 72,0%
- **FPR**: 9,0%
- **FNR**: 60,9%

Das Modell wurde auch für SmoothLLM und Erase-and-Check als Jailbreak-Richter verwendet.

## Verwandte Seiten

- [[llama-guard-2]]
- [[llama-3-70b-richter]]
- [[jailbreaking]]