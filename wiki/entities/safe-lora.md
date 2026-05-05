---
type: entity
title: "Safe LoRA"
tags: ["method", "tool", "safety", "fine-tuning", "LLM"]
related: ["lora", "safety-alignment", "alignment-matrix", "projection-operator", "llama-2-7b-chat", "llama-3-8b-instruct", "parameter-efficient-fine-tuning", "purebad-dataset", "dialog-summary-dataset", "alpaca-dataset"]
sources: ["Hsu 等 - 2024 - Safe LoRA the Silver Lining of Reducing Safety Risks when Fine-tuning Large Language Models.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Safe LoRA

## Επισκόπηση

Το **Safe LoRA** είναι μια μέθοδος που προβάλλει τα βάρη LoRA σε έναν χώρο ευθυγράμμισης ασφαλείας για να αποτρέψει την υποβάθμιση της ασφάλειας κατά το fine-tuning μεγάλων γλωσσικών μοντέλων (LLMs). Η μέθοδος αυτή δεν απαιτεί επιπλέον δεδομένα εκπαίδευσης ή εκπαιδευτική διαδικασία.

## Βασικά Χαρακτηριστικά

- **Εκπαίδευση-ελεύθερη (Training-free)**: Δεν απαιτεί επιπλέον δεδομένα εκπαίδευσης
- **Χωρίς δεδομένα (Data-free)**: Απαιτεί μόνο τις γνώσεις βαρών από τα βασικά και ευθυγραμμισμένα μοντέλα
- **Μέθοδος αιχμής (One-liner patch)**: Απλή τροποποίηση στην αρχική υλοποίηση LoRA

## Πώς Λειτουργεί

1. Υπολογίζεται ο **πίνακας ευθυγράμμισης** V = W_aligned - W_unaligned
2. Για κάθε επίπεδο του LLM όπου χρησιμοποιείται LoRA, υπολογίζεται ο **τελεστής προβολής** C
3. Υπολογίζεται η ομοιότητα μεταξύ των αρχικών και προβεβλημένων βαρών LoRA
4. Αν η ομοιότητα είναι κάτω από ένα κατώφλι τ, τα βάρη προβάλλονται

## Αποτελέσματα

- Για **Llama-2-7B-Chat**: Απαιτείται προβολή ~11% των επιπέδων
- Για **Llama-3-8B-Instruct**: Απαιτείται προβολή ~35% των επιπέδων
- Υπερτερεί των μεθόδων SafeInstr και BEA στην ισορροπία ασφάλειας και χρηστικότητας

## Σύνδεση με Άλλες Σελίδες

- [[lora]]
- [[safety-alignment]]
- [[alignment-matrix]]
- [[projection-operator]]
- [[parameter-efficient-fine-tuning]]
- [[llama-2-7b-chat]]
- [[llama-3-8b-instruct]]
- [[purebad-dataset]]
- [[dialog-summary-dataset]]
- [[alpaca-dataset]]
- [[asr-attack-success-rate]]
- [[harmfulness-score]]