---
type: entity
title: "Llama2-70b"
tags: ["LLM", "target model", "open-source"]
related: ["rl-jack", "safety-alignment", "jailbreaking"]
sources: ["Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Llama2-70b

## Overview

Llama2-70b is a 70-billion parameter large language model developed by Meta (formerly Facebook AI). It is an open-source model that has undergone safety alignment through reinforcement learning from human feedback (RLHF).

## Role in RL-JACK Research

Llama2-70b was used as a primary target model in the RL-JACK paper's experiments. It represents large open-source models that have been safety-aligned.

### Attack Results

RL-JACK demonstrated effective jailbreaking against Llama2-70b, achieving significantly higher success rates compared to baseline attacks including PAIR, AutoDAN, and GCG.

### Transferability

The paper demonstrated that RL-JACK policies trained on other models could transfer to Llama2-70b, marking the first demonstration of cross-model jailbreaking transferability at this scale.

## Model Characteristics

- **Parameters**: 70 billion
- **Developer**: Meta
- **Safety Alignment**: RLHF fine-tuning
- **Access**: Open-weight model

## Related Pages

- [[rl-jack]] - The attack method
- [[safety-alignment]] - The defense mechanism
- [[jailbreaking]] - The attack category
- [[gpt-3.5]] - Another target model tested