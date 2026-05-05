---
type: concept
title: "Reinforcement Learning from Human Feedback (RLHF)"
tags: ["LLM training", "alignment", "reinforcement learning", "human feedback"]
related: ["alignment-finetuning", "reinforcement-learning", "supervised-finetuning", "many-shot-jailbreaking"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Reinforcement Learning from Human Feedback (RLHF)

## Overview

RLHF (Reinforcement Learning from Human Feedback) is a specific variant of **[[reinforcement-learning]]** used in **[[alignment-finetuning]]** where models are trained using human preference data to align with human values.

## Role in LLM Development

RLHF is a core component of modern LLM training:
1. Collect human preference data on model outputs
2. Train reward model on preferences
3. Optimize policy using RL against reward model

## Effect on MSJ

Research shows RLHF affects **[[power-law-scaling]]** parameters:

- **Increases intercept**: Makes zero-shot attacks harder
- **Does not reduce exponent**: In-context learning speed unchanged
- **Not sufficient**: Attacks still succeed at long enough contexts

## Research Context

The **[[many-shot-jailbreaking]]** paper studied models trained with RLHF (Claude 2.0, GPT-3.5, GPT-4) and found that:

1. RL increases context length needed for successful attacks
2. Does not prevent harmful behavior at all context lengths
3. Composition attacks can counter RL benefits

## Related Concepts

- [[alignment-finetuning]] — Parent concept
- [[reinforcement-learning]] — General technique
- [[supervised-finetuning]] — Complementary technique
- [[many-shot-jailbreaking]] — Attack studied on RLHF-trained models
- [[power-law-scaling]] — Relationship affected by RLHF