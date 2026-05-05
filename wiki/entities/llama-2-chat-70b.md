---
type: entity
title: "Llama-2-Chat-70B"
tags: [LLM, Meta, open-weight]
related: [llama-2-chat-7b, llama-2-chat-13b, llama-3-instruct-8b]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Llama-2-Chat-70B

## Επισκόπηση

Το Llama-2-Chat-70B είναι η μεγαλύτερη έκδοση 70 δισεκατομμυρίων παραμέτρων του Llama-2-Chat.

## Αποτελέσματα Επιθέσεων

| Μέθοδος | Ποσοστό Επιτυχίας |
|---------|-------------------|
| Tree of Attacks with Pruning | 13% |
| GCG | 38% |
| **Prompt + RS + Self-Transfer** | **100%** |

## Σημειώσεις

- Το μεγαλύτερο μοντέλο της οικογένειας Llama-2
- Η τεχνική self-transfer εφαρμόζεται ξεχωριστά για κάθε μέγεθος μοντέλου

## Σχετικές Σελίδες

- [[llama-2-chat-7b]]
- [[llama-2-chat-13b]]
- [[self-transfer]]