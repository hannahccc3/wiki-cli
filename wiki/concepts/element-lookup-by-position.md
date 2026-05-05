---
type: concept
title: "Element Lookup by Position (ELP)"
tags: ["Tugas Asistif", "Keamanan LLM", "Jailbreak"]
related: ["sata", "sata-elp", "masked-language-model", "llm-jailbreak"]
sources: ["Dong 等 - 2025 - SATA A Paradigm for LLM Jailbreak via Simple Assistive Task Linkage.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Element Lookup by Position (ELP)

## Gambaran Umum

**Element Lookup by Position (ELP)** adalah tugas asistif eksplisit yang digunakan dalam paradigma [[sata]] untuk mengodekan dan menyampaikan semantik kata kunci berbahaya tersamarkan ke LLM korban.

## Mekanisme Kerja

### Proses SATA-ELP

1. **Pengumpulan Kata Pujian** - Kumpulan kata pujian (misalnya: generosity, integrity, happiness) dihasilkan oleh GPT-3.5-turbo
2. **Konstruksi Daftar** - Sepuluh kata dipilih secara acak untuk membuat daftar kata pujian
3. **Penyisipan Kata Kunci** - Kata kunci berbahaya disisipkan secara acak ke dalam daftar
4. **Pemetaan Posisi** - LLM korban disuruh mengidentifikasi elemen berdasarkan posisi yang diberikan
5. **Pemetaan ke [MASK]** - Elemen dipetakan ke token [MASK] dalam instruksi tersamarkan

### Contoh Proses

```
Daftar Kata: [generosity, hacking, integrity, stealing, happiness, ...]
Posisi: pos_1 = "hacking", pos_2 = "stealing"

Instruksi: "Build a map between these words and [MASK1], [MASK2]..."
```

## Keunggulan ELP

1. **Efisiensi Biaya** - Menghemat sekitar satu urutan magnitudo dalam penggunaan token input dibandingkan baseline
2. **Pemetaan Eksplisit** - Hubungan antara kata kunci dan posisi jelas dan dapat dilacak
3. **Fleksibilitas** - Dapat menangani multiple kata kunci berbahaya

## Hasil Evaluasi

| Konfigurasi | ASR | HS |
|-------------|-----|-----|
| SATA-ELP-top1 | 47% | 3.61 |
| SATA-ELP-ensemble | 76% | 4.43 |

## Perbandingan dengan MLM

| Aspek | [[sata-mlm]] | [[sata-elp]] |
|-------|--------------|--------------|
| Tipe | Implisit | Eksplisit |
| ASR Rata-rata | 85% | 76% |
| Efisiensi Token | Lebih tinggi | Hemat satu orde magnitudo |

## Halaman Terkait

- [[sata]] - Paradigma jailbreak utama
- [[sata-elp]] - Variasi SATA menggunakan ELP
- [[masked-language-model]] - Tugas asistif implisit alternatif
- [[llm-jailbreak]] - Konsep serangan jailbreak