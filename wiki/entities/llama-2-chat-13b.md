---
type: entity
title: "Llama-2-Chat-13B"
tags: [LLM, Meta, open-weight]
related: [llama-2-chat-7b, llama-2-chat-70b, llama-3-instruct-8b]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Llama-2-Chat-13B

## Επισκόπηση

Το Llama-2-Chat-13B είναι η έκδοση 13 δισεκατομμυρίων παραμέτρων του Llama-2-Chat από τη Meta.

## Αποτελέσματα Επιθέσεων

| Μέθοδος | Ποσοστό Επιτυχίας |
|---------|-------------------|
| Tree of Attacks with Pruning | 14% |
| GCG | 30% |
| **Prompt + RS + Self-Transfer** | **100%** |

## Σημειώσεις

- Μεγαλύτερο μοντέλο από το Llama-2-Chat-7B
- Απαιτεί ξεχωριστή διαδικασία self-transfer για βέλτιστα αποτελέσματα

## Σχετικές Σελίδες

- [[llama-2-chat-7b]]
- [[llama-2-chat-70b]]
- [[self-transfer]]