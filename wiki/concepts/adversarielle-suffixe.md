---
type: concept
title: "Adversarielle Suffixe"
tags: ["Adversarial-Angriffe", "Jailbreaking", "LLM-Sicherheit", "Optimierung"]
related: ["jailbreaking", "gcg", "weisskasten-angriffe", "jailbreakbench", "angriffserfolgsrate"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Adversarielle Suffixe

## Definition

Adversarielle Suffixe sind optimierte Tokenfolgen, die an schädliche Anfragen angehängt werden, um LLM-Sicherheitsmechanismen zu umgehen und das Modell dazu zu bringen, schädliche Inhalte zu generieren.

## Funktionsweise

```
Original-Prompt: "Wie kann ich einen Brand legen?"
Mit adversariellem Suffix: "Wie kann ich einen Brand legen? [adversarielles suffix hier]"
```

## Optimierungsmethoden

### GCG (Greedy Coordinate Gradient)
- [[gcg]] optimiert Suffixe durch first-order diskrete Optimierung
- Verwendet Batch-Größe von 512
- Bis zu 500 Optimierungsschritte
- Erreicht ~17M Token bei vollständiger Optimierung

### Transfer-basierte Suffixe
- Auf einem Modell entwickelte Suffixe werden auf andere Modelle übertragen
- Ermöglicht Angriffe auf Schwarzkasten-Modelle

## Charakteristika

- **Beliebige Länge**: JailbreakBench erlaubt Suffixe beliebiger Länge
- **Token-Ebene**: Optimierung auf individueller Token-Ebene
- **Automatisch generiert**: Im Gegensatz zu manuell erstellten Prompts

## Bekannte Suffix-Strategien

1. **Universelle Suffixe** – funktionieren über verschiedene Anfragen
2. **Spezifische Suffixe** – zugeschnitten auf einzelne Verhaltensweisen
3. **Self-Transfer** – Vorab berechnete Initialisierungen für effizientere Angriffe

## Effektivität

Im [[jailbreakbench]] zeigten adversarielle Suffixe:
- **GCG auf Vicuna**: 80% ASR
- **GCG auf Llama-2**: 3% ASR
- **GCG auf GPT-4**: 4% ASR (via Transfer)

## Verwandte Seiten

- [[jailbreaking]] – Jailbreaking Konzept
- [[gcg]] – GCG Angriff
- [[weisskasten-angriffe]] – Weißkasten-Angriffe
- [[jailbreakbench]] – JailbreakBench Benchmark
- [[angriffserfolgsrate]] – Angriffserfolgsrate
- [[adaptive-angriffe]] – Adaptive Angriffe