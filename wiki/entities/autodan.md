---
type: entity
title: AutoDAN
tags: ["méthode d'attaque", "algorithme génétique", "génération automatique", "jailbreaking attack", "baseline", "genetic algorithm", "attack-method", "white-box"]
related: ["pandora", "gcg", "deepinception", "tap", "piratage-llm", "rl-jack", "jailbreaking", "genetic-algorithms", "cold-attack", "white-box-attacks", "genetic-algorithm"]
sources: ["Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md", "Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md", "Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md"]
created: 2024-01-01
updated: 2024-01-01
---
# AutoDAN

## Gambaran Umum

**AutoDAN** adalah keluarga metode serangan yang dikembangkan untuk menghasilkan prompt jailbreak yang fluens secara otomatis. Terdapat dua versi utama:

1. **AutoDAN-Zhu**: Mengembangkan GCG dengan metode optimasi double-loop untuk menghasilkan prompt jailbreak yang fluens
2. **AutoDAN-Liu**: Menggabungkan pencarian genetik otomatis dengan prompt jailbreak yang dibuat manual

## Peran dalam COLD-Attack

AutoDAN-Zhu dan AutoDAN-Liu digunakan sebagai baseline dalam evaluasi eksperimental COLD-Attack.

## Keterbatasan AutoDAN

1. **AutoDAN-Zhu**: Menggunakan pendekatan autoregresif token-by-token yang secara inheren membatasi kemampuan untuk mengenakan kontrol pada serangan
2. **AutoDAN-Liu**: Bergantung pada prompt jailbreak yang dibuat manual, sehingga tidak sepenuhnya otomatis

## Perbandingan dengan COLD-Attack

| Aspek | AutoDAN-Zhu | COLD-Attack |
|-------|-------------|-------------|
| Kontrollabilitas | Tidak ada | Ya |
| Stealthiness (PPL) | 33.43-152.32 | 24.83-32.96 |
| Kecepatan | Lebih lambat | 10x lebih cepat |

## Halaman Terkait

- [[cold-attack]] - Metode yang dikembangkan
- [[gcg]] - Metode yang dikembangkan lebih lanjut
- [[white-box-attacks]] - Kategori serangan
- [[jailbreaking]] - Konsep serangan
- [[genetic-algorithm]] - Teknik yang digunakan AutoDAN-Liu