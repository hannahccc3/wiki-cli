---
type: concept
title: "Safety Alignment (Penyelarasan Keamanan)"
tags: ["Ασφάλεια LLM", "Εκπαίδευση", "Fine-tuning", "AI safety", "LLM training", "RLHF", "harmlessness", "helpfulness", "Keamanan LLM", "Etika AI", "Perlindungan"]
related: ["jailbreaking", "adaptive-attacks", "llm-security", "r2d2", "many-shot-jailbreaking", "supervised-fine-tuning", "reinforcement-learning", "in-context-learning", "llm-jailbreak", "rlhf", "attack-success-rate", "harmful-score"]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md", "Anil 等 - Many-shot Jailbreaking.md", "Dong 等 - 2025 - SATA A Paradigm for LLM Jailbreak via Simple Assistive Task Linkage.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Safety Alignment (Penyelarasan Keamanan)

## Gambaran Umum

**Safety Alignment** adalah metode untuk menyelaraskan preferensi keamanan model bahasa besar (LLM) dengan preferensi manusia, untuk mencegah LLM merespons kueri berbahaya atau memiliki niat buruk.

## Metode Penyelarasan

### 1. Seleksi Data Pelatihan

Membersihkan dan menyeleksi data pelatihan untuk menghilangkan konten berbahaya.

### 2. [[rlhf]] (Reinforcement Learning from Human Feedback)

Menggunakan umpan balik manusia untuk menyempurnakan respons model.

### 3. RLHF Lanjutan

Berbagai variasi RLHF telah dikembangkan untuk meningkatkan keamanan model.

## Tantangan dalam Safety Alignment

Meskipun kemajuan signifikan telah dicapai, kerentanan keamanan masih ada. [[llm-jailbreak]] attacks dapat mengekspos kelemahan ini.

### Mengapa LLM Rentan?

1. **Keterbatasan Pemahaman** - LLM mungkin tidak memahami representasi khusus (misalnya: seni ASCII)
2. **Gangguan Perhatian** - Tugas asistif dapat mengalihkan perhatian dari pemeriksaan keamanan
3. **Rekonstruksi Semantik** - Token [MASK] dapat secara internal ditafsirkan sebagai kata kunci berbahaya

## Metode Pertahanan Jailbreak

| Jenis | Deskripsi |
|-------|-----------|
| Filter-based | Memeriksa perplexity input |
| Modification-based | Mengganggu input melalui permutasi |
| Prompt-based | Mengingatkan LLM melalui demonstrasi |
| Optimization-based | Menghitung suffix prompt defensif |

## Halaman Terkait

- [[llm-jailbreak]] - Serangan yang mencoba membypass safety alignment
- [[rlhf]] - Metode penyelarasan
- [[attack-success-rate]] - Metrik keberhasilan serangan
- [[harmful-score]] - Metrik tingkat bahaya