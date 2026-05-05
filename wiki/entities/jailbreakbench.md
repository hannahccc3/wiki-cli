---
type: entity
title: "JailbreakBench"
tags: ["Benchmark", "LLM-Sicherheit", "Jailbreaking", "Open-Source"]
related: ["jbb-behaviors", "harmbench", "advbench", "llama-3-70b", "robustbench", "pair", "gcg", "smoothllm", "perplexity-filter", "perplexityfilter", "erase-and-check", "llama-3-70b-richter"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# JailbreakBench

## Überblick

JailbreakBench ist ein Open-Source-Benchmark zur Standardisierung der Bewertung von Jailbreaking-Angriffen und -Verteidigungen bei großen Sprachmodellen (LLMs). Das Benchmark wurde 2024 von einem Team von Forschern unter der Leitung von Patrick Chao entwickelt.

## Hauptkomponenten

### 1. Repository von Jailbreak-Artefakten
Ein evolvierendes Repository mit state-of-the-art adversariellen Prompts, die verschiedene Angriffsmethoden repräsentieren.

### 2. JBB-Behaviors Datensatz
Enthält 100 verschiedene Missbrauchsverhaltensweisen, die in zehn Kategorien entsprechend den Nutzungsrichtlinien von OpenAI unterteilt sind.

### 3. Standardisierter Evaluierungsrahmen
Bietet klare Definitionen für Bedrohungsmodelle, System-Prompts und Bewertungsfunktionen.

### 4. Leaderboard
Eine Web-basierte Plattform zur Verfolgung der Leistung verschiedener Angriffe und Verteidigungen auf verschiedenen LLMs.

## Designprinzipien

- **Reproduzierbarkeit**: Vollständige Offenlegung von Jailbreak-Prompts und Artefakten
- **Erweiterbarkeit**: Unterstützung für neue Angriffe, Verteidigungen und LLMs
- **Zugänglichkeit**: Schnelle, leichtgewichtige und kostengünstige Pipeline

## Verwandte Seiten

- [[harmbench]]
- [[advbench]]
- [[robustbench]]
- [[jbb-behaviors]]
- [[gcg]]
- [[pair]]
- [[smoothllm]]
- [[perplexityfilter]]
- [[erase-and-check]]
- [[llama-3-70b-richter]]