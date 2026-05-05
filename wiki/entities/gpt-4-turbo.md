---
type: entity
title: "GPT-4 Turbo"
tags: ["LLM", "OpenAI", "API", "safety-aligned"]
related: ["gpt-3.5-turbo", "gpt-4o", "claude-2.0", "openai", "jailbreaking"]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# GPT-4 Turbo

## Επισκόπηση

Το GPT-4 Turbo είναι ένα προηγμένο μοντέλο LLM από την OpenAI με βελτιωμένη κατανόηση και παραγωγή κειμένου. Αποτελεί κορυφαία επιλογή για απαιτητικές εφαρμογές.

## Αποτελέσματα Έρευνας

Παρά την ισχυρή ευθυγράμμιση ασφαλείας, η έρευνα κατάφερε να επιτύχει υψηλά ποσοστά επιτυχίας:

| Μέθοδος | ASR |
|---------|-----|
| PAIR | 33% |
| TAP | 36% |
| TAP (Transfer) | 59% |
| Prompt | 28% |
| **Prompt + RS + Self-Transfer** | **96%** |

## Σημείωση

Υπάρχει μη-ντετερμινιστική συμπεριφορά στα logprobs που επηρεάζει την αποτελεσματικότητα της τυχαίας αναζήτησης.

## Σχετικές Σελίδες

- [[openai]]
- [[gpt-3.5-turbo]]
- [[gpt-4o]]
- [[jailbreaking]]
- [[random-search]]
- [[self-transfer]]