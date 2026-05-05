---
type: concept
title: "Adversarial Suffix"
tags: ["adversarial attacks", "optimization", "white-box attacks", "jailbreaking"]
related: ["many-shot-jailbreaking", "jailbreaking", "gcg", "composition-attack"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Adversarial Suffix

## Overview

An adversarial suffix is an optimized text sequence designed to increase the probability that a language model will produce a harmful response to a given query. This technique is a form of white-box attack that uses gradient-based optimization.

## Definition

Adversarial suffixes are text strings appended to prompts that have been algorithmically optimized to manipulate model behavior, typically using gradient information from the model.

## GCG Method

The Greedy Coordinate Gradient (GCG) method is commonly used to find adversarial suffixes:

- Uses gradient information to identify promising token substitutions
- Iteratively optimizes the suffix to maximize likelihood of harmful response
- Requires white-box access to the model

## Interaction with Many-shot Jailbreaking

Research shows that composing MSJ with adversarial suffixes has mixed effects:

1. **Short Context**: GCG suffix dramatically increases probability of harmful responses at zero-shot
2. **Long Context**: Effect is much smaller when combined with many-shot demonstrations
3. **Position Sensitivity**: GCG suffixes are highly position-specific and may not retain effectiveness when applied to each demonstration in MSJ

## Future Directions

Further optimization could potentially create GCG suffixes that compose well with MSJ, reducing required context length for successful attacks.

## Related Concepts

- [[many-shot-jailbreaking]] - Attack that can be combined with suffix
- [[jailbreaking]] - General category
- [[gcg]] - Optimization method for finding suffixes
- [[composition-attack]] - Combining techniques