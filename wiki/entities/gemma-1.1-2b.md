---
type: entity
title: "Gemma 1.1 2B"
tags: ["model", "LLM", "safety-tuned"]
related: ["gemma-1.1-7b", "llama-2-7b", "llama-3-8b", "vicuna-1.5-7b", "gcg", "pgd", "harmbench"]
sources: ["Geisler 等 - 2025 - REINFORCE Adversarial Attacks on Large Language Models An Adaptive, Distributional, and Semantic Ob.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Gemma 1.1 2B

## Επισκόπηση

Το Gemma 1.1 2B είναι ένα μικρό μοντέλο γλωσσικής μοντελοποίησης 2 δισεκατομμυρίων παραμέτρων από τη Google DeepMind. Αποτελεί μέρος της οικογένειας Gemma.

## Αποτελέσματα στην Εργασία

| Μέθοδος | ASR@512 |
|---------|---------|
| Affirmative GCG | 0.57 |
| REINFORCE-GCG | 0.88 |
| Affirmative PGD | 0.56 |
| REINFORCE-PGD | 0.82 |

Το REINFORCE objective επιτυγχάνει **πολύ υψηλότερα** ποσοστά επιτυχίας.

## Σχετικές Σελίδες

- [[gemma-1.1-7b]] - Gemma 1.1 7B
- [[llama-2-7b]] - Llama 2 7B
- [[llama-3-8b]] - Llama 3 8B
- [[gcg]] - Greedy Coordinate Gradient
- [[pgd]] - Projected Gradient Descent
- [[harmbench]] - HarmBench Benchmark