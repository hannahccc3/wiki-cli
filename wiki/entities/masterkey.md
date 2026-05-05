---
type: entity
title: "MASTERKEY"
tags: ["Framework", "Jailbreak", "LLM Security", "Research Project"]
related: ["jailbreaking", "llm-chatbot", "rlhf", "gpt-3.5", "gpt-4", "google-bard", "bing-chat", "time-based-testing"]
sources: ["Deng 等 - 2024 - MASTERKEY Automated Jailbreaking of Large Language Model Chatbots.md"]
created: 2024-01-15
updated: 2024-01-15
---
# MASTERKEY

## Gambaran Umum

MASTERKEY adalah framework penelitian yang dikembangkan untuk mengeksplorasi dinamika serangan jailbreak dan countermeasures pada chatbot LLM. Framework ini diperkenalkan dalam paper yang dipresentasikan di NDSS 2024. MASTERKEY menggabungkan metodologi berbasis waktu yang terinspirasi dari teknik SQL injection untuk membedah mekanisme pertahanan layanan LLM, serta pendekatan otomatis untuk menghasilkan prompt jailbreak.

## Karakteristik Utama

### Metodologi Berbasis Waktu

MASTERKEY menggunakan waktu respons sebagai indikator untuk memahami mekanisme pertahanan LLM. Teknik ini terinspirasi dari time-based blind SQL injection dalam keamanan web. Dengan menganalisis waktu yang diperlukan untuk menghasilkan respons, peneliti dapat menyimpulkan:

- Tahap penegakan kebijakan (input vs output validation)
- Apakah pemeriksaan dilakukan secara real-time selama generasi
- Jenis mekanisme deteksi yang digunakan (keyword matching vs semantic analysis)

### Three-Step Fine-tuning

MASTERKEY mengembangkan pendekatan otomatis untuk menghasilkan prompt jailbreak melalui tiga tahap:

1. **Dataset Building and Augmentation**: Mengumpulkan dan menyempurnakan dataset prompt jailbreak dari berbagai sumber
2. **Continuous Pre-training and Task Tuning**: Melatih LLM khusus dengan fokus utama pada jailbreaking
3. **Reward Ranked Fine Tuning**: Menggunakan strategi penghargaan berbasis performa aktual untuk meningkatkan kemampuan bypass

## Hasil Kinerja

MASTERKEY menunjukkan performa yang signifikan dibandingkan metode yang ada:

| Metrik | Nilai |
|--------|-------|
| Tingkat Keberhasilan Query | 21.58% |
| Tingkat Keberhasilan Prompt | 26.05% |
| Peningkatan vs Metode Eksisting | ~3x lebih tinggi (7.33%) |

### Keberhasilan per Model

| Model | Tingkat Keberhasilan |
|-------|---------------------|
| GPT-3.5 | 21.12% |
| GPT-4 | 7.13% |
| Bard | 14.51% |
| Bing Chat | 13.63% |

## Kontribusi Utama

1. **Reverse-Engineering Pertahanan**: Membedah mekanisme pertahanan LLM chatbot yang tidak dipublikasikan menggunakan metodologi berbasis waktu
2. **Bypassing Pertahanan LLM**: Berhasil melewati mekanisme pertahanan menggunakan manipulasi strategis berbasis waktu respons
3. **Generasi Jailbreak Otomatis**: Menunjukkan strategi percontohan yang sangat efektif untuk menghasilkan prompt jailbreak secara otomatis
4. **Generalisasi Jailbreak**: Memperluas teknik jailbreak across pattern dan LLM chatbot yang berbeda

## Pertimbangan Etis

Penelitian ini dilakukan di bawah pedoman etis yang ketat:
- Tidak mengeksploitasi teknik jailbreak untuk merusak layanan
- Melaporkan masalah yang diidentifikasi kepada penyedia layanan
- Hanya menyediakan proof-of-concept (PoC) dalam diskusi
- Tidak merilis dataset jailbreak lengkap sebelum masalah ditangani

## Halaman Terkait

- [[jailbreaking]]
- [[llm-chatbot]]
- [[rlhf]]
- [[fine-tuning]]
- [[time-based-testing]]
- [[gpt-3.5]]
- [[gpt-4]]
- [[google-bard]]
- [[bing-chat]]