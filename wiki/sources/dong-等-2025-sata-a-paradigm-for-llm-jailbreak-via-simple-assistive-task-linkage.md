---
type: source
title: "SATA: Sebuah Paradigma untuk Jailbreak LLM melalui Penghubungan Tugas Assistif Sederhana"
authors: ["Xiaoning Dong", "Wenbo Hu", "Wei Xu", "Tianxing He"]
year: 2025
url: ""
venue: ""
tags: ["Keamanan LLM", "Serangan Jailbreak", "Pembelajaran Mesin Adversarial", "Masked Language Model", "Tugas Asistif", "Keamanan AI", "Red Teaming"]
related: ["advbench", "jbb-behaviors", "sata", "gcg", "autodan", "pair", "artprompt", "llm-jailbreak", "masked-language-model", "element-lookup-by-position"]
sources: ["Dong 等 - 2025 - SATA A Paradigm for LLM Jailbreak via Simple Assistive Task Linkage.md"]
created: 2025-01-15
updated: 2025-01-15
---
# SATA: Sebuah Paradigma untuk Jailbreak LLM melalui Penghubungan Tugas Assistif Sederhana

## Ringkasan

Paper ini memperkenalkan **SATA (Simple Assistive Task Linkage)**, sebuah paradigma jailbreak novel untuk model bahasa besar (LLM) yang bekerja dengan menyamarkan kata kunci berbahaya menggunakan token [MASK] dan menghubungkan dengan tugas asistif sederhana seperti [[masked-language-model]] (MLM) dan [[element-lookup-by-position]] (ELP) untuk menghindari pemeriksaan keamanan.

## Temuan Utama

### Efektivitas Serangan

SATA mencapai hasil yang sangat mengesankan dalam hal tingkat keberhasilan serangan (ASR) dan skor bahaya (HS):

- **SATA-MLM** mencapai ASR keseluruhan sebesar **85%** dan HS sebesar **4.57** pada dataset [[advbench]]
- **SATA-ELP** mencapai ASR keseluruhan sebesar **76%** dan HS sebesar **4.431**
- SATA mengungguli metode baseline seperti [[gcg]], [[autodan]], [[pair]], dan [[artprompt]] secara signifikan

### Efisiensi Biaya

SATA-ELP menghemat sekitar **satu urutan magnitudo** dalam penggunaan token input dibandingkan dengan baseline, menjadikannya pendekatan yang sangat efisien.

### Ketahanan terhadap Pertahanan

SATA tahan terhadap berbagai metode pertahanan termasuk:
- Filter PPL (Perplexity)
- Parafrasa
- Self-reminder
- RPO (Robust Prompt Optimization)

### Model Penalaran

Model penalaran seperti [[deepseek-r1]] dan [[openai-o3-mini]] tidak dapat secara langsung memitigasi jailbreak SATA.

## Metodologi

### Langkah 1: Penyamaran Kata Kunci Berbahaya

SATA menggunakan GPT-4o untuk menyamarkan kata kunci berbahaya dalam kueri berbahaya menggunakan token [MASK], menghasilkan kueri yang relatif jinak.

### Langkah 2: Penghubungan Tugas Asistif

SATA menghubungkan instruksi tersamarkan dengan tugas asistif sederhana:
- [[masked-language-model]] (MLM) sebagai tugas asistif implisit
- [[element-lookup-by-position]] (ELP) sebagai tugas asistif eksplisit

### Tujuan Tugas Asistif

1. **Mengganggu perhatian** LLM korban dari pemeriksaan keamanan
2. **Mengodekan semantik** kata kunci tersamarkan dan menyampaikan informasi ini ke LLM korban

## Model Korban yang Dievaluasi

| Model | Tipe |
|-------|------|
| [[gpt-4o]] | Tertutup |
| [[gpt-3.5-turbo]] | Tertutup |
| [[claude-2.0]] | Tertutup |
| [[llama3-8b]] | Terbuka |
| [[llama3-70b]] | Terbuka |
| [[deepseek-r1]] | Penalaran |
| [[openai-o3-mini]] | Penalaran |

## Kontribusi Paper

1. Paradigma jailbreak novel melalui penghubungan tugas asistif sederhana
2. Evaluasi ekstensif terhadap efektivitas, efisiensi biaya, dan sensitivitas terhadap pertahanan
3. Analisis dampak tingkat kesulitan tugas asistif terhadap kinerja jailbreak

## Halaman Terkait

- [[sata]] - Paradigma jailbreak utama
- [[llm-jailbreak]] - Konsep serangan jailbreak
- [[advbench]] - Dataset evaluasi
- [[masked-language-model]] - Tugas asistif implisit
- [[element-lookup-by-position]] - Tugas asistif eksplisit