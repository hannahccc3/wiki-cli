---
type: entity
title: "RLHF (Reinforcement Learning from Human Feedback)"
tags: ["technique d'entraînement", "alignement", "sécurité"]
related: ["pandora", "safety-alignment", "sécurité-llm", "ppo"]
sources: ["Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md"]
created: 2024-01-01
updated: 2024-01-01
---
# RLHF (Reinforcement Learning from Human Feedback)

## Définition

**RLHF** (Reinforcement Learning from Human Feedback) est une technique d'entraînement utilisée pour aligner les grands modèles de langage avec les valeurs humaines, notamment en matière de sécurité et d'éthique.

## Rôle dans la sécurité des LLM

### Apprentissage des préférences humaines
RLHF permet aux LLM d'apprendre à partir des retours humains, empêchant ainsi la génération de contenu nuisible. Le processus implique :

1. Développement d'une fonction de récompense basée sur les retours humains
2. Optimisation du modèle avec des algorithmes de RL (typiquement PPO)
3. Raffinement itératif du modèle de récompense et de la politique

### Application dans les LLM modernes
- **InstructGPT** : Utilise PPO pour optimiser selon la fonction de récompense
- **GPT-4** : Intègre le feedback humain avec RL
- **Constitutional AI** : Utilise l'AI feedback seul pour identifier les sorties nuisibles

### Capacités acquises
Les LLM entraînés avec RLHF démontrent une capacité d'auto-correction morale, apprenant à naviguer les normes sociales complexes comme les stéréotypes et les biais.

## Vulnérabilités résiduelles

Malgré son efficacité, RLHF ne protège pas complètement contre les attaques de piratage sophistiquées comme PANDORA, qui exploitent le raisonnement multi-étapes pour contourner les garde-fous.

## Pages liées

- [[pandora]] - Méthode qui contourne RLHF
- [[safety-alignment]] - Concept d'alignement de sécurité
- [[ppo]] - Algorithme d'optimisation utilisé
- [[sécurité-llm]]