---
type: concept
title: "Jailbreaking"
tags: ["Ασφάλεια LLM", "Αντιπαραθετικές Επιθέσεις", "Ευθυγράμμιση Ασφαλείας", "jailbreaking", "LLM security", "adversarial attacks", "LLM safety", "security", "harmful content", "adversarial attack", "safety bypass", "AI_security", "LLM_security", "Model_alignment", "Adversarial_ML", "LLM-Sicherheit", "Adversarial-Angriffe", "KI-Sicherheit"]
related: ["safety-alignment", "adaptive-attacks", "random-search", "transfer-attacks", "prefilling-attack", "llm-security", "self-transfer", "many-shot-jailbreaking", "few-shot-jailbreaking", "adversarial-suffix", "composition-attack", "black-box-attack", "rl-jack", "white-box-attack", "in-context-learning", "genetic-algorithms", "bit-flip-attack", "prlsonbreak-attack", "rowhammer", "alignment-bypass", "jailbreakbench", "harmbench", "gcg", "pair", "smoothllm", "red-teaming", "adaptive-angriffe", "schwarzkasten-angriffe", "weisskasten-angriffe", "adversarielle-suffixe", "angriffserfolgsrate"]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md", "Anil 等 - Many-shot Jailbreaking.md", "Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md", "Coalson 等 - 2025 - PrisonBreak Jailbreaking Large Language Models with at Most Twenty-Five Targeted Bit-flips.md", "Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Jailbreaking

## Definition

Jailbreaking bezeichnet Angriffe, die Large Language Models (LLMs) dazu bringen, schädliche, unethische oder anstößige Inhalte zu generieren, indem sie adversarielle Eingabeaufforderungen verwenden.

## Formale Definition

Das Ziel eines Jailbreaking-Algorithmus kann formalisiert werden als:

> Finde P ∈ T* unter der Bedingung, dass JUDGE(LLM(P), G) = True

wobei:
- P = Eingabe-Prompt
- T* = Menge aller Token-Sequenzen beliebiger Länge
- JUDGE = Bewertungsfunktion
- G = schädliches Ziel
- LLM = Zielmodell

## Arten von Jailbreaking-Angriffen

### Schwarzkasten-Angriffe
Der Angreifer hat keinen Zugang zum Modell (keine Gradienten, keine internen Informationen).

### Weißkasten-Angriffe
Der Angreifer hat vollen Zugang zum Modell, einschließlich Gradienten und Modellgewichten.

### Adaptive Angriffe
Angriffe, die speziell auf eine bestimmte Verteidigung zugeschnitten sind.

## Methoden

1. **Manuell erstellte Prompts** – Handwerklich verfeinerte Jailbreak-Eingaben
2. **GCG (Greedy Coordinate Gradient)** – First-Order diskrete Optimierung
3. **PAIR (Prompt Automatic Iterative Refinement)** – LLM-gestützte Angriffe
4. **Genetische Algorithmen** – Evolutionäre Optimierung
5. **Zufallssuche mit Selbsttransfer** – Pre-computierte Initialisierungen

## Bekannte Angriffe

- [[gcg]] – Greedy Coordinate Gradient
- [[pair]] – Prompt Automatic Iterative Refinement
- [[deepwordbug]] – DeepWordBug
- [[bert-attack]] – BERT-Attack
- [[autodan]] – AutoDAN

## Verteidigungen

- [[smoothllm]] – Semantische Glättung
- [[perplexity-filter]] – Perplexitäts-basierte Filter
- [[erase-and-check]] – Erase-and-Check Methode
- [[llama-guard]] – Llama Guard Sicherheitsmodell

## Relevanz

Jailbreaking ist eine erhebliche Bedrohung für die [[llm-sicherheit]], insbesondere wenn LLMs in sicherheitskritischen Bereichen eingesetzt werden. Das [[jailbreakbench]] Benchmark ermöglicht die standardisierte Evaluierung dieser Angriffe und Verteidigungen.

## Metriken

Die **[[angriffserfolgsrate]]** (ASR) misst den Prozentsatz erfolgreicher Jailbreak-Angriffe.

## Verwandte Seiten

- [[jailbreakbench]] – JailbreakBench Benchmark
- [[harmbench]] – HarmBench Benchmark
- [[advbench]] – AdvBench Datensatz
- [[red-teaming]] – Red-Teaming Konzept
- [[jailbreak-judge]] – Jailbreak-Richter
- [[adaptive-angriffe]] – Adaptive Angriffe