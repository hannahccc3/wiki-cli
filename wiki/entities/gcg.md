---
type: entity
title: "GCG (Greedy Coordinate Gradient)"
tags: ["Angriff", "Adversarial Machine Learning", "White-Box-Angriff", "Optimierung", "méthode d'attaque", "optimisation", "attaque par suffixe", "jailbreaking attack", "baseline", "white-box", "token-level", "algorithm", "adversarial attack", "jailbreaking", "attack-method", "Optimierungsbasiert", "method"]
related: ["jailbreakbench", "pair", "jailbreaking", "adversarial-attacken", "weisskasten-angriff", "pandora", "autodan", "deepinception", "tap", "piratage-llm", "rl-jack", "white-box-attack", "reinforce", "pgd", "harmbench", "llama-2-7b", "llama-3-8b", "gemma-1.1-2b", "gemma-1.1-7b", "vicuna-1.5-7b", "cold-attack", "white-box-attacks", "adversarial-suffix", "angriffs-erfolgsrate", "white-box-angriffe", "jailbreak-composition", "many-shot-jailbreaking"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md", "Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md", "Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md", "Geisler 等 - 2025 - REINFORCE Adversarial Attacks on Large Language Models An Adaptive", "Distributional", "and Semantic Ob.md", "Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md", "Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-15
updated: 2024-01-15
---
# GCG (Greedy Coordinate Gradient)

## Overview

Greedy Coordinate Gradient (GCG) is a white-box adversarial suffix optimization method for attacking large language models. It constructs adversarial suffixes designed to increase the likelihood of models producing harmful responses.

## Role in Research

### Composition with MSJ

The researchers explored composing Many-shot Jailbreaking with GCG:

- **Finding**: The effect depends on the number of shots
- **Zero-shot**: GCG suffix drastically increases probability of harmful responses
- **Longer contexts**: Much smaller effect when combined with many-shot demonstrations

### Technical Details

GCG works by:
1. Using gradient information to optimize attack strings
2. Finding token sequences that maximize probability of harmful completions
3. Being location-specific within attack strings

## Related Pages

- [[jailbreak-composition]]
- [[many-shot-jailbreaking]]
- [[white-box-attack]]
- [[adversarial-attacks]]