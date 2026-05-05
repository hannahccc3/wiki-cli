---
type: concept
title: "Alignment Fine-tuning"
tags: ["alignment", "fine-tuning", "RLHF", "safety", "LLM training", "reinforcement learning", "supervised learning"]
related: ["supervised-fine-tuning", "reinforcement-learning", "many-shot-jailbreaking", "in-context-learning", "supervised-finetuning", "rlhf", "power-law-scaling"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Alignment Fine-tuning

## Overview

Alignment fine-tuning refers to the training methods used to make large language models helpful, harmless, and honest. These include supervised learning (SL) and reinforcement learning (RLHF), which are critical for deploying safe AI systems.

## Types of Alignment Training

### Supervised Learning (SL)

Trains models on human-written demonstration responses:
- Uses curated datasets of helpful, harmless responses
- Can include targeted data against specific attacks
- Affects the **intercept** of power laws

### Reinforcement Learning from Human Feedback (RLHF)

Uses reward models to guide policy:
- Human annotators rank model responses
- Policy optimizes for human preferences
- Includes harmlessness training
- Affects the **intercept** of power laws

## Impact on Many-shot Jailbreaking

### Key Finding

**Alignment techniques only affect the intercept, not the exponent of power laws describing MSJ effectiveness.**

| Training Type | Intercept Effect | Exponent Effect | Protection Duration |
|--------------|------------------|-----------------|---------------------|
| Standard SL | Improves | None | Temporary |
| Standard RL | Improves | None | Temporary |
| Targeted SL | Improves | None | Temporary |
| Targeted RL | Improves | None | Temporary |

### Interpretation

- **Intercept increase** = Higher zero-shot resistance
- **Exponent unchanged** = Same rate of attack improvement with more shots
- **Result** = Attacks still succeed at sufficiently long context lengths

## Scaling Does Not Help

Increasing compute/data for alignment:
- Raises the intercept (delays attacks)
- Does NOT reduce the exponent
- Cannot prevent attacks at arbitrary context lengths

## Why It Fails Against MSJ

1. **In-context nature**: MSJ exploits ICL, not model weights
2. **Pattern recognition**: Model learns from demonstrations, not training
3. **Fundamental mechanism**: Alignment doesn't change how ICL works

## Implications

- New alignment methods must address the **exponent**, not just intercept
- Context length limits could help but reduce utility
- May require architectural changes to defend effectively

## Related Pages

- [[many-shot-jailbreaking]]
- [[power-law-scaling]]
- [[in-context-learning]]
- [[rlhf]]