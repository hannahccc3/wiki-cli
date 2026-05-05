---
type: source
title: "JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models"
authors: ["Patrick Chao", "Edoardo Debenedetti", "Alexander Robey", "Maksym Andriushchenko", "Francesco Croce", "Vikash Sehwag", "Edgar Dobriban", "Nicolas Flammarion", "George J. Pappas", "Florian Tramer", "Hamed Hassani", "Eric Wong"]
year: 2024
url: "https://jailbreakbench.github.io/"
venue: "arXiv preprint"
tags: ["Jailbreaking", "Große Sprachmodelle", "LLM-Sicherheit", "Robustheits-Benchmark", "Adversarial Machine Learning", "Robustheit", "Benchmark", "Red-Teaming", "LLM-Verteidigung", "KI-Sicherheit", "Adversarial-Angriffe", "Robustheitsbewertung", "Large Language Models", "Verteidigungsmechanismen", "Schädliche Inhalte Erkennung"]
related: ["jailbreaking", "jbb-behaviors", "gcg", "pair", "smoothllm", "perplexity-filter", "erase-and-check", "llama-3-70b", "llm", "jailbreakbench", "harmbench", "advbench", "robustbench", "perplexityfilter", "angriffs-erfolgsrate", "test-time-verteidigungen", "white-box-angriffe", "black-box-angriffe"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models

## Zusammenfassung

JailbreakBench ist ein Open-Source-Benchmark zur Standardisierung der Evaluierung von Jailbreak-Angriffen und Verteidigungen für Large Language Models (LLMs). Die Arbeit wurde 2024 von einem internationalen Forscherteam unter der Leitung von Patrick Chao, Edoardo Debenedetti und Alexander Robey veröffentlicht.

## Hauptbeiträge

### Repository von Jailbreak-Artefakten

Das Benchmark umfasst ein evolvierendes Repository von state-of-the-art adversariellen Prompts, die als Jailbreak-Artefakte bezeichnet werden. Diese Artefakte können über eine Python-Bibliothek einfach abgerufen werden:

```python
import jailbreakbench as jbb
artifact = jbb.read_artifact(method="PAIR", model_name="vicuna-13b-v1.5")
```

### JBB-Behaviors Datensatz

Der Datensatz enthält 100 schädliche Verhaltensweisen, die in zehn Kategorien entsprechend den Nutzungsrichtlinien von OpenAI unterteilt sind:
- 18% aus AdvBench
- 27% aus TDC/HarmBench
- 55% originäre Einträge

Zusätzlich wurden 100 gutartige Verhaltensweisen erstellt, die als Sanity Check für Ablehnungsraten dienen.

### Standardisiertes Evaluationsframework

Das Framework bietet:
- Definierte Bedrohungsmodelle
- System-Prompts
- Chat-Templates
- Bewertungsfunktionen
- Unterstützung für lokale und Cloud-basierte Abfragen

### JailbreakJudge-Auswahl

Llama-3-70B wurde als effektivster Jailbreak-Richter identifiziert mit:
- Über 90% Übereinstimmung mit menschlichen Annotatoren
- Niedrige False-Positive-Rate (11,6%)
- Niedrige False-Negative-Rate (5,5%)

## Hauptergebnisse

### Angriffsbewertung

| Angriff | Vicuna | Llama-2 | GPT-3.5 | GPT-4 |
|---------|--------|---------|---------|-------|
| PAIR | 69% | 0% | 71% | 34% |
| GCG | 80% | 3% | 47% | 4% |
| JB-Chat | 90% | 0% | 0% | 0% |
| Prompt mit RS | 89% | 90% | 93% | 78% |

### Verteidigungsbewertung

SmoothLLM und Erase-and-Check erwiesen sich als die solidesten Verteidigungsmechanismen.

## Designprinzipien

1. **Reproduzierbarkeit** – Vollständige Open-Source-Veröffentlichung
2. **Erweiterbarkeit** – Unterstützung für Schwarzkasten-, Weißkasten- und adaptive Angriffe
3. **Zugänglichkeit** – Schnelle, leichte und kostengünstige Pipeline

## Technische Details

- **Programmiersprache**: Python
- **Hosting**: GitHub (https://github.com/JailbreakBench/jailbreakbench)
- **Leaderboard**: https://jailbreakbench.github.io/

## Verwandte Seiten

- [[harmbench]] – HarmBench Benchmark
- [[advbench]] – AdvBench Datensatz
- [[robustbench]] – RobustBench Framework
- [[jailbreaking]] – Konzept: Jailbreaking
- [[gcg]] – GCG Angriff
- [[pair]] – PAIR Angriff
- [[smoothllm]] – SmoothLLM Verteidigung
- [[perplexity-filter]] – Perplexity Filter
- [[erase-and-check]] – Erase-and-Check
- [[llama-3-70b]] – Llama-3-70B Modell
- [[jbb-behaviors]] – JBB-Behaviors Datensatz
- [[jailbreak-judge]] – Jailbreak Judge Konzept
- [[red-teaming]] – Red-Teaming Konzept