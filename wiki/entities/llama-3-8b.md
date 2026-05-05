---
type: entity
title: "Llama 3 8B"
tags: ["model", "LLM", "safety-tuned"]
related: ["llama-2-7b", "gemma-1.1-2b", "gemma-1.1-7b", "vicuna-1.5-7b", "gcg", "pgd", "harmbench", "circuit-breaker-defense"]
sources: ["Geisler 等 - 2025 - REINFORCE Adversarial Attacks on Large Language Models An Adaptive, Distributional, and Semantic Ob.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Llama 3 8B

## Επισκόπηση

Το Llama 3 8B είναι ένα μοντέλο γλωσσικής μοντελοποίησης 8 δισεκατομμυρίων παραμέτρων από τη Meta. Αποτελεί μέρος της οικογένειας Llama 3 και διαθέτει ενισχυμένες δυνατότητες ευθυγράμμισης.

## Αποτελέσματα στην Εργασία

Το Llama 3 8B ήταν ένα από τα κύρια μοντέλα-στόχοι:

| Μέθοδος | ASR@512 |
|---------|---------|
| Affirmative GCG | 0.35 |
| REINFORCE-GCG | 0.73 |
| Affirmative PGD | 0.57 |
| REINFORCE-PGD | 0.69 |

Το REINFORCE objective **διπλασίασε** το ASR σε σύγκριση με το affirmative objective.

## Circuit Breaker Defense

Το Llama 3 8B με Circuit Breaker Defense αξιολογήθηκε επίσης:

| Μέθοδος | ASR@512 |
|---------|---------|
| Affirmative GCG | 0.02 |
| REINFORCE-GCG | 0.23 |
| REINFORCE-GCG (βελτιστοποιημένο seed) | 0.50 |

## Σχετικές Σελίδες

- [[llama-2-7b]] - Llama 2 7B
- [[gemma-1.1-2b]] - Gemma 1.1 2B
- [[gemma-1.1-7b]] - Gemma 1.1 7B
- [[vicuna-1.5-7b]] - Vicuna 1.5 7B
- [[gcg]] - Greedy Coordinate Gradient
- [[pgd]] - Projected Gradient Descent
- [[harmbench]] - HarmBench Benchmark
- [[circuit-breaker-defense]] - Circuit Breaker Defense