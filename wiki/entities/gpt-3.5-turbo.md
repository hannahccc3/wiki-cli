---
type: entity
title: "GPT-3.5 Turbo"
tags: ["LLM", "OpenAI", "API", "safety-aligned"]
related: ["gpt-4o", "gpt-4-turbo", "claude-2.0", "openai", "jailbreaking"]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# GPT-3.5 Turbo

## Επισκόπηση

Το GPT-3.5 Turbo είναι ένα μοντέλο LLM από την OpenAI, γνωστό για την ισορροπία μεταξύ κόστους και απόδοσης. Είναι ευρέως χρησιμοποιούμενο σε εφαρμογές παραγωγής.

## Αποτελέσματα Έρευνας

Το μοντέλο αποδείχθηκε ιδιαίτερα ευάλωτο σε χειροκίνητα σχεδιασμένες προτροπές:

| Μέθοδος | ASR |
|---------|-----|
| PAIR | 60% |
| TAP | 80% |
| GCG | 86% |
| PAP | 94% |
| **Prompt (μόνο)** | **100%** |

## Τεχνικές Λεπτομέρειες

Η πρόσβαση σε logprobs επέτρεψε την εύκολη επίθεση χωρίς ανάγκη προηγμένων τεχνικών.

## Σχετικές Σελίδες

- [[openai]]
- [[gpt-4-turbo]]
- [[gpt-4o]]
- [[jailbreaking]]
- [[logprobs]]