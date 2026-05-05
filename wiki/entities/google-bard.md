---
type: entity
title: "Google Bard"
tags: ["Chatbot", "LLM Product", "Google"]
related: ["masterkey", "llm-chatbot", "jailbreaking", "content-moderation", "real-time-monitoring"]
sources: ["Deng 等 - 2024 - MASTERKEY Automated Jailbreaking of Large Language Model Chatbots.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Google Bard

## Gambaran Umum

Google Bard adalah chatbot AI yang dikembangkan oleh Google, menggunakan model bahasa besar sebagai backend. Bard menjadi salah satu target utama dalam penelitian MASTERKEY untuk menganalisis mekanisme pertahanan terhadap serangan jailbreak.

## Karakteristik Pertahanan

Berdasarkan penelitian MASTERKEY, Google Bard memiliki karakteristik pertahanan unik:

### Tidak Ada Penyaringan Input
Bard tidak melakukan penyaringan pada input prompt secara langsung. Validasi dilakukan pada output generasi model.

### Pemantauan Real-time
Bard menggunakan pemantauan dinamis yang mendeteksi pelanggaran kebijakan selama proses generasi konten, bukan hanya setelah generasi selesai.

### Kombinasi Keyword dan Semantic Analysis
Pertahanan Bard menggabungkan:
- **Keyword Matching**: Deteksi berbasis pencocokan kata kunci terlarang
- **Semantic Analysis**: Analisis kontekstual untuk memahami makna

## Hasil Jailbreak

| Metrik | Nilai |
|--------|-------|
| Tingkat Keberhasilan Query (Metode Eksisting) | 0.40% |
| Tingkat Keberhasilan Query (MASTERKEY) | 14.51% |

## Temuan Utama

1. Bard lebih resilient terhadap serangan jailbreak dibandingkan ChatGPT
2. Respons Bard tidak memberikan detail spesifik tentang pelanggaran kebijakan
3. MASTERKEY adalah yang pertama berhasil mendemonstrasikan jailbreak terhadap Bard

## Halaman Terkait

- [[masterkey]]
- [[llm-chatbot]]
- [[jailbreaking]]
- [[content-moderation]]
- [[real-time-monitoring]]
- [[keyword-matching]]