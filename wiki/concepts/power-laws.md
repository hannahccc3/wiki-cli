---
type: concept
title: "Power Laws in In-context Learning"
tags: ["mathematical modeling", "scaling", "in-context learning", "jailbreaking", "power laws", "scaling laws", "LLM security"]
related: ["many-shot-jailbreaking", "in-context-learning", "induction-heads"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Power Laws in In-context Learning

## Overview

**Power laws** describe mathematical relationships where effectiveness scales according to a power function. Research on [[many-shot-jailbreaking]] demonstrates that the effectiveness of in-context learning follows predictable power laws up to hundreds of demonstrations.

## Mathematical Formulation

The power law relationship for [[many-shot-jailbreaking]] effectiveness:

```
-NLL(harmful | n shots) = C × n^(-α) + K
```

Where:
- **n**: Number of in-context demonstrations
- **C**: Scaling constant
- **α (exponent)**: Determines speed of in-context learning
- **K**: Asymptotic offset term

## Key Properties

### Log-log Linearity

When K = 0, this relationship appears as a straight line in log-log plots, a hallmark of power law behavior.

### Components

| Component | Meaning | Mitigation Impact |
|-----------|---------|-------------------|
| **C × n^(-α)** | Main scaling term | Higher α = faster attack growth |
| **K** | Asymptotic floor | Higher K = requires more shots |

## Implications for Attack Effectiveness

### Predictability

Power laws enable forecasting:
- Context length required for attack success
- Scaling behavior beyond tested ranges
- Effectiveness across diverse tasks and models

### Model Size Dependence

- Larger models exhibit larger α values
- Faster in-context learning → more susceptible to attacks
- Creates safety concerns as models scale

## Defense Implications

### Why Standard Alignment Fails

[[supervised-fine-tuning]] and [[reinforcement-learning]]:
- Can increase K (intercept)
- Cannot reduce α (exponent)
- Only delays, doesn't prevent attacks

### Effective Solutions Must

1. **Reduce the slope (α)** close to 0
2. **Increase the offset (K)** significantly
3. Address both to prevent attacks at arbitrary context lengths

## Connection to Induction Heads

[[induction-heads]] provide a theoretical foundation:
- Simplified mechanisms that produce power law emergence
- Mathematical tractability for studying ICL scaling
- Suggests fundamental link between architecture and scaling behavior

## Empirical Observations

Power laws hold:
- Across diverse tasks (LogiQA, TruthfulQA, Winogrande, etc.)
- On multiple models (Claude 2.0, GPT-3.5, GPT-4, Llama 2, Mistral)
- With varying prompt formats (affects intercept, not slope)
- Even on unrelated, non-harmful tasks