---
type: entity
title: "Llama 2 7B"
tags: ["model", "LLM", "safety-tuned"]
related: ["llama-3-8b", "gemma-1.1-2b", "gemma-1.1-7b", "vicuna-1.5-7b", "gcg", "harmbench"]
sources: ["Geisler 等 - 2025 - REINFORCE Adversarial Attacks on Large Language Models An Adaptive, Distributional, and Semantic Ob.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Llama 2 7B

## Επισκόπηση

Το Llama 2 7B είναι ένα μοντέλο γλωσσικής μοντελοποίησης 7 δισεκατομμυρίων παραμέτρων από τη Meta. Αποτελεί μέρος της οικογένειας Llama 2 και έχει υποστεί εκπαίδευση ευθυγράμμισης (safety-tuning).

## Αποτελέσματα στην Εργασία

Το Llama 2 7B αξιολογήθηκε ως μοντέλο-στόχος στις επιθέσεις:

| Μέθοδος | ASR@512 |
|---------|---------|
| Affirmative GCG | 0.32 |
| REINFORCE-GCG | 0.56 |
| Affirmative PGD | 0.17 |
| REINFORCE-PGD | 0.22 |

Το REINFORCE objective **αύξησε σημαντικά** το ποσοστό επιτυχίας επίθεσης.

## Σχετικές Σελίδες

- [[llama-3-8b]] - Llama 3 8B
- [[gemma-1.1-2b]] - Gemma 1.1 2B
- [[gemma-1.1-7b]] - Gemma 1.1 7B
- [[vicuna-1.5-7b]] - Vicuna 1.5 7B
- [[gcg]] - Greedy Coordinate Gradient
- [[harmbench]] - HarmBench Benchmark