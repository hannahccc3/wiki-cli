---
type: concept
title: "Alignment Finetuning"
tags: ["alignment", "fine-tuning", "RLHF", "safety", "LLM training", "reinforcement learning"]
related: ["supervised-fine-tuning", "reinforcement-learning", "many-shot-jailbreaking", "in-context-learning", "supervised-finetuning", "rlhf", "power-law-scaling"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Alignment Finetuning

## Overview

Alignment finetuning encompasses the training techniques (supervised fine-tuning and reinforcement learning) used to make large language models helpful, harmless, and honest. These techniques are central to modern LLM development but have limitations against **[[many-shot-jailbreaking]]**.

## Components

### Supervised Fine-tuning (SL)

Training on human/AI preference dialogues to encourage helpful, harmless responses.

### Reinforcement Learning (RL / RLHF)

Training using reward models to optimize for human preferences.

## Effect on Power Laws

Research shows that **[[alignment-finetuning]]** affects the **intercept** of power laws but **NOT the exponent**:

| Technique | Effect on Intercept | Effect on Exponent |
|-----------|--------------------|--------------------|
| SL | Increases | No change |
| RL | Increases | No change |

### Implications

- Higher intercept = more shots needed for jailbreak
- But attacks still succeed at sufficiently long contexts
- Cannot simply "scale up" alignment to prevent MSJ

## Limitations Against MSJ

1. **[[power-law-scaling]]** exponent does not decrease
2. **[[composition-attacks]]** can reduce intercept
3. Long enough contexts bypass safety measures entirely

## Research Conclusion

> "Simply scaling up RL or SL training will not defend against MSJ attacks at all context-lengths."

## Related Concepts

- [[many-shot-jailbreaking]] — Attack that bypasses alignment
- [[supervised-finetuning]] — Component of alignment
- [[reinforcement-learning]] — Component of alignment
- [[rlhf]] — Reinforcement Learning from Human Feedback
- [[power-law-scaling]] — Relationship affected by alignment