---
type: entity
title: "SememePSO"
tags: ["attack", "adversarial", "word-level", "NLP"]
related: [["adversarial-samples"], ["word-level-attacks"], ["rocket"]]
sources: ["Chen 等 - 2022 - Why Should Adversarial Perturbations be Imperceptible Rethink the Research Paradigm in Adversarial.md"]
created: 2024-01-15
updated: 2024-01-15
---
# SememePSO

## Επισκόπηση

Το **SememePSO** είναι μια μέθοδος επίθεσης που βασίζεται σε Particle Swarm Optimization (PSO) με χρήση σημασιολογικών πόρων (sememes) για την υποκατάσταση λέξεων. Προτάθηκε από τους Zang et al. (2020).

## Αποτελέσματα στο Advbench

| Dataset | ASR (%) (maxiter=100) | Queries |
|---------|----------------------|---------|
| LUN | 0.9 | 2020.85 |
| Amazon-LB | 23.8 | 1627.97 |
| HSOL | 66.9 | 233.11 |
| EDENCE | 79.6 | 231.17 |

## Κριτική

Η μέθοδος απαιτεί εξωτερικές γνωσιακές βάσεις και είναι αναποτελεσματική, καθιστώντας την μη πρακτική για πραγματικούς επιτιθέμενους.

## Σχετικές Σελίδες

- [[word-level-attacks]]
- [[adversarial-samples]]
- [[rocket]]