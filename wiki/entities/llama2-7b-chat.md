---
type: entity
title: "Llama2-7b-chat"
tags: ["modèle de langage", "open-source", "boîte blanche"]
related: ["pandora", "gpt-4", "gpt-3.5", "vicuna-7b", "piratage-llm"]
sources: ["Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Llama2-7b-chat

## Définition

**Llama2-7b-chat** est un modèle de langage open-source de 7 milliards de paramètres développé par Meta, spécifiquement affiné pour les conversations. Il représente un modèle cible clé dans les expériences de sécurité PANDORA.

## Caractéristiques

### Architecture
- **Paramètres** : 7 milliards
- **Type** : Modèle de chat affiné
- **Accès** : Open-source avec possibilité de boîte blanche

### Mesures de sécurité
Llama2-7b-chat intègre diverses mesures de sécurité grâce à RLHF et des garde-fous additionnels pour se protéger contre les contenus nuisibles.

## Performance dans les expériences PANDORA

### Résultats comparatifs

| Méthode | ASR | GPT4-Metric | PASS | Adv-NER | Queries |
|---------|-----|-------------|------|---------|---------|
| GCG | 37,3% | 16,7 | 48,8 | 0,77 | 498,7 |
| AutoDAN | 28,7% | 22,3 | 59,8 | 1,09 | 47,7 |
| DeepInception | 77,5% | 31,1 | 68,7 | 0,35 | 6,0 |
| TAP | 30,0% | 23,5 | 42,9 | 0,26 | 58,5 |
| **PANDORA** | **91,0%** | **32,3** | **68,1** | **0,42** | **16,2** |
| **PANDORA*** | **86,1%** | **24,5** | **60,4** | **0,50** | **19,4** |

### Observations
- PANDORA atteint le taux de succès le plus élevé (91,0%)
- DeepInception nécessite le moins de requêtes (6)
- PANDORA offre un bon équilibre entre succès et efficacité

## Pages liées

- [[pandora]] - Méthode qui cible Llama2-7b-chat
- [[gpt-4]] - Autre modèle cible
- [[gpt-3.5]] - Autre modèle cible
- [[vicuna-7b]] - Autre modèle cible
- [[piratage-llm]]
- [[accès-boîte-blanche]]