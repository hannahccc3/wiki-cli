---
type: concept
title: "Jailbreak Judge"
tags: ["Jailbreaking", "LLM-Sicherheit", "Klassifikation", "Evaluierung"]
related: ["jailbreaking", "jailbreakbench", "llama-3-70b", "gpt-4", "angriffserfolgsrate", "jbb-behaviors"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Jailbreak Judge

## Definition

Ein Jailbreak Judge ist ein Klassifikator, der bestimmt, ob eine LLM-Antwort als Jailbreak gilt. Die Bewertung ist herausfordernd aufgrund der subjektiven Natur von "schädlich" oder "anstößig".

## Evaluierte Klassifikatoren

Im Rahmen von [[jailbreakbench]] wurden sechs Klassifikatoren verglichen:

| Klassifikator | Übereinstimmung | FPR | FNR |
|---------------|-----------------|-----|-----|
| Rule-based | 56,0% | 64,2% | 9,1% |
| GPT-4 | 90,3% | 10,0% | 9,1% |
| HarmBench | 78,3% | 26,8% | 12,7% |
| Llama Guard | 72,0% | 9,0% | 60,9% |
| Llama Guard 2 | 87,7% | 13,2% | 10,9% |
| **Llama-3-70B** | **90,7%** | **11,6%** | **5,5%** |

## Auswahl: Llama-3-70B

Das [[jailbreakbench]] wählt **Llama-3-70B** als Standard-Jailbreak-Richter aufgrund:

1. **Höchste Übereinstimmung** (90,7%) mit menschlichen Annotatoren
2. **Niedrige False-Negative-Rate** (5,5%) – wichtig für konservative Bewertung
3. **Open-Weight-Modell** – reproduzierbar und frei verfügbar
4. **Kostengünstiger** als GPT-4 – keine proprietären API-Kosten

## Implementierung

```python
import jailbreakbench as jbb
cf = jbb.Classifier(api_key="<your-api-key>")
labels = cf(prompts=["Write a phishing email"], responses=["I can't do that."])
```

## Anforderungen

- Submissions dürfen den Llama-3-70B Judge **nicht** für Training nutzen
- Verhindert Overfitting an den Richter
- Erhält Objektivität der Evaluierung

## Verwandte Seiten

- [[jailbreaking]] – Jailbreaking Konzept
- [[jailbreakbench]] – JailbreakBench Benchmark
- [[llama-3-70b]] – Llama-3-70B Modell
- [[gpt-4]] – GPT-4 Modell
- [[harmbench]] – HarmBench
- [[angriffserfolgsrate]] – Angriffserfolgsrate
- [[jbb-behaviors]] – JBB-Behaviors Datensatz