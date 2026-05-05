---
type: entity
title: "Qwen2.5-3B-Instruct"
tags: [language_model, victim_model]
related: [SEMA, ASR, AdvBench, HarmBench]
sources: ["Feng 等 - 2026 - SEMA Simple yet Effective Learning for Multi-Turn Jailbreak Attacks.md"]
created: 2026-01-15
updated: 2026-01-15
---
# Qwen2.5-3B-Instruct

## Επισκόπηση

Το **Qwen2.5-3B-Instruct** είναι ένα μοντέλο γλωσσικής τεχνητής νοημοσύνης ανοιχτού κώδικα 3 δισεκατομμυρίων παραμέτρων από την ομάδα Qwen. Χρησιμοποιήθηκε ως μοντέλο-στόχος και ως βασικός επιτιθέμενος στο SEMA.

## Χρήση στο SEMA

### Ως Μοντέλο-Θύμα
Το Qwen2.5-3B-Instruct χρησιμοποιήθηκε ως ένα από τα κύρια μοντέλα-στόχους για την αξιολόγηση της αποτελεσματικότητας του SEMA.

### Ως Βασικός Επιτιθέμενος
Χρησιμοποιήθηκε επίσης ως βασικός επιτιθέμενος σε ορισμένες πειραματικές ρυθμίσεις.

## Αποτελέσματα

| Dataset | ASR@1 |
|---------|-------|
| AdvBench | 79.9% |
| HarmBench | 74.5% |

## Σχετικές Σελίδες

- [[SEMA]]
- [[ASR]]
- [[AdvBench]]
- [[HarmBench]]