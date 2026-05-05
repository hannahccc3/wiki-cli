---
type: entity
title: "BEA (Backdoor Enhanced Alignment)"
tags: ["method", "safety", "fine-tuning", "baseline", "backdoor"]
related: ["safe-lora", "safeinstr", "safety-alignment"]
sources: ["Hsu 等 - 2024 - Safe LoRA the Silver Lining of Reducing Safety Risks when Fine-tuning Large Language Models.md"]
created: 2024-01-15
updated: 2024-01-15
---
# BEA (Backdoor Enhanced Alignment)

## Επισκόπηση

Το **BEA (Backdoor Enhanced Alignment)** είναι μια μέθοδος βασικής γραμμής που χρησιμοποιεί backdoor triggers ως μυστικές εντολές για την ενεργοποίηση κανόνων ασφαλείας.

## Τεχνικές Λεπτομέρειες

- Χρησιμοποιεί ζεύγη triggers ως secret prompts
- Κατά τη συμπερίληψη του trigger και επιβλαβών οδηγιών, η επίδραση μετριάζεται
- Απαιτεί 10% δείγματα backdoor στο σύνολο εκπαίδευσης

## Μειονεκτήματα

- Απαιτεί επιπλέον δεδομένα εκπαίδευσης
- Λιγότερο αποτελεσματικό σε μεγάλα σύνολα δεδομένων
- Χειρότερη απόδοση σε ορισμένες περιπτώσεις σε σχέση με την καθόλου άμυνα

## Σύνδεση με Άλλες Σελίδες

- [[safe-lora]]
- [[safeinstr]]
- [[safety-alignment]]