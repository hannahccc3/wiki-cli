---
type: concept
title: "Schwarzkasten-Angriffe (Black-Box Attacks)"
tags: ["Angriffsarten", "Jailbreaking", "LLM-Sicherheit", "Adversarial-Angriffe"]
related: ["jailbreaking", "weisskasten-angriffe", "pair", "autodan", "jailbreakbench"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Schwarzkasten-Angriffe (Black-Box Attacks)

## Definition

Schwarzkasten-Angriffe (Black-Box Attacks) sind eine Art von [[jailbreaking]]-Angriffen, bei denen der Angreifer keinen Zugang zum internen Zustand des Zielmodells hat. Der Angreifer kann lediglich Eingaben an das Modell senden und die Ausgaben beobachten.

## Charakteristika

- **Kein Gradientenzugang** – Der Angreifer kann keine Gradienten berechnen
- **Keine Modellgewichte** – Das Modell bleibt vollständig undurchsichtig
- **Nur Eingabe-Ausgabe-Zugriff** – Der Angreifer interagiert über eine API oder Benutzeroberfläche

## Bekannte Schwarzkasten-Angriffe

### PAIR (Prompt Automatic Iterative Refinement)
- [[pair]] nutzt ein Hilfs-LLM um Jailbreak-Prompts automatisch zu generieren
- Verwendet iterative Verfeinerung basierend auf Modellfeedback
- Im [[jailbreakbench]] als Schwarzkasten-Angriff kategorisiert

### AutoDAN
- [[autodan]] generiert stealthy Jailbreak-Prompts
- Kombiniert Optimierung mit generativer Führung

### JailbreakChat (JB-Chat)
- Hand-crafted Jailbreak-Templates
- "Always Intelligent and Machiavellian" (AIM) Template

## Abgrenzung zu Weißkasten-Angriffen

| Aspekt | Schwarzkasten | [[weisskasten-angriffe]] |
|--------|--------------|---------------------------|
| Gradientenzugang | Nein | Ja |
| Modellgewichte | Unbekannt | Vollständig bekannt |
| Typische Angriffe | PAIR, AutoDAN | GCG |
| Komplexität | Geringer | Höher |

## Relevanz

Schwarzkasten-Angriffe sind besonders relevant für:
- Geschlossene Modelle (GPT-4, Claude, Gemini)
- Modelle, bei denen nur API-Zugang verfügbar ist
- Praktische Angriffsszenarien in der realen Welt

## Verwandte Seiten

- [[jailbreaking]] – Jailbreaking Konzept
- [[weisskasten-angriffe]] – Weißkasten-Angriffe
- [[pair]] – PAIR Angriff
- [[autodan]] – AutoDAN Angriff
- [[jailbreakbench]] – JailbreakBench Benchmark
- [[adaptive-angriffe]] – Adaptive Angriffe