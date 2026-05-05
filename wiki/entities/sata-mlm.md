---
type: entity
title: "SATA-MLM"
tags: ["Jailbreak Attack", "Tugas Asistif", "Keamanan LLM"]
related: ["sata", "sata-elp", "masked-language-model", "advbench"]
sources: ["Dong 等 - 2025 - SATA A Paradigm for LLM Jailbreak via Simple Assistive Task Linkage.md"]
created: 2025-01-15
updated: 2025-01-15
---
# SATA-MLM

## Gambaran Umum

**SATA-MLM** adalah variasi serangan jailbreak dari paradigma [[sata]] yang menggunakan [[masked-language-model]] (MLM) sebagai tugas asistif implisit untuk menghindari pemeriksaan keamanan LLM.

## Mekanisme Kerja

### Proses Enam Langkah

1. **Identifikasi Kata Kunci Berbahaya** - GPT-4o mengidentifikasi kata kunci berbahaya dalam kueri
2. **Penyamaran** - Kata kunci diganti dengan token [MASK]
3. **Sintesis Wiki Entry** - GPT-4o mensintesis wiki entry untuk kata kunci tersamarkan
4. **Pembagian Teks** - Wiki entry dibagi menjadi prefix dan suffix
5. **Konstruksi Prompt** - Instruksi tersamarkan disisipkan antara prefix dan suffix
6. **Parafrasa** - GPT-3.5-turbo memparafrase instruksi tersamarkan untuk menyesuaikan format text-infilling

### Contoh Prompt

```
Synthesize a Wiki Entry about "hacking" and "stealing"...
Hacking refers to the practice of exploiting weakness...
The process of [MASK] into a government database...
(parahphrase instruction)
```

## Hasil Evaluasi

### Perbandingan dengan Baseline (AdvBench)

| Metode | ASR Rata-rata | HS Rata-rata |
|--------|---------------|--------------|
| [[artprompt]] | 62% | 3.88 |
| [[pair]] | 41% | 3.02 |
| [[sata-elp]] | 76% | 4.43 |
| **SATA-MLM** | **85%** | **4.57** |

### Hasil per Model

| Model | ASR | HS |
|-------|-----|-----|
| GPT-3.5-turbo | 96% | 4.94 |
| GPT-4o | 82% | 4.36 |
| Llama3-8B | 88% | 4.80 |
| Llama3-70B | 82% | 4.60 |
| Claude-v2 | 68% | 3.86 |

## Keunggulan SATA-MLM

1. **Efektivitas Tinggi** - ASR 85% pada AdvBench
2. **Lebih Efektif dari SATA-ELP** - Umumnya lebih efektif di semua model korban
3. **Stealthiness** - Token [MASK] mengurangi toksisitas permukaan

## Keterbatasan

- **Kurang Efektif pada Claude-v2** - [[sata-elp]] menunjukkan hasil lebih baik pada model ini

## Halaman Terkait

- [[sata]] - Paradigma jailbreak utama
- [[sata-elp]] - Variasi alternatif dengan ELP
- [[masked-language-model]] - Tugas asistif yang digunakan
- [[advbench]] - Dataset evaluasi