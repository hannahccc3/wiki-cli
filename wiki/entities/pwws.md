---
type: entity
title: "PWWS (Probability Weighted Word Substitution)"
tags: ["attack", "adversarial", "word-level", "NLP"]
related: [["adversarial-samples"], ["word-level-attacks"], ["rocket"], ["textfooler"]]
sources: ["Chen 等 - 2022 - Why Should Adversarial Perturbations be Imperceptible Rethink the Research Paradigm in Adversarial.md"]
created: 2024-01-15
updated: 2024-01-15
---
# PWWS (Probability Weighted Word Substitution)

## Επισκόπηση

Το **PWWS** είναι μια μέθοδος επίθεσης σε επίπεδο λέξης που προτάθηκε από τους Ren et al. (2019). Η μέθοδος χρησιμοποιεί στρατηγικές υποκατάστασης λέξεων βασισμένες σε πιθανότητες.

## Αποτελέσματα στο Advbench

| Dataset | ASR (%) | Queries |
|---------|---------|---------|
| LUN | 1.3 | 1707.19 |
| Amazon-LB | 18.8 | 1019.91 |
| HSOL | 9.9 | 107.23 |
| EDENCE | 46.0 | 129.68 |

## Κριτική

Σύμφωνα με την εργασία Chen et al. (2022), η PWWS απαιτεί πολλά ερωτήματα και δεν είναι αποδοτική για πραγματικές επιθέσεις. Επιπλέον, αποτυγχάνει σε πολλές ασφαλιστικές εργασίες.

## Σχετικές Σελίδες

- [[word-level-attacks]]
- [[adversarial-samples]]
- [[rocket]]
- [[textfooler]]