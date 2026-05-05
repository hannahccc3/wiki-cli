---
type: entity
title: "HarmBench"
tags: ["Benchmark", "Red-Teaming", "Jailbreaking", "LLM-Sicherheit"]
related: ["jailbreakbench", "advbench", "jbb-behaviors", "jailbreaking"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# HarmBench

## Überblick

HarmBench ist ein standardisierter Evaluierungsrahmen für automatisiertes Red-Teaming und robuste Ablehnung, entwickelt von Mazeika et al. (2024). Der Benchmark inspirierte und trug zum JBB-Behaviors-Datensatz in JailbreakBench bei.

## Hauptmerkmale

- Breites Themenspektrum einschließlich Urheberrechtsverletzungen und multimodaler Modelle
- Implementierung von Jailbreaking-Angriffen und -Verteidigungen
- Llama-2-13B-basierter Richter

## Verbindung zu JailbreakBench

HarmBench war eine wichtige Quelle für den JBB-Behaviors-Datensatz (27% der Verhaltensweisen stammen aus HarmBench/TDC). JailbreakBench konzentriert sich jedoch auf:
- Unterstützung von adaptiven Angriffen
- Standardisierung von Test-Time-Verteidigungen
- Community-getriebener Ansatz

## Verwandte Seiten

- [[jailbreakbench]]
- [[advbench]]
- [[jbb-behaviors]]
- [[jailbreaking]]