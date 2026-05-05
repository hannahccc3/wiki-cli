---
type: entity
title: "BERT-Attack"
tags: ["attack", "adversarial", "word-level", "NLP"]
related: [["adversarial-samples"], ["black-box-attack"], ["word-level-attacks"], ["rocket"], ["deepwordbug"]]
sources: ["Chen 等 - 2022 - Why Should Adversarial Perturbations be Imperceptible Rethink the Research Paradigm in Adversarial.md"]
created: 2024-01-15
updated: 2024-01-15
---
# BERT-Attack

## Επισκόπηση

Το **BERT-Attack** είναι μια μέθοδος επίθεσης που προτάθηκε από τους Li et al. (2020) για τη δημιουργία κειμενικών επιθετικών δειγμάτων χρησιμοποιώντας το ίδιο το μοντέλο BERT για την επίθεση. Η μέθοδος χρησιμοποιείται ως βασική γραμμή σύγκρισης στο Advbench.

## Χαρακτηριστικά

- **Τύπος Επίθεσης**: Word-level (επίπεδο λέξης)
- **Πρόσβαση**: Απαιτεί πρόσβαση σε confidence scores ή gradients
- **Αποδοτικότητα**: Χαμηλή - απαιτεί πολλα ερωτήματα (π.χ. 3966.60 μέσος όρος στο LUN)

## Αποτελέσματα στο Advbench

Σύμφωνα με τα πειράματα της εργασίας Chen et al. (2022):

| Dataset | ASR (%) | Queries |
|---------|---------|---------|
| LUN | 7.0 | 3966.60 |
| Amazon-LB | 43.0 | 1625.37 |
| HSOL | 56.8 | 139.14 |
| EDENCE | 90.3 | 140.98 |

## Κριτική

Οι συγγραφείς επισημαίνουν ότι το BERT-Attack, μαζί με άλλες word-level μεθόδους, σοβαρά καταστρέφει το αρχικό επιθετικό νόημα λόγω υποκατάστασης με ασυνήθιστες λέξεις. Επιπλέον, η υψηλή απαίτηση σε ερωτήματα την καθιστά μη πρακτική για πραγματικούς επιτιθέμενους.

## Σχετικές Σελίδες

- [[adversarial-samples]]
- [[word-level-attacks]]
- [[rocket]]
- [[deepwordbug]]
- [[textfooler]]