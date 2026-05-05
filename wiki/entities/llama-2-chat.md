---
type: entity
title: "Llama-2-Chat"
tags: ["LLM", "Meta", "open-weight", "safety-aligned"]
related: ["llama-3-instruct-8b", "gemma-7b", "vicuna-13b", "mistral-7b", "meta", "jailbreaking", "safety-alignment"]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Llama-2-Chat

## Επισκόπηση

Το Llama-2-Chat είναι ένα οικογένεια ανοιχτών μοντέλων LLM από τη Meta που έχουν υποστεί εκτεταμένη εκπαίδευση ευθυγράμμισης ασφαλείας (safety alignment). Διατίθεται σε διάφορα μεγέθη: 7B, 13B και 70B παραμέτρων.

## Αποτελέσματα Έρευνας

Η έρευνα έδειξε ότι το Llama-2-Chat είναι ευάλωτο σε προσαρμοστικές επιθέσεις:

| Μέγεθος | Προηγούμενο ASR | Δικό μας ASR |
|---------|-----------------|--------------|
| 7B | 92% | 100% |
| 13B | 30% | 100% |
| 70B | 38% | 100% |

## Τεχνικές Επίθεσης

Η επιτυχία επιτεύχθηκε χρησιμοποιώντας **Prompt + Random Search + Self-Transfer**.

## Σχετικές Σελίδες

- [[meta]]
- [[llama-3-instruct-8b]]
- [[jailbreaking]]
- [[random-search]]
- [[self-transfer]]