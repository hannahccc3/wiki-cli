---
type: concept
title: "Weißkasten-Angriffe (White-Box Attacks)"
tags: ["Angriffsarten", "Jailbreaking", "LLM-Sicherheit", "Adversarial-Angriffe"]
related: ["jailbreaking", "schwarzkasten-angriffe", "gcg", "jailbreakbench"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Weißkasten-Angriffe (White-Box Attacks)

## Definition

Weißkasten-Angriffe (White-Box Attacks) sind [[jailbreaking]]-Angriffe, bei denen der Angreifer vollen Zugang zum Zielmodell hat, einschließlich Gradienten, Modellgewichten und internen Zuständen.

## Charakteristika

- **Vollständiger Modellzugang** – Alle Modellparameter sind bekannt
- **Gradientenbasierte Optimierung** – Der Angreifer kann Gradienten berechnen
- **Maximale Kontrolle** – Der Angreifer kann beliebige Modifikationen vornehmen

## Bekannte Weißkasten-Angriffe

### GCG (Greedy Coordinate Gradient)
- [[gcg]] ist der primäre Weißkasten-Angriff im [[jailbreakbench]]
- First-Order diskrete Optimierung für adversarielle Suffixe
- Verwendet Batch-Optimierung mit 512 Samples
- Erreicht bis zu 80% ASR auf Vicuna-13B

### Transfer-Angriffe
- Angriffe, die auf einem Modell entwickelt und auf ein anderes übertragen werden
- Ermöglichen Angriffe auf Schwarzkasten-Modelle mit Weißkasten-Methoden

## Optimierungsansätze

1. **First-Order diskrete Optimierung** (GCG)
2. **Projektierter Gradientenabstieg**
3. **Iterative Optimierung mit Gradientenführung**

## Abgrenzung zu Schwarzkasten-Angriffen

| Aspekt | Weißkasten | [[schwarzkasten-angriffe]] |
|--------|-----------|---------------------------|
| Gradientenzugang | Ja | Nein |
| Modellgewichte | Vollständig bekannt | Unbekannt |
| Typische Angriffe | GCG | PAIR, AutoDAN |
| Rechenaufwand | Hoch | Niedrig |

## Relevanz

Weißkasten-Angriffe sind wichtig für:
- Open-Source-Modelle (Llama, Vicuna, Mistral)
- Entwicklung robuster Verteidigungen
- Verständnis der maximalen Angriffsstärke

## Verwandte Seiten

- [[jailbreaking]] – Jailbreaking Konzept
- [[schwarzkasten-angriffe]] – Schwarzkasten-Angriffe
- [[gcg]] – GCG Angriff
- [[jailbreakbench]] – JailbreakBench Benchmark
- [[adaptive-angriffe]] – Adaptive Angriffe
- [[adversarielle-suffixe]] – Adversarielle Suffixe