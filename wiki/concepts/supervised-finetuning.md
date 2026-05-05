---
type: concept
title: "Supervised Fine-tuning (SL)"
tags: ["LLM training", "alignment", "fine-tuning", "machine learning"]
related: ["alignment-finetuning", "reinforcement-learning", "many-shot-jailbreaking", "power-law-scaling"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Supervised Fine-tuning (SL)

## Overview

Supervised Fine-tuning (SL) is a training technique used in **[[alignment-finetuning]]** where models are trained on human/AI preference dialogues to encourage helpful, harmless, and honest responses.

## Effect on Power Laws

Research shows SL affects the **intercept** of **[[power-law-scaling]]** but NOT the exponent:

- **Intercept increases**: Zero-shot probability of harmful behavior decreases
- **Exponent unchanged**: Speed of in-context learning remains the same
- **Result**: More shots needed, but attacks still succeed at long enough contexts

## Targeted SL Against MSJ

Researchers explored SL training specifically on MSJ prompts:

### Method
1. Create dataset of benign responses to MSJ attacks
2. Train model to produce refusal responses
3. Evaluate on MSJ prompts up to 30 shots

### Findings
- Zero-shot harmful response probability decreases
- Power law exponent remains largely unaffected
- Supervised finetuning does not prevent in-context learning of harmful behaviors

## Research Conclusion

> "Supervised finetuning in this way does not prevent the model from learning harmful behaviors from in-context patterns."

## Related Concepts

- [[alignment-finetuning]] — Parent concept
- [[reinforcement-learning]] — Complementary training technique
- [[many-shot-jailbreaking]] — Attack being defended against
- [[power-law-scaling]] — Relationship affected by SL