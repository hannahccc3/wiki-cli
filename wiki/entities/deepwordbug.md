---
type: entity
title: "DeepWordBug"
tags: ["attack", "adversarial", "character-level", "NLP"]
related: [["adversarial-samples"], ["character-level-attacks"], ["rocket"], ["heuristic-rules"]]
sources: ["Chen 等 - 2022 - Why Should Adversarial Perturbations be Imperceptible Rethink the Research Paradigm in Adversarial.md"]
created: 2024-01-15
updated: 2024-01-15
---
# DeepWordBug

## Επισκόπηση

Το **DeepWordBug** είναι μια μέθοδος επίθεσης σε επίπεδο χαρακτήρα που προτάθηκε από τους Gao et al. (2018). Η μέθοδος δημιουργεί επιθετικά δείγματα με μικρές διαταραχές σε επίπεδο χαρακτήρων, συμπεριλαμβανομένων ανταλλαγών, διαγραφών και εισαγωγών.

## Χαρακτηριστικά

- **Τύπος Επίθεσης**: Character-level (επίπεδο χαρακτήρα)
- **Αποδοτικότητα**: Υψηλή - χαμηλός αριθμός ερωτημάτων
- **Διατήρηση Νοήματος**: Πολύ καλή - διατηρεί το επιθετικό νόημα

## Αποτελέσματα στο Advbench

| Dataset | ASR (%) (power=5) | ASR (%) (power=25) |
|---------|-------------------|---------------------|
| LUN | 0.1 | 0.2 |
| Amazon-LB | 9.3 | 12.4 |
| HSOL | 56.4 | 85.4 |
| EDENCE | 22.9 | 79.9 |

## Σύγκριση με ROCKET

Το DeepWordBug επιτυγχάνει καλή διατήρηση νοήματος αλλά η ROCKET υπερτερεί συνολικά σε:
- Ποσοστό επιτυχίας επίθεσης
- Αποδοτικότητα ερωτημάτων
- Πρακτικότητα για πραγματικούς επιτιθέμενους

## Σχετικές Σελίδες

- [[character-level-attacks]]
- [[adversarial-samples]]
- [[rocket]]
- [[heuristic-rules]]