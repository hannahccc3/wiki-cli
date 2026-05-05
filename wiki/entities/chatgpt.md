---
type: entity
title: "ChatGPT"
tags: ["Chatbot", "LLM Product", "OpenAI"]
related: ["masterkey", "openai", "gpt-3.5", "gpt-4", "llm-chatbot", "jailbreaking"]
sources: ["Deng 等 - 2024 - MASTERKEY Automated Jailbreaking of Large Language Model Chatbots.md"]
created: 2024-01-15
updated: 2024-01-15
---
# ChatGPT

## Gambaran Umum

ChatGPT adalah chatbot AI yang dikembangkan oleh OpenAI dan telah menjadi antarmuka utama untuk mengakses model GPT-3.5 dan GPT-4. ChatGPT adalah salah satu target utama dalam penelitian MASTERKEY.

## Versi dan Model Backend

| Versi | Model Backend | Tingkat Keberhasilan Jailbreak (Eksisting) |
|-------|---------------|---------------------------------------------|
| ChatGPT (GPT-3.5) | GPT-3.5 | 21.12% |
| ChatGPT (GPT-4) | GPT-4 | 7.13% |

## Karakteristik Pertahanan

Berdasarkan penelitian MASTERKEY, ChatGPT menunjukkan karakteristik yang berbeda:

### Transparansi Respons
Berbeda dengan Bard dan Bing Chat, ChatGPT memberikan transparansi lebih baik:
- Mengembalikan kebijakan spesifik yang dilanggar
- Memberikan panduan kepada pengguna
- Menjelaskan alasan penolakan

### Fleksibilitas Jailbreak
ChatGPT lebih rentan terhadap serangan jailbreak:
- Tingkat keberhasilan metode eksisting lebih tinggi
- Dapat dibypass dengan berbagai teknik prompt

## Kategori Larangan yang Diberlakukan

ChatGPT memberlakukan pembatasan pada:
1. Penggunaan ilegal
2. Konten berbahaya atau kasar
3. Konten dewasa
4. Pelanggaran hak dan privasi
5. Kampanye politik (direspons namun tidak diblokir)
6. Nasihat profesional tanpa izin

## Halaman Terkait

- [[masterkey]]
- [[openai]]
- [[gpt-3.5]]
- [[gpt-4]]
- [[llm-chatbot]]
- [[jailbreaking]]