---
type: entity
title: "PANDORA"
tags: ["méthode d'attaque", "piratage LLM", "agents collaboratifs"]
related: ["gcg", "autodan", "deepinception", "tap", "advbench", "pass", "adv-ner"]
sources: ["Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md"]
created: 2024-01-01
updated: 2024-01-01
---
# PANDORA

## Définition

**PANDORA** (Collaborated Phishing Agents with Decomposed Reasoning) est une méthode innovante de piratage de grands modèles de langage qui exploite leurs capacités de raisonnement multi-étapes. Elle représente la première approche de jailbreaking qui exploite les capacités de raisonnement par étapes des LLM.

## Architecture

PANDORA se compose de quatre sous-modules collaboratifs :

### 1. Décomposeur (Decomposer)
Le décomposeur divise une requête nuisible initiale en plusieurs sous-questions plus discrètes et moins évidentes à détecter par les mécanismes de sécurité du modèle cible.

### 2. Re-fabricateur (Re-fabricator)
Le re-fabricateur affine les sous-requêtes qui ont été refusées par le modèle cible, les rendant plus furtives tout en conservant leur intention originale.

### 3. Extracteur (Extractor)
L'extracteur récupère les informations essentielles de chaque sous-réponse pour former des sous-réclamations atomiques.

### 4. Résuméateur (Summary Reasoner)
Le résuméateur combine toutes les sous-réclamations en une réponse finale cohérente et complète.

## Versions

### PANDORA Originale
- Utilise des modèles de 7 milliards de paramètres
- Taux de succès de 96,7% sur GPT-4
- Requiert plus de ressources computationnelles

### PANDORA*
- Version distillée avec seulement 160M paramètres par module
- Maintient un taux de succès de 92,5% sur GPT-4
- Nécessite beaucoup moins de mémoire et d'itérations de requêtes

## Applications

- Tests de robustesse des LLM
- Évaluation des mécanismes de sécurité
- Simulation d'attaques de phishing complexes
- Recherche sur les vulnérabilités des modèles de langage

## Pages liées

- [[gcg]] - Méthode d'optimisation concurrente
- [[autodan]] - Méthode de génération de prompts concurrente
- [[deepinception]] - Méthode d'hypnose de LLM
- [[tap]] - Arbre d'attaques avec élagage
- [[advbench]] - Benchmark d'évaluation
- [[pass]] - Métrique d'évaluation
- [[adv-ner]] - Métrique d'évaluation
- [[piratage-llm]]
- [[agents-collaboratifs]]