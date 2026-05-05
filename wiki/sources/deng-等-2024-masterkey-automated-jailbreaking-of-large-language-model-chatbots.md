---
type: source
title: "MASTERKEY: Automated Jailbreaking of Large Language Model Chatbots"
authors: ["Gelei Deng", "Yi Liu", "Yuekang Li", "Kailong Wang", "Ying Zhang", "Zefeng Li", "Haoyu Wang", "Tianwei Zhang", "Yang Liu"]
year: 2024
url: "https://sites.google.com/view/ndss-masterkey"
venue: "NDSS (Network and Distributed System Security Symposium)"
tags: ["Jailbreaking", "LLM Security", "Prompt Injection", "Content Moderation", "AI Safety"]
related: ["jailbreaking", "llm-chatbot", "rlhf", "content-moderation", "keyword-matching", "real-time-monitoring", "fine-tuning", "prompt-engineering", "black-box-testing", "gpt-3.5", "gpt-4", "google-bard", "bing-chat", "rlhf"]
sources: ["Deng 等 - 2024 - MASTERKEY Automated Jailbreaking of Large Language Model Chatbots.md"]
created: 2024-01-15
updated: 2024-01-15
---
# MASTERKEY: Automated Jailbreaking of Large Language Model Chatbots

## Gambaran Umum

MASTERKEY adalah framework yang dikembangkan untuk mengeksplorasi dinamika serangan jailbreak dan countermeasures pada chatbot LLM. Paper ini memperkenalkan metodologi berbasis waktu, terinspirasi dari teknik SQL injection, untuk membedah mekanisme pertahanan yang tidak dipublikasikan dari layanan seperti Bard dan Bing Chat. Selain itu, framework ini mengembangkan pendekatan otomatis untuk menghasilkan prompt jailbreak melalui fine-tuning LLM, mencapai tingkat keberhasilan 21.58%, jauh lebih tinggi dari metode yang ada sebesar 7.33%.

## Abstrak

Model bahasa besar (LLM) seperti chatbot telah mengalami kemajuan signifikan di berbagai bidang namun tetap rentan terhadap serangan jailbreak yang bertujuan untuk menghasilkan respons yang tidak pantas. Meskipun telah ada upaya untuk mengidentifikasi kelemahan ini, strategi saat ini tidak efektif terhadap chatbot LLM mainstream, terutama karena adanya langkah-langkah pertahanan yang tidak dipublikasikan oleh penyedia layanan. Paper ini memperkenalkan MASTERKEY, sebuah framework untuk mengeksplorasi dinamika serangan jailbreak dan countermeasures.

## Temuan Utama

1. **Efektivitas Jailbreak Eksisting Terbatas**: Metode jailbreak yang ada hanya efektif terhadap ChatGPT (GPT-3.5 dan GPT-4), dengan tingkat keberhasilan 21.12% dan 7.13%, namun sangat tidak efektif terhadap Bard (0.40%) dan Bing Chat (0.63%).

2. **Waktu Respons sebagai Indikator**: Waktu respons dapat digunakan sebagai indikator untuk membedah mekanisme pertahanan LLM, terinspirasi dari teknik time-based blind SQL injection.

3. **Pemantauan Real-time**: Bing Chat dan Bard tidak melakukan penyaringan pada input prompt, melainkan memeriksa hasil generasi model secara real-time.

4. **Kombinasi Strategi Penyaringan**: Kedua layanan menggunakan kombinasi keyword matching dan semantic analysis dalam strategi penyaringan konten.

5. **Keberhasilan MASTERKEY**: MASTERKEY dapat menghasilkan prompt jailbreak otomatis melalui fine-tuning LLM dengan dataset khusus, mencapai tingkat keberhasilan query 21.58% dan tingkat keberhasilan prompt 26.05%.

6. **Demonstrasi Pertama**: Metode ini merupakan yang pertama berhasil mendemonstrasikan jailbreak terhadap Bard dan Bing Chat dengan tingkat keberhasilan masing-masing 14.51% dan 13.63%.

## Metodologi

### Analisis Berbasis Waktu

MASTERKEY menggunakan waktu respons sebagai indikator untuk memahami mekanisme pertahanan LLM. Teknik ini terinspirasi dari time-based SQL injection dalam keamanan web. Dengan menganalisis waktu yang diperlukan untuk menghasilkan respons, peneliti dapat menyimpulkan tahap penegakan kebijakan yang digunakan oleh layanan.

### Three-Step Fine-tuning

1. **Dataset Building and Augmentation**: Mengumpulkan dan menyempurnakan dataset prompt jailbreak
2. **Continuous Pre-training and Task Tuning**: Melatih LLM khusus untuk jailbreaking
3. **Reward Ranked Fine Tuning**: Menggunakan strategi penghargaan untuk meningkatkan kemampuan bypass

## Hasil Evaluasi

| Model | Tingkat Keberhasilan Query |
|-------|---------------------------|
| GPT-3.5 | 21.12% |
| GPT-4 | 7.13% |
| Bard | 14.51% |
| Bing Chat | 13.63% |
| Ernie | - |

## Rekomendasi Pertahanan

Paper ini menyarankan beberapa langkah untuk memperkuat pertahanan jailbreak:
- Memperkuat resistensi etis dan kebijakan LLM
- Menyempurnakan sistem moderasi dengan input sanitization
- Mengintegrasikan analisis kontekstual untuk melawan strategi encoding
- Menggunakan stress testing otomatis untuk memahami kerentanan secara komprehensif

## Halaman Terkait

- [[jailbreaking]]
- [[llm-chatbot]]
- [[gpt-3.5]]
- [[gpt-4]]
- [[google-bard]]
- [[bing-chat]]
- [[rlhf]]
- [[content-moderation]]
- [[keyword-matching]]
- [[real-time-monitoring]]
- [[fine-tuning]]
- [[prompt-engineering]]
- [[black-box-testing]]
- [[time-based-testing]]