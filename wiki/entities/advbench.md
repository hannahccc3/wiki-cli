---
type: entity
title: "AdvBench"
tags: ["dataset", "security", "adversarial", "benchmark", "évaluation", "sécurité LLM", "Datensatz", "Schädliche Verhaltensweisen", "Jailbreaking"]
related: ["["rocket", "pandora", "gcg", "autodan", "jailbreakbench", "piratage-llm", "cold-attack", "jailbreaking", "attack-success-rate", "harmful-content", "harmbench", "jbb-behaviors"]
sources: ["Chen 等 - 2022 - Why Should Adversarial Perturbations be Imperceptible Rethink the Research Paradigm in Adversarial.md", "Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md", "Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md", "Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# AdvBench

## Überblick

AdvBench ist ein Datensatz mit schädlichen Verhaltensweisen, der von Zou et al. (2023) im Rahmen der Arbeit "Universal and Transferable Adversarial Attacks on Aligned Language Models" entwickelt wurde. Der Datensatz dient als Quelle für den JBB-Behaviors-Datensatz in JailbreakBench.

## Zusammensetzung

18% der Verhaltensweisen im JBB-Behaviors-Datensatz stammen aus AdvBench. Der Datensatz enthält typische schädliche Anfragen, die LLMs dazu bringen sollen, anstößige Inhalte zu generieren.

## Verbindung zu JailbreakBench

AdvBench stellt eine der Hauptquellen für die schädlichen Verhaltensweisen im JBB-Behaviors-Datensatz dar und ermöglicht so Vergleiche mit früheren Forschungsarbeiten.

## Verwandte Seiten

- [[jailbreakbench]]
- [[harmbench]]
- [[jbb-behaviors]]
- [[jailbreaking]]