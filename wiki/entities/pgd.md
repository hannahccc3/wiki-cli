---
type: entity
title: "Projected Gradient Descent (PGD)"
tags: ["algorithm", "adversarial attack", "jailbreaking"]
related: ["reinforce", "gcg", "jailbreaking", "harmbench", "llama-2-7b", "llama-3-8b", "gemma-1.1-2b", "gemma-1.1-7b", "vicuna-1.5-7b"]
sources: ["Geisler 等 - 2025 - REINFORCE Adversarial Attacks on Large Language Models An Adaptive, Distributional, and Semantic Ob.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Projected Gradient Descent (PGD)

## Επισκόπηση

Ο Projected Gradient Descent (PGD) είναι ένας αλγόριθμος βελτιστοποίησης βασισμένος σε κλίση για επιθέσεις jailbreaking σε LLMs. Αναπτύχθηκε από τους Geisler et al. (2024) και αποτελεί μία από τις κύριες μεθόδους που χρησιμοποιούνται σε αυτήν την εργασία.

## Λειτουργία

Ο PGD χρησιμοποιεί:
- **Adam Optimizer** για την ενημέρωση των παραμέτρων
- **Entropy Projection** για τον έλεγχο της τυχαιότητας
- **Cosine Annealing with Warm Restarts** για το learning rate
- **Batch Processing** για παράλληλη επίθεση σε πολλαπλά prompts

## REINFORCE-PGD

Η ενσωμάτωση του REINFORCE objective στον PGD οδηγεί σε σημαντικές βελτιώσεις:

| Μοντέλο | Affirmative PGD ASR@512 | REINFORCE-PGD ASR@512 |
|---------|-------------------------|------------------------|
| Llama 3 8B | 0.57 | 0.69 |
| Gemma 1.1 7B | 0.54 | 0.84 |
| Vicuna 1.5 7B | 0.87 | 0.94 |

## Σχετικές Σελίδες

- [[reinforce]] - REINFORCE Algorithm
- [[gcg]] - Greedy Coordinate Gradient
- [[jailbreaking]] - Jailbreaking Attacks
- [[harmbench]] - HarmBench Benchmark
- [[policy-gradient]] - Policy Gradient Methods