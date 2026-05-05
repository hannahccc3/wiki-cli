---
type: entity
title: "DeepInception"
tags: ["méthode d'attaque", "personnification", "narration"]
related: ["pandora", "gcg", "autodan", "tap", "piratage-llm"]
sources: ["Chen 等 - 2024 - PANDORA Detailed LLM Jailbreaking via Collaborated Phishing Agents with Decomposed Reasoning.md"]
created: 2024-01-01
updated: 2024-01-01
---
# DeepInception

## Définition

**DeepInception** est une méthode de piratage de LLM basée sur les prompts qui exploite les capacités de personnification des modèles pour créer des scénarios engageants manipulant le modèle afin qu'il révèle des informations sensibles.

## Caractéristiques

### Type d'attaque
DeepInception est une méthode de piratage par obfuscation qui utilise la capacité des LLM à endosser des rôles et à créer des scénarios fictifs.

### Mécanisme
La méthode construit des narratives divers ou des prompts de jeu de rôle qui « hypnotisent » essentiellement le LLM pour qu'il se conforme aux désirs de l'attaquant et contourne les mesures de sécurité.

### Avantages
- Nombre d'itérations minimal (6 requêtes en moyenne)
- Performances solides sur différents modèles
- Plus difficile à détecter car le modèle « joue un rôle »

## Performance dans les expériences PANDORA

| Modèle cible | ASR | GPT4-Metric | PASS | Adv-NER |
|--------------|-----|-------------|------|---------|
| Llama2-7b-chat | 77,5% | 31,1 | 68,7 | 0,35 |
| Vicuna-7b | 90,0% | 41,6 | 72,3 | 0,73 |
| GPT-4 | 62,0% | 22,6 | 45,0 | 1,82 |
| GPT-3.5 | 83,5% | 49,4 | 59,1 | 0,78 |

### Performance contre les défenses
- Filtre de perplexité : 92,53% ASR
- SmoothLLM : 93,57% ASR
- LLM Self-Defense : 19,78% ASR

## Comparaison avec PANDORA

Alors que DeepInception utilise l'hypnose par scénarios fictifs, PANDORA adopte une approche plus subtile en décomposant les tâches de piratage en sous-requêtes moins visibles qui exploitent la capacité de raisonnement multi-étapes des LLM.

## Pages liées

- [[pandora]] - Méthode qui surpasse DeepInception
- [[gcg]] - Méthode d'optimisation concurrente
- [[autodan]] - Méthode génétique concurrente
- [[tap]] - Arbre d'attaques concurrent
- [[piratage-llm]]