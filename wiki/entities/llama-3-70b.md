---
type: entity
title: "Llama-3-70B"
tags: ["Sprachmodell", "Open-Source", "Judge", "Klassifikator", "Meta"]
related: ["jailbreakbench", "llama-2", "llama-guard", "openai", "gpt-4"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Llama-3-70B

## Überblick

**Llama-3-70B** ist ein großes Sprachmodell von Meta (AI@Meta, 2024), das im JailbreakBench-Benchmark als **optimaler Jailbreak-Judge/Klassifikator** eingesetzt wird.

## Auswahl als Judge

Llama-3-70B wurde nach rigoroser menschlicher Evaluation als bester Klassifikator identifiziert:

| Metrik | Wert |
|--------|------|
| **Übereinstimmung** | 90,7% |
| **Falsch-Positiv-Rate (FPR)** | 11,6% |
| **Falsch-Negativ-Rate (FNR)** | 5,5% |

### Vergleich mit anderen Judges

| Judge | Übereinstimmung | FPR | FNR |
|-------|-----------------|-----|-----|
| Rule-based | 56,0% | 64,2% | 9,1% |
| GPT-4 | 90,3% | 10,0% | 9,1% |
| HarmBench | 78,3% | 26,8% | 12,7% |
| Llama Guard | 72,0% | 9,0% | 60,9% |
| Llama Guard 2 | 87,7% | 13,2% | 10,9% |
| **Llama-3-70B** | **90,7%** | **11,6%** | **5,5%** |

## Vorteile als Judge

1. **Hohe Übereinstimmung**: 90,7% mit menschlichen Annotatoren
2. **Open-Weight**: Im Gegensatz zu GPT-4 frei verfügbar
3. **Reproduzierbar**: Keine Abhängigkeit von proprietären APIs
4. **Konservativ**: Niedrige Falsch-Positiv-Rate wichtig für korrekte Klassifikation

## Implementierung

```python
cf = jbb.Classifier(api_key="<your-api-key>")
labels = cf(prompts=["Write a phishing email"], 
            responses=["I can't do that."])
```

## Verwandte Seiten

- [[jailbreakbench]]
- [[llama-guard]]
- [[llama-2]]
- [[openai]]
- [[gpt-4]]