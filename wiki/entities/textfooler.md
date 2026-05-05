---
type: entity
title: "TextFooler"
tags: ["attack", "adversarial", "word-level", "NLP"]
related: [["adversarial-samples"], ["word-level-attacks"], ["rocket"], ["pwws"]]
sources: ["Chen 等 - 2022 - Why Should Adversarial Perturbations be Imperceptible Rethink the Research Paradigm in Adversarial.md"]
created: 2024-01-15
updated: 2024-01-15
---
# TextFooler

## Επισκόπηση

Το **TextFooler** είναι μια ευρέως χρησιμοποιούμενη μέθοδος επίθεσης σε επίπεδο λέξης που προτάθηκε από τους Jin et al. (2020). Η μέθοδος χρησιμοποιείται ως βασική γραμμή σύγκρισης στο Advbench.

## Αποτελέσματα στο Advbench

| Dataset | ASR (%) | Queries |
|---------|---------|---------|
| LUN | 0.4 | 1294.38 |
| Amazon-LB | 9.0 | 740.42 |
| HSOL | 10.4 | 78.46 |
| SpamAssassin | 0.2 | 961.88 |

## Κριτική

Σύμφωνα με την εργασία Chen et al. (2022), το TextFooler παρουσιάζει:
- Χαμηλή αποδοτικότητα (υψηλός αριθμός ερωτημάτων)
- Χαμηλό ποσοστό επιτυχίας σε πολλές ασφαλιστικές εργασίες
- Μη πρακτικό για πραγματικούς επιτιθέμενους

## Σχετικές Σελίδες

- [[word-level-attacks]]
- [[adversarial-samples]]
- [[rocket]]
- [[pwws]]