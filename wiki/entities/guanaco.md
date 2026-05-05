---
type: entity
title: Guanaco
tags: ["LLM", "model"]
related: ["cold-attack", "llama-2", "mistral", "vicuna", "gpt-3.5", "gpt-4", "white-box-attacks"]
sources: ["Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Guanaco

## Gambaran Umum

**Guanaco** adalah keluarga model bahasa besar yang dilatih menggunakan teknik kuantisasi. Guanaco-7B-HF dan Guanaco-13B-HF digunakan dalam eksperimen COLD-Attack.

## Penggunaan dalam COLD-Attack

Guanaco digunakan sebagai model target white-box untuk evaluasi serangan.

## Hasil Eksperimen

Berdasarkan hasil eksperimen untuk Guanaco-7B:

- **ASR**: 96.00%
- **ASR-G**: 84.00%
- **PPL**: 30.55

Guanaco menunjukkan kerentanan terhadap serangan COLD-Attack, terutama dengan sentimen negatif.

## Halaman Terkait

- [[cold-attack]] - Metode serangan
- [[llama-2]] - Model target lain
- [[mistral]] - Model target lain
- [[vicuna]] - Model target lain
- [[gpt-3.5]] - Model target lain
- [[gpt-4]] - Model target lain
- [[white-box-attacks]] - Kategori serangan