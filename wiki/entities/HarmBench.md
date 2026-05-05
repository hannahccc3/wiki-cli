---
type: entity
title: "HarmBench"
tags: [benchmark, dataset, jailbreak_evaluation]
related: [AdvBench, ASR, TASR]
sources: ["Feng 等 - 2026 - SEMA Simple yet Effective Learning for Multi-Turn Jailbreak Attacks.md"]
created: 2026-01-15
updated: 2026-01-15
---
# HarmBench

## Επισκόπηση

Το **HarmBench** είναι ένα benchmark dataset για την αξιολόγηση επιθέσεων jailbreak και την ασφάλεια μοντέλων γλωσσικής τεχνητής νοημοσύνης. Περιλαμβάνει 320 κείμενες συμπεριφορές στο test set.

## Χρήση στο SEMA

Το HarmBench χρησιμοποιήθηκε για την αξιολόγηση της γενίκευσης του SEMA σε out-of-distribution δεδομένα.

## Αποτελέσματα SEMA στο HarmBench

| Μοντέλο Θύματος | ASR@1 |
|-----------------|-------|
| Qwen2.5-3B-Instruct | 74.5% |
| Llama-3.1-8B-Instruct | 70.6% |
| GPT-4.1-mini | 79.8% |
| **Μέσος όρος** | **75.0%** |

## Σχετικές Σελίδες

- [[AdvBench]]
- [[ASR]]
- [[TASR]]
- [[SEMA]]