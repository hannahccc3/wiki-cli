---
type: entity
title: "PAIR (Prompt Automatic Iterative Refinement)"
tags: ["Angriff", "Black-Box-Angriff", "LLM-Assistiert", "Automatisiert", "jailbreaking attack", "baseline", "in-context learning", "red-teaming", "adversarial", "Black-Box", "LLM-gestützt", "Jailbreaking"]
related: ["jailbreakbench", "gcg", "jailbreaking", "schwarzkasten-angriff", "mixtral", "rl-jack", "in-context-learning", "jailbreak-r1", "tap", "auto Dan-turbo", "gpo", "arrattack", "advprompter", "harmbench", "angriffs-erfolgsrate", "black-box-angriffe"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md", "Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md", "Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2024-12-10
updated: 2024-12-10
---
# PAIR (Prompt Automatic Iterative Refinement)

## Überblick

PAIR (Prompt Automatic Iterative Refinement) ist ein von Chao et al. (2023) entwickelter LLM-gestützter Jailbreaking-Angriff. Der Angriff nutzt ein Hilfs-LLM (standardmäßig Mixtral), um automatisch Jailbreak-Prompts zu generieren und zu verfeinern.

## Methode

Der Angriff verwendet:
- **Attacker-Modell**: Mixtral
- **Temperatur**: 1
- **Sampling**: top-p mit p = 0.9
- **Streams**: N = 30
- **Maximale Tiefe**: K = 3

## Evaluierungsergebnisse (JailbreakBench)

| Modell | Attack Success Rate | Ø Queries | Ø Tokens |
|--------|---------------------|-----------|----------|
| Vicuna | 69% | 34 | 12K |
| Llama-2 | 0% | 88 | 29K |
| GPT-3.5 | 71% | 30 | 9K |
| GPT-4 | 34% | 51 | 13K |

## Eigenschaften

- **Black-Box-Angriff**: Kein direkter Zugriff auf Modellparameter erforderlich
- **Query-effizient**: Verwendet durchschnittlich deutlich weniger Queries als GCG
- **Automatisiert**: Eliminiert die Notwendigkeit manueller Prompt-Konstruktion

## Verwandte Seiten

- [[jailbreakbench]]
- [[gcg]]
- [[jailbreaking]]
- [[angriffs-erfolgsrate]]
- [[black-box-angriffe]]