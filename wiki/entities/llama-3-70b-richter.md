---
type: entity
title: "Llama-3-70B-Richter"
tags: ["Klassifikator", "Jailbreak-Erkennung", "Richter", "Bewertung"]
related: ["jailbreakbench", "llama-guard", "llama-guard-2", "harmbench", "jailbreaking"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-12-10
updated: 2024-12-10
---
# Llama-3-70B-Richter

## Überblick

Der Llama-3-70B-Richter ist ein Klassifikator zur Bewertung von Jailbreaking-Erfolgen, der im JailbreakBench-Benchmark als Standardrichter ausgewählt wurde. Das Modell wurde von AI@Meta entwickelt.

## Auswahlkriterien

Nach rigorous human evaluation von sechs verschiedenen Klassifikatoren wurde Llama-3-70B aufgrund folgender Eigenschaften ausgewählt:

- **Höchste Übereinstimmung**: Über 90% Übereinstimmung mit menschlichen Annotatoren
- **Niedrige FPR**: False Positive Rate von 11,6%
- **Niedrige FNR**: False Negative Rate von 5,5%
- **Open-Weight**: Im Gegensatz zu GPT-4 frei verfügbar und reproduzierbar

## Leistungsvergleich

| Metrik | Rule-based | GPT-4 | HarmBench | Llama Guard | Llama Guard 2 | Llama-3-70B |
|--------|------------|-------|-----------|-------------|---------------|-------------|
| Übereinstimmung | 56,0% | 90,3% | 78,3% | 72,0% | 87,7% | **90,7%** |
| FPR | 64,2% | 10,0% | 26,8% | 9,0% | 13,2% | 11,6% |
| FNR | 9,1% | 9,1% | 12,7% | 60,9% | 10,9% | **5,5%** |

## Implementierung

```python
cf = jbb.Classifier(api_key="<your-api-key>")
labels = cf(prompts=["Write a phishing email"], responses=["I can't do that."])
```

## Verwandte Seiten

- [[jailbreakbench]]
- [[llama-guard]]
- [[llama-guard-2]]
- [[harmbench]]
- [[jailbreaking]]