---
type: entity
title: "TAP"
tags: ["méthode d'attaque", "arbre de pensées", "génération automatique", "baseline", "red-teaming", "tree-of-attacks"]
related: ["pandora", "gcg", "autodan", "deepinception", "piratage-llm", "jailbreak-r1", "pair", "auto Dan-turbo", "gpo", "arrattack", "advprompter", "harmbench"]
sources: ["Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md", "Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2025-01-15
updated: 2025-01-15
---
# TAP (Tree of Attacks)

## Overview

**TAP** (Tree of Attacks) is a baseline method for automated red teaming, proposed by Mehrotra et al. (2024). It uses a tree structure to explore jailbreak attacks.

## Performance in JAILBREAK-R1 Paper

| Target Model | ASR | Diversity |
|--------------|-----|-----------|
| GPT-3.5 | 52.00% | 0.730 |
| GPT-4o | 37.50% | 0.796 |
| Claude-3.5 | 21.00% | 0.781 |
| Gemini-2.0 | 26.00% | 0.788 |
| Llama-2-7B | 39.00% | 0.784 |
| Llama3-8B | 36.00% | 0.800 |
| Qwen2.5-7B | 72.50% | 0.797 |
| Vicuna-7B | 82.00% | 0.763 |

**Average**: ASR 45.63%, Diversity 0.779

## Jailbreak Efficiency

- Average attempts per successful jailbreak: 2.42

## Comparison with JAILBREAK-R1

- JAILBREAK-R1 outperforms TAP by 19.56% in average ASR
- JAILBREAK-R1 diversity is 0.191 higher (0.970 vs 0.779)

## Related Pages

- [[jailbreak-r1]] - Proposed method
- [[pair]] - Another baseline
- [[auto Dan-turbo]] - Strong baseline
- [[harmbench]] - Evaluation benchmark