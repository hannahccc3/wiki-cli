---
type: entity
title: "AdvBench"
tags: [benchmark, dataset, jailbreak_evaluation]
related: [HarmBench, ASR, TASR]
sources: ["Feng 等 - 2026 - SEMA Simple yet Effective Learning for Multi-Turn Jailbreak Attacks.md"]
created: 2026-01-15
updated: 2026-01-15
---
# AdvBench

## Επισκόπηση

Το **AdvBench** είναι ένα benchmark dataset για την αξιολόγηση επιθέσεων jailbreak σε μοντέλα γλωσσικής τεχνητής νοημοσύνης. Περιέχει 520 δείγματα επιβλαβών ερωτήσεων.

## Χρήση στο SEMA

Το AdvBench χρησιμοποιήθηκε ως ένα από τα κύρια datasets για την αξιολόγηση του SEMA. Οι ερευνητές χρησιμοποίησαν το 80% του dataset για εκπαίδευση.

## Αποτελέσματα SEMA στο AdvBench

| Μοντέλο Θύματος | ASR@1 |
|-----------------|-------|
| Qwen2.5-3B-Instruct | 79.9% |
| Llama-3.1-8B-Instruct | 77.2% |
| GPT-4.1-mini | 83.3% |
| **Μέσος όρος** | **80.1%** |

## Σχετικές Σελίδες

- [[HarmBench]]
- [[ASR]]
- [[TASR]]
- [[SEMA]]