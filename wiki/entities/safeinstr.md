---
type: entity
title: "SafeInstr"
tags: ["method", "safety", "fine-tuning", "baseline"]
related: ["safe-lora", "bea-backdoor-enhanced-alignment", "safety-alignment"]
sources: ["Hsu 等 - 2024 - Safe LoRA the Silver Lining of Reducing Safety Risks when Fine-tuning Large Language Models.md"]
created: 2024-01-15
updated: 2024-01-15
---
# SafeInstr

## Επισκόπηση

Το **SafeInstr** είναι μια μέθοδος βασικής γραμμής για τη διατήρηση της ασφάλειας κατά το fine-tuning. Η μέθοδος προσθέτει δείγματα ασφαλείας (3-10%) στο σύνολο δεδομένων fine-tuning.

## Σύγκριση με Safe LoRA

| Μέθοδος | Απαιτεί επιπλέον δεδομένα | Αποτελεσματικότητα |
|---------|---------------------------|---------------------|
| SafeInstr | Ναι (10% δείγματα ασφαλείας) | Μέτρια |
| Safe LoRA | Όχι | Υψηλή |

## Μειονεκτήματα

- Απαιτεί επιπλέον δεδομένα εκπαίδευσης
- Λιγότερο αποτελεσματικό σε μεγάλα σύνολα δεδομένων όπως το Alpaca

## Σύνδεση με Άλλες Σελίδες

- [[safe-lora]]
- [[bea-backdoor-enhanced-alignment]]
- [[safety-alignment]]