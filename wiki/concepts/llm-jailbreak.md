---
type: concept
title: "Jailbreak Attack (Serangan Jailbreak)"
tags: ["Keamanan LLM", "Serangan Adversarial", "Keamanan AI"]
related: ["sata", "safety-alignment", "gcg", "autodan", "pair", "artprompt", "attack-success-rate", "harmful-score"]
sources: ["Dong 等 - 2025 - SATA A Paradigm for LLM Jailbreak via Simple Assistive Task Linkage.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Jailbreak Attack (Serangan Jailbreak)

## Gambaran Umum

**Serangan Jailbreak** adalah serangan adversarial yang memancing model bahasa besar (LLM) untuk menghasilkan respons berbahaya atau dilarang, dengan cara mem-bypass atau mengelak dari mekanisme [[safety-alignment]].

## Kategori Serangan Jailbreak

### 1. Metode Berbasis Pencarian

Menggunakan LLM sebagai sistem komputasional dan menjailbreak menggunakan metode pencarian:

| Metode | Deskripsi |
|--------|-----------|
| [[gcg]] | Menggabungkan optimasi greedy dan gradient-based untuk menghitung suffix adversarial |
| [[autodan]] | Menggunakan algoritma genetik untuk menghasilkan dan menyempurnakan prompt jailbreak secara iteratif |
| [[pair]] | Memanfaatkan attacker LLM untuk menghasilkan dan menyempurnakan prompt jailbreak secara iteratif |
| AdvPrompter | Fine-tune attacker LLM untuk menghasilkan suffix adversarial |

### 2. Metode Penyamaran

Menyamarkan instruksi berbahaya dalam skenario tertentu atau transformasi khusus:

| Metode | Deskripsi |
|--------|-----------|
| [[artprompt]] | Mentransformasi kata berbahaya ke format seni ASCII |
| DrAttack | Memecah instruksi berbahaya menjadi sub-prompt |
| [[sata]] | Menyamarkan kata kunci dengan token [MASK] dan mengaitkan dengan tugas asistif |

## Metrik Evaluasi

### [[attack-success-rate]]

Metrik yang mengukur persentase keberhasilan jailbreak, didefinisikan sebagai rasio respons dengan [[harmful-score]] = 5.

### [[harmful-score]]

Skor 1-5 yang mengukur tingkat bahaya respons LLM:
- **1**: Model menolak merespons atau respons tidak berbahaya
- **5**: Respons sangat berbahaya atau relevan

## Pertahanan Jailbreak

Empat jenis utama metode pertahanan:

1. **Filter-based** - Memeriksa perplexity input
2. **Modification-based** - Mengganggu input melalui permutasi
3. **Prompt-based** - Menggunakan demonstrasi untuk mengingatkan LLM
4. **Optimization-based** - Menghitung suffix prompt defensif

## Halaman Terkait

- [[sata]] - Paradigma jailbreak terbaru
- [[safety-alignment]] - Mekanisme keamanan yang di-bypass
- [[attack-success-rate]] - Metrik keberhasilan
- [[harmful-score]] - Metrik bahaya
- [[gcg]], [[autodan]], [[pair]], [[artprompt]] - Metode jailbreak lainnya