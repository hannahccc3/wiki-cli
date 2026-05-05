---
type: source
title: "JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models"
authors: ["Patrick Chao", "Edoardo Debenedetti", "Alexander Robey", "Maksym Andriushchenko", "Francesco Croce", "Vikash Sehwag", "Edgar Dobriban", "Nicolas Flammarion", "George J. Pappas", "Florian Tramer", "Hamed Hassani", "Eric Wong"]
year: 2024
url: "https://jailbreakbench.github.io/"
venue: "arXiv preprint"
tags: ["Jailbreaking", "Große Sprachmodelle", "LLM-Sicherheit", "Robustheits-Benchmark", "Adversarial Machine Learning", "Robustheit", "Benchmark", "Red-Teaming", "LLM-Verteidigung", "KI-Sicherheit"]
related: ["jailbreaking", "jbb-behaviors", "gcg", "pair", "smoothllm", "perplexity-filter", "erase-and-check", "llama-3-70b", "llm", "jailbreakbench", "harmbench", "advbench", "robustbench", "perplexityfilter", "angriffs-erfolgsrate", "test-time-verteidigungen", "white-box-angriffe", "black-box-angriffe"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models

## Zusammenfassung

JailbreakBench ist ein Open-Source-Benchmark zur Standardisierung der Bewertung von Jailbreaking-Angriffen und -Verteidigungen bei großen Sprachmodellen (LLMs). Die Arbeit adressiert drei Hauptprobleme in der Jailbreaking-Forschung: fehlende Evaluierungsstandards, unvergleichbare Kosten- und Erfolgsraten sowie fehlende Reproduzierbarkeit.

## Hauptbeiträge

### 1. Repository von Jailbreak-Artefakten
Das Benchmark enthält ein evolvierendes Repository von state-of-the-art adversariellen Prompts, einschließlich der Angriffe GCG, PAIR, JailbreakChat und Prompt with Random Search.

### 2. JBB-Behaviors Datensatz
Ein Datensatz mit 100 schädlichen und harmlosen Verhaltensweisen zur Bewertung von Jailbreaking, inspiriert von und beitragend zu HarmBench und AdvBench.

### 3. Standardisierter Evaluierungsrahmen
Ein reproduzierbarer Framework mit klar definiertem Bedrohungsmodell, System-Prompts, Chat-Templates und Bewertungsfunktionen.

### 4. JailbreakBench Leaderboard
Eine Website unter https://jailbreakbench.github.io/ zur Verfolgung der Leistung von Angriffen und Verteidigungen.

## Auswahl des Jailbreak-Richters

Die Autoren verglichen sechs verschiedene Klassifikatoren zur Bewertung von Jailbreaking-Erfolgen:
- Rule-based Judge
- GPT-4
- HarmBench (Llama-2-13B)
- Llama Guard
- Llama Guard 2
- **Llama-3-70B** (ausgewählt als effektivster Richter mit über 90% Übereinstimmung mit menschlichen Annotatoren)

## Evaluierungsergebnisse

### Angriffsergebnisse (Attack Success Rate)
| Angriff | Vicuna | Llama-2 | GPT-3.5 | GPT-4 |
|---------|--------|---------|---------|-------|
| PAIR | 69% | 0% | 71% | 34% |
| GCG | 80% | 3% | 47% | 4% |
| JB-Chat | 90% | 0% | 0% | 0% |
| Prompt with RS | 89% | 90% | 93% | 78% |

### Verteidigungsergebnisse
Erase-and-Check erweist sich als solideste Verteidigung, obwohl Prompt with RS weiterhin erhebliche Erfolgsraten erzielt.

## Ethische Überlegungen

Die Autoren argumentieren, dass die Veröffentlichung von Jailbreak-Artefakten zur Entwicklung von adverserialem Training beitragen und LLMs sicherer machen kann. Der Großteil des Codes für Jailbreaking-Angriffe ist bereits Open-Source.

## Verwandte Seiten

- [[jailbreakbench]]
- [[harmbench]]
- [[advbench]]
- [[robustbench]]
- [[jbb-behaviors]]
- [[gcg]]
- [[pair]]
- [[smoothllm]]
- [[perplexityfilter]]
- [[erase-and-check]]