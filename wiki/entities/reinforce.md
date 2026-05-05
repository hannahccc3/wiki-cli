---
type: entity
title: "REINFORCE"
tags: ["algorithm", "reinforcement learning", "policy gradient"]
related: ["policy-gradient", "value-function", "rloo-estimator", "gcg", "pgd", "jailbreaking", "adversarial-attacks"]
sources: ["Geisler 等 - 2025 - REINFORCE Adversarial Attacks on Large Language Models An Adaptive, Distributional, and Semantic Ob.md"]
created: 2025-01-01
updated: 2025-01-01
---
# REINFORCE

## Επισκόπηση

Ο REINFORCE είναι ένας αλγόριθμος βελτιστοποίησης **policy-gradient** που χρησιμοποιεί την κλίση της συνάρτησης αξίας για τη μεγιστοποίηση της αναμενόμενης ανταμοιβής. Αναπτύχθηκε από τον Ronald Williams (1992) και αποτελεί τη βάση για την προτεινόμενη μέθοδο επίθεσης.

## Εφαρμογή σε LLMs

Στην εργασία Geisler et al. (2025), ο REINFORCE χρησιμοποιείται για:
- Μεγιστοποίηση της πιθανότητας επιβλαβών αποκρίσεων
- Προσαρμοστική βελτιστοποίηση στο μοντέλο-στόχο
- Εκμετάλλευση της κατανομικής φύσης των αποκρίσεων

## Μαθηματική Θεμελίωση

Η κλίση πολιτικής υπολογίζεται ως:

∇_x̃ E[y~P_fθ(Y|X=x̃)] [Reward(y, x̃)] ∝ E[y~P_fθ(Y|X=x̃)] [Reward(y, x̃) ∇_x̃ log P_fθ(y|x̃)]

## REINFORCE-GCG και REINFORCE-PGD

Η μέθοδος REINFORCE ενσωματώθηκε στους αλγορίθμους:
- [[gcg]] - REINFORCE-GCG
- [[pgd]] - REINFORCE-PGD

## Σχετικές Σελίδες

- [[policy-gradient]] - Policy Gradient Methods
- [[value-function]] - Value Function
- [[rloo-estimator]] - RLOO Estimator
- [[jailbreaking]] - Jailbreaking Attacks
- [[adversarial-attacks]] - Adversarial Attacks