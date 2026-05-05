---
type: concept
title: "Power Law Scaling"
tags: ["mathematical modeling", "scaling laws", "attack effectiveness", "in-context learning", "scaling", "mathematical model", "ICL", "jailbreaking", "mathematics", "LLM behavior"]
related: ["many-shot-jailbreaking", "in-context-learning", "alignment-finetuning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Power Law Scaling

## Overview

Power Law Scaling refers to the mathematical relationship where Many-shot Jailbreaking effectiveness follows predictable power laws as the number of demonstrations increases. This enables forecasting what context length is required for attacks to succeed.

## Mathematical Formulation

The expected negative log-probability of a successful attack follows:

```
-E[log P(harmful resp. | n-shot MSJ)] = C × n^(-α) + K
```

Where:
- `n` = number of in-context demonstrations (shots)
- `C` = constant
- `α` (alpha) = power law exponent (measures speed of in-context learning)
- `K` = offset term

## Key Properties

### Intercept (K)
- Measures zero-shot likelihood of successful attack
- Can be increased through alignment training (SL, RL)
- Does NOT affect how quickly attack effectiveness grows with more shots

### Exponent (α)
- Measures speed of in-context learning
- Determines how quickly attack effectiveness grows
- NOT reduced by standard alignment techniques
- Critical for long-term defense

## Implications for Defense

If `K` is increased but `α` remains constant:
- Attack is only temporarily delayed
- Sufficient context length will always enable successful attack
- Effective solutions must either reduce `α` or sufficiently increase `K`

## Connection to ICL

Power laws in MSJ are governed by the same underlying mechanisms as general ICL power laws, suggesting the vulnerability is intrinsic to how LLMs learn from context.

## Related Pages

- [[many-shot-jailbreaking]]
- [[in-context-learning]]