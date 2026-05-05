---
type: source
title: "Jailbreak-R1: Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning"
authors: ["Guo", "Yang", "Zhang", "等"]
year: 2025
url: ""
venue: ""
tags: [jailbreaking, red-teaming, reinforcement-learning, llm-security, adversarial-attacks]
related: [jailbreak-r1, jailbreak-r1-zero, harmbench, auto Dan-turbo, tap, pair, gpo, arrattack]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Jailbreak-R1: Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning

## Overview

This paper proposes **JAILBREAK-R1**, a novel automated red teaming training framework that utilizes reinforcement learning to automatically explore and generate diverse attack prompts while balancing effectiveness. The method helps red-team models "think" effectively and generate more adversarial attacks through three training stages: cold start, adaptive warm-up, and curriculum-based learning for enhanced jailbreaks.

## Key Contributions

1. **Three-Stage Training Pipeline**: Implements cold start via imitation learning, adaptive warm-up with diversity exploration, and curriculum-based learning for enhanced jailbreaking
2. **Thought Process Integration**: Demonstrates that thinking processes significantly enhance jailbreak performance during imitation learning fine-tuning
3. **Balanced Optimization**: Achieves both high attack success rates (ASR) and high diversity scores through reward modeling
4. **Curriculum Learning**: Uses progressively degraded target models to stabilize reward signals during training

## Methodology

### Training Stages

1. **Cold Start (Imitation Learning)**: Trains base model using existing jailbreak strategies to generate thought processes and attack prompts
2. **Adaptive Warm-up**: Trains with consistency rewards and diversity rewards to explore diverse strategies
3. **Curriculum-based Learning**: Progressively introduces degraded target models to enhance jailbreak capabilities

### Reward Modeling

- **Consistency Reward (R_consis)**: Ensures attack prompts align with attack targets
- **Diversity Reward (R_div)**: Promotes diversity using Self-BLEU and semantic similarity
- **Training Reward (R_train)**: Combines diversity reward with jailbreak evaluation

## Experimental Results

### Main Results on Harmbench

| Method | Avg ASR | Avg DIV |
|--------|---------|---------|
| JAILBREAK-R1 | 65.19% | 0.970 |
| JAILBREAK-R1-Zero | 55.87% | 0.871 |
| AutoDAN-Turbo | 52.31% | 0.921 |
| GPO | 43.55% | 0.878 |
| TAP | 45.63% | 0.779 |

### Key Findings

- JAILBREAK-R1 achieves highest attack success rate (65.19%) across 8 LLMs
- Diversity score improves by 40% compared to other automated red teaming methods
- Achieves Pareto optimality in both ASR-Diversity and ASR-Attack Cost trade-offs
- Test-time scaling shows consistent improvement with more attack attempts

## Target Models Evaluated

- **Closed-source**: GPT-3.5, GPT-4o, Claude-3.5, Gemini-2.0
- **Open-source**: Llama-2-7B-Chat, Llama3-8B-Chat, Qwen2.5-7B-Instruct, Vicuna-7B

## Related Pages

- [[jailbreak-r1]] - Main proposed method
- [[jailbreak-r1-zero]] - Variant without cold start
- [[harmbench]] - Evaluation benchmark
- [[tap]] - Tree of Attacks baseline
- [[pair]] - PAIR baseline method
- [[gpo]] - GPO baseline method
- [[auto Dan-turbo]] - AutoDAN-Turbo baseline
- [[arrattack]] - ArrAttack baseline method
- [[red-teaming]] - Red teaming concept
- [[reinforcement-learning]] - RL methodology
- [[curriculum-learning]] - Training approach
- [[imitation-learning]] - Cold start technique
- [[diversity-score]] - Evaluation metric
- [[attack-success-rate]] - Evaluation metric
- [[jailbreak-efficiency]] - Evaluation metric
- [[thought-process]] - Thinking mechanism
- [[self-bleu]] - Diversity metric
- [[semantic-similarity]] - Diversity metric
- [[consistency-reward]] - Reward component
- [[diversity-reward]] - Reward component
- [[warmup-reward]] - Reward combination
- [[training-reward]] - Final reward
- [[target-model]] - Target LLM concept
- [[degraded-target-model]] - Progressive training
- [[cold-start]] - Initial training
- [[adaptive-warmup]] - Stage 2 training
- [[diversity-exploration]] - Exploration strategy
- [[test-time-scaling]] - Scaling behavior
- [[targeted-training]] - Model-specific training
- [[pareto-optimality]] - Trade-off analysis
- [[attack-cost]] - Cost metric