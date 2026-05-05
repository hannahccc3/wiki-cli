---
type: entity
title: "GPT-2"
tags: ["Γλωσσικό Μοντέλο", "Μεγάλο Γλωσσικό Μοντέλο", "OpenAI"]
related: ["large-language-models", "text-generation", "curiosity-driven-red-teaming", "llama-2", "dolly-v2"]
sources: ["Hong 等 - 2024 - CURIOSITY-DRIVEN RED-TEAMING FOR LARGE LAN- GUAGE MODELS.md"]
created: 2024-01-15
updated: 2024-01-15
---
# GPT-2

## Επισκόπηση

Το **GPT-2** (Generative Pre-trained Transformer 2) είναι ένα γλωσσικό μοντέλο 137 εκατομμυρίων παραμέτρων από την OpenAI. Στην εργασία χρησιμοποιήθηκε ως αρχικό μοντέλο για το red team και ως target LLM σε πειράματα συνέχισης κειμένου.

## Χρήση στην Έρευνα

### Ως Red Team Model
Το GPT-2 χρησιμοποιήθηκε ως αρχικό μοντέλο για την εκπαίδευση της πολιτικής red team:
- Αρχικοποίηση πολιτικής πλην = GPT-2 137M
- Χρήση ως reference model πλην_ref

### Ως Target LLM
Στα πειράματα συνέχισης κειμένου, το GPT-2 ήταν το μοντέλο-στόχος για δοκιμή τοξικότητας.

## Χαρακτηριστικά

- **Παράμετροι**: 137 εκατομμύρια
- **Αρχιτεκτονική**: Transformer decoder
- **Εκπαίδευση**: Self-supervised σε μεγάλο corpus κειμένου

## Σχετικές Σελίδες

- [[large-language-models]] - Κατηγορία μοντέλου
- [[text-generation]] - Ικανότητα μοντέλου
- [[curiosity-driven-red-teaming]] - Η έρευνα που χρησιμοποίησε το μοντέλο
- [[gpt-3]] - Διάδοχο μοντέλο
- [[alpaca]] - Παραλλαγή fine-tuned