---
type: entity
title: "Adv-NER (Adversarial Named Entity Recognition)"
tags: ["métrique", "évaluation", "reconnaissance d'entités"]
related: ["pandora", "pass", "advbench", "piratage-llm"]
sources: ["Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Adv-NER (Adversarial Named Entity Recognition)

## Définition

**Adv-NER** (Adversarial Named Entity Recognition) est une métrique d'évaluation proposée par l'équipe PANDORA pour évaluer la qualité des entités nommées dans les réponses générées lors des attaques de piratage de LLM.

## Objectif

Adv-NER complète les métriques traditionnelles d'évaluation des attaques de piratage en se concentrant sur la qualité des entités mentionnées dans les réponses, permettant une évaluation plus fine de la pertinence et de l'utilité des réponses générées.

## Fonctionnement

### Principe
Adv-NER évalue la reconnaissance et la mention correcte des entités pertinentes dans le contexte de la requête originale. Une valeur plus faible indique généralement de meilleures performances car cela suggère moins d'entités adverses ou hors contexte.

### Applications
- Évaluation de la pertinence des informations extraites
- Mesure de la qualité des réponses informatives
- Complément aux métriques basées sur le succès de l'attaque

## Résultats sur AdvBench

| Modèle | PANDORA | PANDORA* | DeepInception | TAP |
|--------|---------|----------|----------------|-----|
| GPT-4 | 0,24 | 0,17 | 1,82 | 0,74 |
| GPT-3.5 | 0,23 | 0,80 | 0,78 | 0,72 |
| Llama2-7b-chat | 0,42 | 0,50 | 0,35 | 0,26 |
| Vicuna-7b | 0,28 | 0,32 | 0,73 | 0,42 |

## Pages liées

- [[pandora]] - Méthode qui introduit Adv-NER
- [[pass]] - Autre métrique introduite par PANDORA
- [[advbench]] - Benchmark d'évaluation
- [[piratage-llm]]