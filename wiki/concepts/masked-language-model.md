---
type: concept
title: "Masked Language Model (MLM)"
tags: ["Model Bahasa", "Tugas Asistif", "Pemrosesan Bahasa Alami"]
related: ["sata", "sata-mlm", "element-lookup-by-position", "llm-jailbreak"]
sources: ["Dong 等 - 2025 - SATA A Paradigm for LLM Jailbreak via Simple Assistive Task Linkage.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Masked Language Model (MLM)

## Gambaran Umum

**Masked Language Model (MLM)** adalah tugas asistif implisit yang digunakan dalam paradigma [[sata]] untuk mengodekan semantik kata kunci berbahaya yang tersamarkan. Model bahasa besar (LLM) sangat mahir dalam menyimpulkan token [MASK] dalam konteks yang diberikan.

## Peran dalam SATA

### Proses SATA-MLM

1. **Sintesis Wiki Entry** - GPT-4o disuruh mensintesis wiki entry untuk kata kunci berbahaya tersamarkan
2. **Pembagian Teks** - Wiki entry dibagi menjadi dua bagian:
   - **Prefix wiki text** - Ditempatkan sebelum instruksi tersamarkan
   - **Suffix wiki text** - Ditempatkan setelah instruksi tersamarkan
3. **Text-infilling** - LLM korban disuruh menyimpulkan token [MASK] dari konteks wiki sekitarnya

### Mekanisme Efektivitas

- Token [MASK] mengurangi toksisitas permukaan konten berbahaya
- Tugas MLM memungkinkan LLM secara internal menyimpulkan semantik sebagai kata kunci berbahaya yang dimaksud
- Representasi internal [MASK] secara progresif semakin mirip dengan kata kunci berbahaya asli di setiap layer

## Keunggulan MLM sebagai Tugas Asistif

1. **Friendly untuk LLM** - LLM sangat mahir dalam tugas isian teks
2. **Efisien** - Dapat menyimpulkan dengan benar dan efisien
3. **Compact** - Template prompt jailbreak dapat dirancang dengan ringkas

## Hasil Evaluasi

| Konfigurasi | ASR | HS |
|-------------|-----|-----|
| SATA-MLM-top1 | 72% | 4.17 |
| SATA-MLM-ensemble | 85% | 4.57 |

## Halaman Terkait

- [[sata]] - Paradigma jailbreak utama
- [[sata-mlm]] - Variasi SATA menggunakan MLM
- [[element-lookup-by-position]] - Tugas asistif eksplisit alternatif
- [[llm-jailbreak]] - Konsep serangan jailbreak