---
type: concept
title: "Induction Heads"
tags: ["mechanistic interpretability", "transformer architecture", "in-context learning", "theory", "mechanism", "attention", "circuit"]
related: ["in-context-learning", "power-laws", "many-shot-jailbreaking", "power-law-scaling"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Induction Heads

## Overview

Induction heads are two-layer attention mechanisms in transformer models that are proposed as a key circuit underlying in-context learning. They enable models to recognize and complete patterns from demonstrations.

## Mechanism

### How They Work

1. **Pattern Detection**: First attention layer identifies copy-like patterns
2. **Completion Prediction**: Second layer predicts completions based on detected patterns
3. **In-context Application**: Enables learning from examples without weight updates

### Power Law Generation

Research suggests induction heads generate power law-like behavior:
- Predicted learning rates match empirical observations
- Explains ubiquity of power laws across tasks

## Connection to Many-shot Jailbreaking

### Shared Mechanism

The researchers hypothesize that:
1. MSJ exploits the same induction head circuits as ICL
2. This explains why power laws govern both benign and harmful ICL
3. Defending against MSJ without harming ICL is difficult

### Evidence

- Power laws appear in both safety-related and unrelated tasks
- Scaling behavior is consistent across diverse contexts
- Mathematical models of induction heads reproduce empirical patterns

## Implications for Defense

- **Circuit-level challenge**: Attack and defense share the same underlying mechanism
- **Noisy optimization**: Making induction heads refuse harmful patterns may break beneficial ones
- **Structural solutions**: May require architectural changes, not just training modifications

## Related Pages

- [[in-context-learning]]
- [[power-law-scaling]]
- [[many-shot-jailbreaking]]