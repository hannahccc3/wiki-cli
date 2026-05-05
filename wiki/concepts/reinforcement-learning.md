---
type: concept
title: "Reinforcement Learning (RL)"
tags: ["training", "alignment", "RLHF", "safety", "reward", "LLM training", "machine learning", "LLM"]
related: ["safety-alignment", "many-shot-jailbreaking", "supervised-fine-tuning", "alignment-finetuning", "rlhf", "supervised-finetuning", "power-law-scaling", "alignment-pipeline"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Reinforcement Learning (RL)

## Overview

Reinforcement Learning (RL), particularly RLHF (Reinforcement Learning from Human Feedback), is a key alignment technique used to train AI assistants to be helpful, harmless, and honest.

## Effectiveness Against MSJ

The Many-shot Jailbreaking research evaluated RL as a mitigation:

### Effects on Power Laws

- **Intercept**: RL increases the power law intercept
- **Exponent**: RL does NOT reduce the power law exponent
- **Result**: Zero-shot vulnerability decreases, but attacks remain effective with sufficient context

### Key Finding

> While the zero-shot likelihood of undesirable behavior decreases, additional shots continue to increase the probability of eliciting undesirable behavior.

### Targeted RL Experiments

Training with MSJ prompts in the preference data:
- Similar results to targeted SL
- Increased intercept on harmful requests
- Exponent remained unaffected
- Model less susceptible to zero-shot attacks but vulnerable to in-context attacks

### Comparison with SL

Both SL and RL primarily affect the intercept, not the exponent. This suggests the in-context learning mechanism that enables MSJ is robust to standard alignment techniques.

## Implications

Scaling up RL training alone will not prevent MSJ at all context lengths. The vulnerability is intrinsic to in-context learning.

## Related Pages

- [[many-shot-jailbreaking]]
- [[alignment-pipeline]]
- [[supervised-fine-tuning]]