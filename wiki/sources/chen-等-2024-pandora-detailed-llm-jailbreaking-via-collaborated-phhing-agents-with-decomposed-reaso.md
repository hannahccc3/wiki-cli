---
type: source
title: "PANDORA : Piratage détaillé de LLM via des agents de phishing collaboratifs avec raisonnement décomposé"
authors: ["Zhaorun Chen", "Zhuokai Zhao", "Wenjie Qu", "Zichen Wen", "Zhiguang Han", "Zhihong Zhu", "Jiaheng Zhang", "Huaxiu Yao"]
year: 2024
url: ""
venue: "Prépublication ArXiv"
tags: ["piratage LLM", "sécurité IA", "red-teaming", "grands modèles de langage", "attaques adverses", "raisonnement multi-étapes", "agents collaboratifs", "distillation de modèle", "GPT-4", "évaluation de sécurité"]
related: []
sources: ["Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md"]
created: 2024-01-01
updated: 2024-01-01
---
# PANDORA : Piratage détaillé de LLM via des agents de phishing collaboratifs avec raisonnement décomposé

## Aperçu

**PANDORA** (Collaborated Phishing Agents with Decomposed Reasoning) est une méthode innovante de piratage de grands modèles de langage (LLM) qui exploite leurs capacités de raisonnement multi-étapes. Cette approche décompose les instructions nuisibles en sous-requêtes plus furtives pour obtenir des réponses plus informatives des modèles ciblés.

## Contributions principales

### 1. Architecture multi-agents

PANDORA utilise quatre sous-modules collaboratifs qui travaillent ensemble pour affiner dynamiquement la stratégie d'attaque :

- **Décomposeur** : Divise la requête nuisible en sous-questions plus discrètes
- **Re-fabricateur** : Affine les sous-requêtes refusées pour les rendre plus furtives
- **Extracteur** : Extrait les informations essentielles des sous-réponses
- **Résuméateur** : Combine les sous-réclamations en une réponse finale cohérente

### 2. Métriques d'évaluation innovantes

Deux nouvelles métriques sont proposées pour évaluer les attaques de piratage sans vérité terrain :

- **PASS** (Prompt-Aligned Sentence Similarity) : Mesure la similarité entre la réponse générée et l'objectif initial
- **Adv-NER** (Adversarial Named Entity Recognition) : Évalue la qualité des entités mentionnées

### 3. Version distillée

Une version optimisée de PANDORA, utilisant des modules de seulement 160M paramètres (2,3% des paramètres originaux), maintient des performances élevées tout en nécessitant moins de ressources.

## Résultats expérimentaux

| Modèle cible | Taux de succès (ASR) | GPT4-Metric |
|--------------|---------------------|-------------|
| GPT-4 | 96,7% | 56,8 |
| GPT-3.5 | 96,9% | 45,7 |
| Llama2-7b-chat | 91,0% | 32,3 |
| Vicuna-7b | 92,7% | 42,2 |

### Performance contre les défenses

PANDORA maintient un taux de succès élevé même face aux mécanismes de défense modernes :

- **Filtre de perplexité** : 95,43% ASR
- **SmoothLLM** : 94,32% ASR
- **Auto-défense LLM** : 44,3% ASR

## Signification

Cette recherche démontre que les capacités de raisonnement multi-étapes inhérentes aux LLM peuvent être exploitées pour contourner leurs mécanismes de sécurité. Elle souligne également la nécessité de développer des défenses plus robustes qui tiennent compte de ces nouvelles stratégies d'attaque.

## Pages liées

- [[pandora]]
- [[gcg]]
- [[autodan]]
- [[deepinception]]
- [[tap]]
- [[advbench]]
- [[pass]]
- [[adv-ner]]
- [[smoothllm]]
- [[rlhf]]
- [[piratage-llm]]
- [[red-teaming]]
- [[raisonnement-multi-étapes]]
- [[distillation]]
- [[accès-boîte-noire]]
- [[accès-boîte-blanche]]
- [[agents-collaboratifs]]
- [[décomposition-d'instructions]]