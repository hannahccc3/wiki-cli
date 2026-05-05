---
type: source
title: "SEMA: Απλή αλλά αποτελεσματική εκμάθηση για επιθέσεις jailbreak πολλαπλών στροφών"
authors: ["Mingqian Feng", "Xiaodong Liu", "Weiwei Yang", "Jialin Song", "Xuekai Zhu", "Chenliang Xu", "Jianfeng Gao"]
year: 2026
url: "https://github.com/fmmarkmq/SEMA"
venue: "University of Rochester και Microsoft Research"
tags: [jailbreak_attacks, multi-turn_interactions, LLM_safety, reinforcement_learning, adversarial_attacks]
related: [multi-turn_jailbreak, intent_drift, open-loop_generation, prefilling_self-tuning, intent-drift-aware_reward, ASR, TASR, GRPO]
sources: ["Feng 等 - 2026 - SEMA Simple yet Effective Learning for Multi-Turn Jailbreak Attacks.md"]
created: 2026-01-15
updated: 2026-01-15
---
# SEMA: Απλή αλλά αποτελεσματική εκμάθηση για επιθέσεις jailbreak πολλαπλών στροφών

## Επισκόπηση

Η ερευνητική εργασία παρουσιάζει το **SEMA** (Simple yet Effective Framework for Multi-Turn Jailbreak Learning), ένα πλαίσιο εκμάθησης για επιθέσεις jailbreak πολλαπλών στροφών σε μοντέλα γλωσσικής τεχνητής νοημοσύνης (LLM). Το SEMA αποτελείται από δύο βασικά στάδια: την **προσυμπλήρωση αυτο-ρύθμισης** (prefilling self-tuning) για σταθεροποίηση των rollouts και την **ενισχυτική μάθηση με ανταμοιβή επίγνωσης απόκλισης πρόθεσης** (reinforcement learning with intent-drift-aware reward).

## Κύρια Σημεία

### Μεθοδολογία
- **Προσυμπλήρωση αυτο-ρύθμισης**: Επιτρέπει χρησιμοποιήσιμα rollouts μέσω βελτιστοποίησης σε μη-απορριπτικές, καλά δομημένες αντιεπιθετικές προτροπές πολλαπλών στροφών
- **Ανταμοιβή με επίγνωση απόκλισης πρόθεσης**: Εκπαιδεύει τον επιτιθέμενο να διατηρεί τον ίδιο επιβλαβή σκοπό σε όλες τις στροφές
- **Δημιουργία ανοιχτού βρόχου**: Αποφεύγει την εξάρτηση από τις απαντήσεις του θύματος

### Αποτελέσματα
- **80.1% ASR@1** κατά μέσο όρο σε τρία μοντέλα θύματα (Qwen2.5-3B, Llama-3.1-8B, GPT-4.1-mini)
- Υπερβαίνει σημαντικά όλα τα baseline μονής και πολλαπλών στροφών
- Ισχυρή μεταφορά σε διάφορες ρυθμίσεις

### Καινοτομίες
1. Εκπαιδεύει επιτιθέμενους χωρίς εξωτερικές στρατηγικές ή δεδομένα
2. Μειώνει την πολυπλοκότητα εξερεύνησης
3. Παρέχει πιο ισχυρό και ρεαλιστικό τεστ ασφαλείας για τα LLM

## Σχετικές Σελίδες

- [[SEMA]]
- [[multi-turn_jailbreak]]
- [[intent_drift]]
- [[open-loop_generation]]
- [[prefilling_self-tuning]]
- [[intent-drift-aware_reward]]
- [[ASR]]
- [[TASR]]
- [[GRPO]]
- [[AdvBench]]
- [[HarmBench]]