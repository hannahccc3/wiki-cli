---
type: entity
title: "Llama-3-8B-Instruct"
tags: ["model", "LLM", "meta", "instruct"]
related: ["lora", "safe-lora", "llama-2-7b-chat", "alignment-matrix"]
sources: ["Hsu 等 - 2024 - Safe LoRA the Silver Lining of Reducing Safety Risks when Fine-tuning Large Language Models.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Llama-3-8B-Instruct

## Επισκόπηση

Το **Llama-3-8B-Instruct** είναι ένα μοντέλο γλωσσικής κατανόησης της Meta που έχει βελτιστοποιηθεί για ακολουθία οδηγιών. Στην έρευνα Safe LoRA, χρησιμοποιείται ως παράδειγμα μοντέλου που απαιτεί περισσότερη προβολή.

## Αποτελέσματα με Safe LoRA

- **Απαιτούμενη προβολή**: ~35% των επιπέδων
- **Βαθμός επιβλαβότητας**: 1.10
- **MT-Bench Score**: 5.05
- **ASR**: 6.36%

## Παρατηρήσεις

Η ευθυγράμμιση του Llama-3 δεν είναι τόσο ισχυρή όσο του Llama-2, γι' αυτό απαιτείται προβολή περισσότερων επιπέδων.

## Σύνδεση με Άλλες Σελίδες

- [[safe-lora]]
- [[lora]]
- [[llama-2-7b-chat]]
- [[alignment-matrix]]
- [[parameter-efficient-fine-tuning]]
- [[harmfulness-score]]
- [[asr-attack-success-rate]]