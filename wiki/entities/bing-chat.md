---
---
type: entity
title: "Bing Chat"
tags: ["Chatbot", "LLM Product", "Microsoft"]
related: ["masterkey", "llm-chatbot", "jailbreaking", "content-moderation", "real-time-monitoring"]
sources: ["Deng 等 - 2024 - MASTERKEY Automated Jailbreaking of Large Language Model Chatbots.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Bing Chat

## Gambaran Umum

Bing Chat adalah chatbot AI yang dikembangkan oleh Microsoft dan diintegrasikan ke dalam mesin pencari Bing. Bing Chat menjadi salah satu target utama dalam penelitian MASTERKEY untuk menganalisis mekanisme pertahanan terhadap serangan jailbreak.

## Karakteristik Pertahanan

Berdasarkan penelitian MASTERKEY, Bing Chat memiliki karakteristik pertahanan unik:

### Tidak Ada Penyaringan Input
Mirip dengan Bard, Bing Chat tidak melakukan penyaringan pada input prompt secara langsung. Validasi dilakukan pada output generasi model.

### Pemantauan Real-time
Bing Chat menggunakan pemantauan dinamis yang mendeteksi pelanggaran kebijakan selama proses generasi konten.

### Kombinasi Keyword dan Semantic Analysis
Pertahanan Bing Chat menggabungkan:
- **Keyword Matching**: Deteksi berbasis pencocokan kata kunci terlarang
- **Semantic Analysis**: Analisis kontekstual untuk memahami makna

## Hasil Jailbreak

| Metrik | Nilai |
|--------|-------|
| Tingkat Keberhasilan Query (Metode Eksisting) | 0.63% |
| Tingkat Keberhasilan Query (MASTERKEY) | 13.63% |

## Temuan Utama

1. Bing Chat lebih resilient terhadap serangan jailbreak dibandingkan ChatGPT
2. Respons Bing Chat tidak memberikan transparansi tentang kebijakan yang dilanggar
3. MASTERKEY adalah yang pertama berhasil mendemonstrasikan jailbreak terhadap Bing Chat
4. Waktu respons Bing Chat lebih lama dibandingkan layanan lain

## Halaman Terkait

- [[masterkey]]
- [[llm-chatbot]]
- [[jailbreaking]]
- [[content-moderation]]
- [[real-time-monitoring]]
- [[keyword-matching]]