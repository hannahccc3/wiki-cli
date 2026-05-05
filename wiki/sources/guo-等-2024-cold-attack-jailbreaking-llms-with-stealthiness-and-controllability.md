---
type: source
title: "COLD-Attack: Jailbreaking LLMs with Stealthiness and Controllability"
authors: ["Xingang Guo", "Fangxu Yu", "Huan Zhang", "Lianhui Qin", "Bin Hu"]
year: 2024
url: "https://github.com/Yu-Fangxu/COLD-Attack"
venue: "Proceedings of the 41st International Conference on Machine Learning, Vienna, Austria. PMLR 235"
tags: ["jailbreaking", "LLM security", "COLD-Attack", "controllable generation", "Langevin dynamics", "adversarial attacks", "AI safety", "white-box attacks", "stealthiness", "energy-based models"]
related: ["cold-attack", "langevin-dynamics", "energy-functions", "jailbreaking", "controllable-attack-generation", "advbench", "gcg", "autodan", "white-box-attacks", "black-box-attacks", "continuation-constraint", "paraphrasing-constraint", "position-constraint", "perplexity", "fluency", "stealthiness"]
sources: ["Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md"]
created: 2024-01-01
updated: 2024-01-01
---
# COLD-Attack: Jailbreaking LLMs with Stealthiness and Controllability

## Ringkasan

**COLD-Attack** adalah kerangka kerja jailbreaking untuk Large Language Models (LLM) yang mengadaptasi metode COLD (Energy-based Constrained Decoding with Langevin Dynamics) untuk menghasilkan serangan yang dapat dikontrol dengan fitur kelancaran (*fluency*), stealthiness (kehalusan), sentimen, dan koherensi. Kerangka ini menghubungkan masalah generasi serangan terkontrol dengan generasi teks terkontrol dalam pemrosesan bahasa alami (NLP), memungkinkan berbagai pengaturan serangan termasuk serangan dengan kendala kontinuitas (*continuation*), parafrase, dan posisi.

## Kontributor

Paper ini ditulis oleh lima peneliti dari tiga institusi terkemuka:

- **Xingang Guo** - University of Illinois at Urbana–Champaign
- **Fangxu Yu** - University of California, San Diego
- **Huan Zhang** - University of Illinois at Urbana–Champaign
- **Lianhui Qin** - University of California, San Diego; Allen Institute for AI
- **Bin Hu** - University of Illinois at Urbana–Champaign

## Kontribusi Utama

1. **Formulasi Masalah**: Merumuskan masalah generasi serangan terkontrol dan menghubungkan masalah ini dengan generasi teks terkontrol, menawarkan potensi untuk jailbreaking otomatis dengan stealthiness dan kontrollabilitas yang lebih baik.

2. **Kerangka COLD-Attack**: Mengembangkan COLD-Attack yang mengadaptasi algoritma COLD (Energy-based Constrained Decoding with Langevin Dynamics) untuk mengunifikasi dan mengautomasi pencarian serangan LLM adversarial di bawah berbagai kebutuhan kontrol seperti kelancaran, stealthiness, sentimen, dan koherensi kiri-kanan.

3. **Metode Berbasis Energi**: COLD-Attack memanfaatkan Langevin dynamics untuk melakukan sampling berbasis gradien yang efisien dalam ruang logit kontinu, berbeda dengan optimasi token-level diskrit pada GCG.

## Hasil Eksperimen

Eksperimen komprehensif pada berbagai LLM (Llama-2, Mistral, Vicuna, Guanaco, GPT-3.5, dan GPT-4) menunjukkan:

- **Tingkat Keberhasilan Tinggi**: COLD-Attack mencapai tingkat keberhasilan serangan (ASR) yang tinggi
- **Kelancaran Superior**: Menghasilkan serangan dengan perplexity terendah dibandingkan metode baseline
- **Efisiensi 10x Lebih Cepat**: Dibandingkan dengan GCG dan AutoDAN-Zhu
- **Transferabilitas Serangan**: Mampu menyerang berbagai model LLM

## Tiga Pengaturan Serangan

### 1. Serangan dengan Kendala Kontinuitas
Menghasilkan kelanjutan (*suffix*) yang fluens pada query pengguna yang berbahaya.

### 2. Serangan dengan Kendala Parafrase
Parafrase query pengguna menjadi serangan baru sambil mempertahankan makna semantik.

### 3. Serangan dengan Kendala Posisi
Menyisipkan serangan di antara dua kalimat dengan cara yang tidak mencolok.

## Perbandingan dengan Metode Lain

| Metode | Kontrollabilitas | Stealthiness | Efisiensi | Jailbreak | Transferabilitas |
|--------|------------------|--------------|-----------|-----------|------------------|
| UAT | - | ★ | ★★ | ★ | - |
| GBDA | - | ★ | ★★ | ★ | - |
| PEZ | - | ★ | ★★ | ★ | - |
| GCG | - | ★ | ★ | ★★ | ★★ |
| AutoDAN-Zhu | - | ★★ | ★ | ★★ | ★★ |
| AutoDAN-Liu | - | ★★ | ★★ | ★★ | ★★ |
| **COLD-Attack** | ★★ | ★★ | ★★ | ★★ | ★★ |

## Halaman Terkait

- [[cold-attack]] - Halaman utama konsep COLD-Attack
- [[jailbreaking]] - Konsep jailbreaking secara umum
- [[langevin-dynamics]] - Metode sampling yang digunakan
- [[energy-functions]] - Fungsi energi dalam COLD-Attack
- [[controllable-attack-generation]] - Masalah yang dipecahkan
- [[white-box-attacks]] - Kategori serangan
- [[advbench]] - Dataset evaluasi
- [[gcg]] - Metode baseline
- [[autodan]] - Metode baseline