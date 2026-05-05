---
type: entity
title: "GPT-oss-20B"
tags: [language_model, victim_model, reasoning_model]
related: [SEMA, ASR, multi-turn_jailbreak]
sources: ["Feng 等 - 2026 - SEMA Simple yet Effective Learning for Multi-Turn Jailbreak Attacks.md"]
created: 2026-01-15
updated: 2026-01-15
---
# GPT-oss-20B

## Επισκόπηση

Το **GPT-oss-20B** είναι ένα μοντέλο γλωσσικής τεχνητής νοημοσύνης ανοιχτού κώδικα 20 δισεκατομμυρίων παραμέτρων με δυνατότητες συλλογιστικής (reasoning). Θεωρείται ιδιαίτερα ασφαλές μοντέλο.

## Χρήση ως Θύμα στο SEMA

Το GPT-oss-20B χρησιμοποιήθηκε ως μοντέλο-στόχος για την αξιολόγηση της μεταφοράς επιθέσεων. Αν και θεωρείται πολύ ασφαλές, το SEMA κατάφερε να επιτύχει σημαντικά ποσοστά επιτυχίας.

## Αποτελέσματα

| Dataset | LLM Classifier | HarmBench Classifier |
|---------|-----------------|----------------------|
| AdvBench | 36.0% | 57.7% |
| HarmBench | 15.1% | 39.0% |

## Σημασία

Αποτελεί ένα από τα πιο ασφαλή μοντέλα-στόχους στη μελέτη, με τα χαμηλότερα ποσοστά ASR μεταξύ όλων των θυμάτων.

## Σχετικές Σελίδες

- [[SEMA]]
- [[ASR]]
- [[multi-turn_jailbreak]]
- [[TASR]]