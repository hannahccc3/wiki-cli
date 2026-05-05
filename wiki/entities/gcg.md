---
type: entity
title: "GCG (Greedy Coordinate Gradient)"
tags: ["Angriff", "Adversarial Machine Learning", "White-Box-Angriff", "Optimierung", "méthode d'attaque", "optimisation", "attaque par suffixe", "jailbreaking attack", "baseline", "white-box", "token-level", "algorithm", "adversarial attack", "jailbreaking", "attack-method", "Optimierungsbasiert"]
related: ["jailbreakbench", "pair", "jailbreaking", "adversarial-attacken", "weisskasten-angriff", "pandora", "autodan", "deepinception", "tap", "piratage-llm", "rl-jack", "white-box-attack", "reinforce", "pgd", "harmbench", "llama-2-7b", "llama-3-8b", "gemma-1.1-2b", "gemma-1.1-7b", "vicuna-1.5-7b", "cold-attack", "white-box-attacks", "adversarial-suffix", "angriffs-erfolgsrate", "white-box-angriffe"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md", "Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md", "Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md", "Geisler 等 - 2025 - REINFORCE Adversarial Attacks on Large Language Models An Adaptive", "Distributional", "and Semantic Ob.md", "Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md"]
created: 2024-12-10
updated: 2024-12-10
---
# GCG (Greedy Coordinate Gradient)

## Überblick

GCG (Greedy Coordinate Gradient) ist ein optimierungsbasierter Jailbreaking-Angriff, der von Zou et al. (2023) entwickelt wurde. Der Angriff verwendet Gradienten-basierte diskrete Optimierung, um adversarielle Suffixe zu generieren, die LLMs dazu bringen, schädliche Inhalte zu generieren.

## Methode

Der Angriff optimiert einen einzelnen adversariellen Suffix für jedes Verhaltensziel mit folgenden Standard-Hyperparametern:
- Batch-Größe: 512
- Optimierungsschritte: 500

## Evaluierungsergebnisse (JailbreakBench)

| Modell | Attack Success Rate |
|--------|---------------------|
| Vicuna | 80% |
| Llama-2 | 3% |
| GPT-3.5 | 47% |
| GPT-4 | 4% |

## Eigenschaften

- **White-Box-Angriff**: Erfordert Zugriff auf Modellparameter
- **Hoher Rechenaufwand**: Durchschnittlich 256K Queries und 17M Tokens
- **Transfer-fähig**: Suffixe können auf geschlossene Modelle übertragen werden

## Verwandte Seiten

- [[jailbreakbench]]
- [[pair]]
- [[jailbreaking]]
- [[angriffs-erfolgsrate]]
- [[white-box-angriffe]]