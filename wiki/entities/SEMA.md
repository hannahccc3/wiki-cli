---
type: entity
title: "SEMA (Simple yet Effective Framework for Multi-Turn Jailbreak Learning)"
tags: [jailbreak_attacks, multi-turn_interactions, LLM_safety, reinforcement_learning]
related: [multi-turn_jailbreak, intent_drift, open-loop_generation, prefilling_self-tuning, intent-drift-aware_reward, GRPO, ASR]
sources: ["Feng 等 - 2026 - SEMA Simple yet Effective Learning for Multi-Turn Jailbreak Attacks.md"]
created: 2026-01-15
updated: 2026-01-15
---
# SEMA

## Επισκόπηση

Το **SEMA** (Simple yet Effective Framework for Multi-Turn Jailbreak Learning) είναι ένα πλαίσιο εκμάθησης για επιθέσεις jailbreak πολλαπλών στροφών σε μοντέλα γλωσσικής τεχνητής νοημοσύνης. Αναπτύχθηκε από ερευνητές του University of Rochester και της Microsoft Research το 2026.

## Αρχιτεκτονική

Το SEMA αποτελείται από δύο βασικά στάδια:

### Στάδιο 1: Προσυμπλήρωση αυτο-ρύθμισης (Prefilling Self-tuning)
- Επιτρέπει χρησιμοποιήσιμα rollouts
- Βελτιστοποιεί σε μη-απορριπτικές, καλά δομημένες αντιεπιθετικές προτροπές
- Σταθεροποιεί τα rollouts για επακόλουθη εκμάθηση

### Στάδιο 2: Ενισχυτική μάθηση με ανταμοιβή επίγνωσης απόκλισης πρόθεσης
- Χρησιμοποιεί GRPO (Group Relative Policy Optimization)
- Εκπαιδεύει τον επιτιθέμενο να διατηρεί τον επιβλαβή σκοπό
- Δημιουργεί έγκυρες προτροπές πολλαπλών στροφών

## Αποτελεσματικότητα

| Μοντέλο Θύματος | ASR@1 (AdvBench) |
|-----------------|------------------|
| Qwen2.5-3B-Instruct | 79.9% |
| Llama-3.1-8B-Instruct | 77.2% |
| GPT-4.1-mini | 83.3% |
| **Μέσος όρος** | **80.1%** |

## Σημασία

- Υπερβαίνει όλα τα υπάρχοντα baseline μονής και πολλαπλών στροφών
- Επιδεικνύει ισχυρή μεταφορά σε διάφορες ρυθμίσεις
- Παρέχει πιο ισχυρό και ρεαλιστικό τεστ ασφαλείας για τα LLM

## Σχετικές Σελίδες

- [[multi-turn_jailbreak]]
- [[intent_drift]]
- [[open-loop_generation]]
- [[prefilling_self-tuning]]
- [[intent-drift-aware_reward]]
- [[GRPO]]
- [[ASR]]
- [[AdvBench]]
- [[HarmBench]]