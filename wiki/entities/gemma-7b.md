---
type: entity
title: "Gemma-7B"
tags: ["LLM", "Google", "open-weight", "safety-aligned"]
related: ["llama-2-chat", "llama-3-instruct-8b", "gpt-4o", "llama-2-chat-7b", "google", "jailbreaking", "safety-alignment"]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Gemma-7B

## Επισκόπηση

Το Gemma-7B είναι ένα ανοιχτό μοντέλο LLM από την Google, μέρος της οικογένειας Gemma. Έχει σχεδιαστεί για να παρέχει ισχυρές δυνατότητες γλωσσικής κατανόησης με ενσωματωμένη ασφάλεια.

## Αποτελέσματα Έρευνας

Η έρευνα έδειξε ότι το Gemma-7B είναι ευάλωτο σε προσαρμοστικές επιθέσεις:

| Μέθοδος | ASR |
|---------|-----|
| Prompt | 20% |
| Prompt + Random Search | 84% |
| Prompt + RS + Self-Transfer | 100% |

## Σχετικές Σελίδες

- [[google]]
- [[jailbreaking]]
- [[random-search]]
- [[self-transfer]]