---
type: entity
title: COLD (Energy-based Constrained Decoding with Langevin Dynamics)
tags: ["method", "controllable-text-generation", "energy-based"]
related: ["cold-attack", "langevin-dynamics", "energy-functions", "controllable-text-generation", "lianhui-qin"]
sources: ["Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md"]
created: 2024-01-01
updated: 2024-01-01
---
# COLD (Energy-based Constrained Decoding with Langevin Dynamics)

## Gambaran Umum

**COLD** adalah algoritma state-of-the-art dalam generasi teks terkontrol yang dikembangkan oleh Qin et al. (2022). COLD menggunakan pendekatan berbasis energi dengan Langevin Dynamics untuk menghasilkan teks yang memenuhi berbagai kendala.

## Komponen Utama

### 1. Fungsi Energi
COLD mendefinisikan fungsi energi komposisional E(y) yang menangkap berbagai kendala pada teks yang dihasilkan.

### 2. Langevin Dynamics
Menggunakan sampling berbasis gradien dalam ruang logit kontinu untuk mengoptimalkan tekst.

### 3. Proses Decoding
Menggunakan proses decoding yang dipandu oleh LLM untuk mengubah logit kontinu menjadi teks diskrit.

## Adaptasi untuk COLD-Attack

COLD-Attack mengadaptasi COLD untuk masalah generasi serangan terkontrol dengan menambahkan fungsi energi yang menangkap keberhasilan serangan.

## Halaman Terkait

- [[cold-attack]] - Adaptasi dari COLD
- [[langevin-dynamics]] - Metode sampling
- [[energy-functions]] - Komponen utama
- [[controllable-text-generation]] - Domain aplikasi
- [[lianhui-qin]] - Pengembang COLD