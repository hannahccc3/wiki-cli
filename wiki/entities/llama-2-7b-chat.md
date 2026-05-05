---
type: entity
title: "Llama-2-7B-Chat"
tags: ["target-model", "open-source", "meta", "model", "LLM", "chatbot"]
related: ["llama-3-8b-chat", "vicuna-7b", "qwen-2.5-7b-instruct", "gpt-3.5", "gpt-4o", "claude-3.5-sonnet", "gemini-2.0-flash", "harmbench", "jailbreak-r1", "lora", "safe-lora", "llama-3-8b-instruct", "alignment-matrix"]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md", "Hsu 等 - 2024 - Safe LoRA the Silver Lining of Reducing Safety Risks when Fine-tuning Large Language Models.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Llama-2-7B-Chat

## Επισκόπηση

Το **Llama-2-7B-Chat** είναι ένα μοντέλο γλωσσικής κατανόησης της Meta που έχει εκπαιδευτεί για συνομιλιακή χρήση. Στην έρευνα Safe LoRA, χρησιμοποιείται ως παράδειγμα ευθυγραμμισμένου μοντέλου.

## Αποτελέσματα με Safe LoRA

- **Απαιτούμενη προβολή**: ~11% των επιπέδων
- **Βαθμός επιβλαβότητας**: 1.055 (χαμηλότερος από το αρχικό μοντέλο)
- **MT-Bench Score**: 6.34 (υψηλότερος από το αρχικό μοντέλο)
- **ASR**: 3.03%

## Σύνδεση με Άλλες Σελίδες

- [[safe-lora]]
- [[lora]]
- [[llama-3-8b-instruct]]
- [[alignment-matrix]]
- [[parameter-efficient-fine-tuning]]
- [[harmfulness-score]]
- [[asr-attack-success-rate]]