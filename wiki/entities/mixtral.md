---
type: entity
title: "Mixtral"
tags: ["LLM", "Mixture of Experts", "Open-Source"]
related: ["jailbreakbench", "pair", "vicuna", "llama-2"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# Mixtral

## Überblick

Mixtral of Experts ist ein Mischung-von-Experten-Sprachmodell, entwickelt von Jiang et al. (2024). In JailbreakBench wird Mixtral als Standard-Attacker-Modell für den PAIR-Angriff verwendet.

## Verwendung in PAIR

Der PAIR-Angriff nutzt Mixtral mit folgenden Parametern:
- Temperatur: 1
- Top-p Sampling: p = 0.9
- Streams: N = 30
- Maximale Tiefe: K = 3

## Verwandte Seiten

- [[jailbreakbench]]
- [[pair]]
- [[vicuna]]
- [[llama-2]]