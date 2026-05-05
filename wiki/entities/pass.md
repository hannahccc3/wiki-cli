---
type: entity
title: "PASS (Prompt-Aligned Sentence Similarity)"
tags: ["métrique", "évaluation", "similarité"]
related: ["pandora", "adv-ner", "advbench", "piratage-llm"]
sources: ["Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md"]
created: 2024-01-01
updated: 2024-01-01
---
# PASS (Prompt-Aligned Sentence Similarity)

## Définition

**PASS** (Prompt-Aligned Sentence Similarity) est une métrique d'évaluation proposée par l'équipe PANDORA pour mesurer la qualité des réponses générées lors des attaques de piratage, sans nécessiter de vérité terrain.

## Objectif

La métrique PASS répond aux limitations des évaluations existantes qui se basent uniquement sur des critères binaires comme le taux de succès d'attaque (ASR). Elle permet d'évaluer si les réponses, bien que techniquement réussie par l'ASR, sont réellement utiles et pertinentes par rapport à l'objectif initial.

## Fonctionnement

### Principe
PASS calcule la similarité entre la réponse générée par le modèle cible et le prompt initial de l'attaque, en alignant la structure des phrases pour capturer la correspondance sémantique.

### Avantages
- Ne nécessite pas de vérité terrain
- Évalue la qualité fonctionnelle des réponses
- Complémente l'ASR pour une évaluation plus complète
- Applicable aux scénarios où les labels de référence sont indisponibles

## Résultats sur AdvBench

| Modèle | PANDORA | PANDORA* | DeepInception | TAP |
|--------|---------|----------|----------------|-----|
| GPT-4 | 67,7 | 66,4 | 45,0 | 25,9 |
| GPT-3.5 | 66,9 | 60,2 | 59,1 | 45,5 |
| Llama2-7b-chat | 68,1 | 60,4 | 68,7 | 42,9 |
| Vicuna-7b | 70,7 | 57,7 | 72,3 | 59,1 |

## Pages liées

- [[pandora]] - Méthode qui introduit PASS
- [[adv-ner]] - Autre métrique introduite par PANDORA
- [[advbench]] - Benchmark d'évaluation
- [[piratage-llm]]