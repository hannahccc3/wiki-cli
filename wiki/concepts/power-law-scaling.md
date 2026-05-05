---
type: concept
title: "Power Law Scaling"
tags: ["mathematical modeling", "scaling laws", "attack effectiveness", "in-context learning"]
related: ["many-shot-jailbreaking", "in-context-learning", "alignment-finetuning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Power Law Scaling

## Overview

Power law scaling refers to a mathematical relationship where attack effectiveness follows a predictable power law pattern with increasing numbers of demonstrations. The expected negative log-probability of an attack being successful follows:

```
-ℰ[log P(harmful response | n-shot MSJ)] = Cn^(-α) + K
```

## Components

### Exponent (α)
- Measures the speed of **[[in-context-learning]]**
- Larger exponent = faster learning = more effective attack
- Does NOT decrease with standard **[[alignment-finetuning]]**

### Intercept (K or zero-shot term)
- Represents zero-shot likelihood of harmful behavior
- Can be increased through RL and SL training
- Higher intercept = more shots needed for attack to succeed

### Constant term (C)
- Scales the overall effectiveness
- Affected by prompt formatting changes

## Implications

### Why Exponent Matters

A unit increase in intercept corresponds to an **exponential increase** in shots needed to jailbreak. However:
- If exponent stays constant, attacks will eventually succeed
- Composition attacks can decrease intercept, negating RL/SL benefits

### Model Size Effects

Larger models tend to have:
- Larger exponents (faster learning)
- Greater susceptibility to attacks at all context lengths

## Defense Implications

Effective defenses must either:
1. Reduce the power law exponent (making in-context learning slower)
2. Increase the offset term K sufficiently
3. Constrain context length (impacting model usefulness)

Standard **[[alignment-finetuning]]** only addresses the intercept, not the fundamental vulnerability.

## Related Concepts

- [[many-shot-jailbreaking]] — Attack following power laws
- [[in-context-learning]] — Mechanism exhibiting power laws
- [[alignment-finetuning]] — Affects intercept but not exponent