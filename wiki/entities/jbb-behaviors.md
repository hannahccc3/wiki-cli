---
type: entity
title: "JBB-Behaviors"
tags: ["Datensatz", "LLM-Sicherheit", "Jailbreaking", "Missbrauchsszenarien", "Schädliche Verhaltensweisen"]
related: ["jailbreakbench", "advbench", "harmbench", "jailbreaking", "llm"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# JBB-Behaviors

## Überblick

JBB-Behaviors ist ein Datensatz mit 100 verschiedenen Missbrauchsverhaltensweisen, der im Rahmen des JailbreakBench-Benchmarks erstellt wurde. Der Datensatz dient zur Bewertung von Jailbreaking-Angriffen und -Verteidigungen bei großen Sprachmodellen.

## Zusammensetzung

- **18%** aus AdvBench (Zou et al., 2023)
- **27%** aus TDC/HarmBench (Mazeika et al., 2023, 2024)
- **55%** originale Verhaltensweisen

## Struktur

Jede Zeile im Datensatz enthält fünf Felder:
1. **Behavior**: Eindeutiger Identifikator für ein bestimmtes Missbrauchsverhalten
2. **Goal**: Anfrage, die ein anstößiges Verhalten anfordert
3. **Target**: Bestätigende Antwort auf die schädliche Zielzeichenfolge
4. **Category**: Breitere Kategorie von Missbrauch entsprechend den Nutzungsrichtlinien von OpenAI
5. **Source**: Referenz zur Quell-Datenbank der Goal- und Target-Zeichenfolge

## Benigne Verhaltensweisen

Zusätzlich wurden 100 benigne Verhaltensweisen erstellt, die das exakte Thema der entsprechenden schädlichen Verhaltensweise abdecken. Diese werden verwendet, um Ablehnungsraten für verschiedene Modelle und Verteidigungen zu evaluieren.

## Verwandte Seiten

- [[jailbreakbench]]
- [[harmbench]]
- [[advbench]]
- [[jailbreaking]]