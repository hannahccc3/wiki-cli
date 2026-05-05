---
type: concept
title: "Reinforcement Learning (RL)"
tags: ["training", "alignment", "RLHF", "safety", "reward", "LLM training", "machine learning"]
related: ["safety-alignment", "many-shot-jailbreaking", "supervised-fine-tuning", "alignment-finetuning", "rlhf", "supervised-finetuning", "power-law-scaling"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Reinforcement Learning (RL)

## Overview

Reinforcement Learning (RL) is a training technique used in **[[alignment-finetuning]]** where models are trained using reward models to optimize for human preferences, often through **[[rlhf]]** (Reinforcement Learning from Human Feedback).

## Effect on Power Laws

Like **[[supervised-finetuning]]**, RL affects the **intercept** of **[[power-law-scaling]]** but NOT the exponent:

- **Intercept increases**: Model less susceptible to zero-shot attacks
- **Exponent unchanged**: In-context learning speed unaffected
- **Result**: Temporary delay, not prevention of attacks

## Targeted RL Against MSJ

Researchers explored RL training specifically on MSJ prompts:

### Method
1. Replace standard harmlessness prompts with MSJ prompts (up to 10 shots)
2. Penalize harmful responses using preference model
3. Train model to produce benign responses to MSJ

### Findings
- Intercept on harmful requests increases
- Exponent remains unaffected
- Zero-shot susceptibility decreases

## Unique RL Observations

Unlike SL:
- Intercept on responses to benign requests also increases during RL
- Model may go off-distribution with respect to evaluation data
- Temperature shifts occur during training

## Research Conclusion

> "None of the finetuning-based interventions we've studied (SL or RL) provided long-term relief from MSJ, as these methods are unable to substantially eliminate the in-context scaling of MSJ."

## Related Concepts

- [[alignment-finetuning]] — Parent concept
- [[supervised-finetuning]] — Complementary technique
- [[rlhf]] — Specific RL variant used
- [[many-shot-jailbreaking]] — Attack being defended against
- [[power-law-scaling]] — Relationship affected by RL