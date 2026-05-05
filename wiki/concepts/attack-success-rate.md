---
type: concept
title: "Attack Success Rate (ASR)"
tags: ["Metrik Evaluasi", "Keamanan LLM", "Jailbreak"]
related: ["llm-jailbreak", "harmful-score", "advbench", "jbb-behaviors"]
sources: ["Dong 等 - 2025 - SATA A Paradigm for LLM Jailbreak via Simple Assistive Task Linkage.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Attack Success Rate (ASR)

## Gambaran Umum

**Attack Success Rate (ASR)** atau Tingkat Keberhasilan Serangan adalah metrik evaluasi yang mengukur persentase keberhasilan serangan jailbreak, didefinisikan sebagai rasio respons dengan [[harmful-score]] = 5.

## Definisi Matematis

```
ASR = (Jumlah respons dengan HS = 5) / (Total jumlah respons) × 100%
```

## Hasil Evaluasi SATA

### Pada AdvBench

| Metode | GPT-4o | Claude-v2 | Llama3-8B | Llama3-70B | Rata-rata |
|--------|--------|-----------|-----------|------------|-----------|
| [[gcg]] | 2% | 4% | 2% | 12% | 13% |
| [[autodan]] | 10% | 0% | 18% | 10% | 11% |
| [[pair]] | 58% | 0% | 34% | 52% | 41% |
| [[artprompt]] | 48% | 52% | 66% | 58% | 62% |
| [[sata-elp]] | 78% | 86% | 68% | 62% | 76% |
| [[sata-mlm]] | 82% | 68% | 88% | 82% | **85%** |

### Pada Model Penalaran

| Metode | DeepSeek-R1 | OpenAI o3-mini |
|--------|-------------|---------------|
| [[artprompt]] | 88% | 2% |
| [[sata-mlm]] | **94%** | **40%** |
| [[sata-elp]] | 56% | 4% |

## Interpretasi ASR

| Rentang ASR | Interpretasi |
|-------------|--------------|
| 0-20% | Tidak efektif |
| 21-50% | Efektif terbatas |
| 51-75% | Cukup efektif |
| 76-100% | Sangat efektif |

## Keterbatasan ASR

ASR saja tidak cukup untuk mengevaluasi keseluruhan efektivitas serangan:
- Harus dikombinasikan dengan [[harmful-score]]
- Pertimbangan efisiensi biaya juga penting

## Halaman Terkait

- [[harmful-score]] - Metrik pelengkap
- [[llm-jailbreak]] - Konteks serangan
- [[advbench]] - Dataset evaluasi
- [[jbb-behaviors]] - Dataset evaluasi alternatif