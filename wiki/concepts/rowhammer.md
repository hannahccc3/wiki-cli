---
type: concept
title: "Rowhammer"
tags: ["Hardware_security", "Fault_injection", "DRAM", "GPU_security", "Memory_vulnerabilities"]
related: ["bit-flip-attack", "prlsonbreak-attack", "gddr6", "hardware-aware-search", "dram-disturbance"]
sources: ["Coalson 等 - 2025 - PrisonBreak Jailbreaking Large Language Models with at Most Twenty-Five Targeted Bit-flips.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Rowhammer

## Ορισμός

Το **Rowhammer** είναι μια τεχνική έγχυσης σφαλμάτων λογισμικού που εκμεταλλεύεται σφάλματα διαταραχής DRAM. Προκαλεί bit-flips στη μνήμη μέσω επαναλαμβανόμενης προσπέλασης σε γειτονικές σειρές DRAM.

## Μηχανισμός Λειτουργίας

1. **Επαναλαμβανόμενη προσπέλαση**: Πολλαπλές προσπελάσεις σε γειτονικές σειρές (aggressors)
2. **Διαρροή φορτίου**: Επιτάχυνση διαρροής φορτίου σε παρακείμενες σειρές
3. **Bit-flip**: Αναστροφή bits στις επηρεαζόμενες σειρές

## Εφαρμογές σε GPU

### GDDR6 DRAM
Η εργασία PRISONBREAK εστιάζει σε:
- **NVIDIA A6000 GPU** με GDDR6 μνήμη
- **MLaaS περιβάλλοντα**: Κοινόχρηστες GPU
- **RMM (RAPIDS Memory Manager)**: Διαχείριση μνήμης CUDA

### Διαφορές CPU vs GPU
| Χαρακτηριστικό | CPU (DDR4/LPDDR4) | GPU (GDDR6) |
|----------------|-------------------|-------------|
| Ευπάθεια | ~10^5× πιο ευάλωτη | Λιγότερο ευάλωτη |
| Flippable bits | Πολύ περισσότερα | Έως 10^5× λιγότερα |

## Τεχνικές Εκμετάλλευσης

### Memory Templating
Αντιστοίχιση λογικών διευθύνσεων με φυσικές θέσεις μνήμης.

### Memory Massaging
Τοποθέτηση στόχων βαρών σε επιθυμητές φυσικές θέσεις.

### Target Row Refresh (TRR) Bypass
Τεχνικές παράκαμψης της ενσωματωμένης προστασίας.

## Αποτελέσματα PRISONBREAK

- **69-91% ASR** σε 5 μοντέλα
- Μόνο **2 φυσικές θέσεις bit** απαιτούνται
- Παρά τις ~10^5× λιγότερες ευάλωτες θέσεις από prior work

## Σχετικές Σελίδες

- [[bit-flip-attack]] - Επίθεση αναστροφής bit
- [[prlsonbreak-attack]] - Η επίθεση PRISONBREAK
- [[hardware-aware-search]] - Αναζήτηση με γνώση υλικού
- [[gddr6]] - Τύπος μνήμης GDDR6
- [[fault-injection]] - Έγχυση σφαλμάτων