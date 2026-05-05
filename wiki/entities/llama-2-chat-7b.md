---
type: entity
title: "Llama-2-Chat-7B"
tags: [LLM, Meta, open-weight]
related: [llama-2-chat-13b, llama-2-chat-70b, llama-3-instruct-8b, meta]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Llama-2-Chat-7B

## Επισκόπηση

Το Llama-2-Chat-7B είναι ένα μοντέλο 7 δισεκατομμυρίων παραμέτρων από τη Meta, εκπαιδευμένο με τεχνικές ευθυγράμμισης ασφαλείας. Αποτελεί ένα από τα πιο δημοφιλή ανοιχτά LLMs.

## Αποτελέσματα στην Έρευνα

Σύμφωνα με την εργασία Andriushchenko et al. 2024:

| Μέθοδος | Ποσοστό Επιτυχίας |
|---------|-------------------|
| Tree of Attacks with Pruning | 4% |
| Prompt Automatic Iterative Refinement | 10% |
| GCG | 54% |
| Persuasive Adversarial Prompts | 92% |
| **Prompt + RS + Self-Transfer** | **100%** |

## Βασικά Ευρήματα

- Το μοντέλο είναι ανθεκτικό σε απλές επιθέσεις (0% με μόνο prompt)
- Η τεχνική self-transfer είναι κρίσιμη για την επίτευξη 100% επιτυχίας
- Η αρχικοποίηση με επιτυχημένα επιθήματα από απλούστερα αιτήματα βελτιώνει σημαντικά τα αποτελέσματα

## Σχετικές Σελίδες

- [[llama-2-chat-13b]]
- [[llama-2-chat-70b]]
- [[llama-3-instruct-8b]]
- [[self-transfer]]
- [[random-search]]