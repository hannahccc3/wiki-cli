---
type: concept
title: "SATA (Simple Assistive Task Linkage)"
tags: ["Keamanan LLM", "Serangan Jailbreak", "Tugas Asistif"]
related: ["llm-jailbreak", "masked-language-model", "element-lookup-by-position", "advbench", "jbb-behaviors"]
sources: ["Dong 等 - 2025 - SATA A Paradigm for LLM Jailbreak via Simple Assistive Task Linkage.md"]
created: 2025-01-15
updated: 2025-01-15
---
# SATA (Simple Assistive Task Linkage)

## Gambaran Umum

**SATA (Simple Assistive Task Linkage)** adalah paradigma jailbreak novel untuk model bahasa besar (LLM) yang menggunakan penghubungan tugas asistif sederhana untuk menghindari perlindungan keamanan LLM.

## Mekanisme Kerja

### Proses Tiga Langkah

1. **Penyamaran Kata Kunci** - Kata kunci berbahaya dalam kueri diganti dengan token [MASK]
2. **Konstruksi Tugas Asistif** - Tugas asistif sederhana dibangun untuk mengodekan semantik kata kunci tersamarkan
3. **Penghubungan** - Tugas asistif dihubungkan dengan instruksi tersamarkan untuk melakukan jailbreak

### Variasi SATA

| Varian | Deskripsi | ASR (AdvBench) |
|--------|-----------|----------------|
| [[sata-mlm]] | Menggunakan MLM sebagai tugas asistif implisit | 85% |
| [[sata-elp]] | Menggunakan ELP sebagai tugas asistif eksplisit | 76% |

## Keunggulan SATA

- **Efektivitas tinggi** - Mengalahkan metode baseline secara signifikan
- **Efisiensi biaya** - Menghemat satu urutan magnitudo dalam penggunaan token
- **Ketahanan pertahanan** - Tahan terhadap berbagai metode pertahanan
- **Kemudahan implementasi** - Tugas asistif dirancang agar mudah dilakukan oleh LLM

## Tujuan Tugas Asistif

1. **Mengganggu perhatian** LLM korban dari pemeriksaan keamanan
2. **Mengodekan semantik** kata kunci tersamarkan dan seringkonfirmasikan ke LLM korban

## Relevansi Keamanan

SATA mendemonstrasikan kerentanan baru dalam mekanisme penyelarasan keamanan LLM dan memberikan wawasan penting untuk pengembangan pertahanan yang lebih kuat.

## Halaman Terkait

- [[llm-jailbreak]] - Konsep serangan jailbreak secara umum
- [[masked-language-model]] - Tugas asistif implisit
- [[element-lookup-by-position]] - Tugas asistif eksplisit
- [[safety-alignment]] - Metode penyelarasan keamanan
- [[attack-success-rate]] - Metrik evaluasi
- [[harmful-score]] - Metrik evaluasi
- [[masking-granularity]] - Tingkat detail penyamaran