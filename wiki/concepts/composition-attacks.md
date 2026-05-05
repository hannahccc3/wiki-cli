---
type: concept
title: "Composition Attacks"
tags: ["adversarial attacks", "jailbreaking", "combined attacks", "multi-technique"]
related: ["many-shot-jailbreaking", "gcg", "few-shot-jailbreaking"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Composition Attacks

## Overview

Composition attacks refer to combining multiple jailbreak techniques to reduce required context length or increase attack effectiveness. **[[many-shot-jailbreaking]]** can be fruitfully combined with other jailbreak methods.

## Types of Composition

### 1. MSJ + Competing Objectives Attack

- Combines MSJ with blackbox semantic jailbreak
- Increases probability of harmful response at **all** context lengths
- Hybrid attack outperforms standard MSJ with same demonstrations

### 2. MSJ + GCG Adversarial Suffix

- Combines **[[gcg]]** adversarial suffix with MSJ
- Effects depend on number of shots:
  - Zero-shot: Large effect
  - Many-shot: Smaller effect
- GCG is location-specific and loses effectiveness when position changes

## Why Composition Matters

### Intercept Reduction

Composition attacks can decrease the power law intercept:
- Reduces shots needed for successful jailbreak
- Counteracts benefits of RL/SL training
- Makes attacks more practical

### Practical Implications

> "Our results suggest that MSJ can be combined with other jailbreaks to yield successful attacks at even shorter context lengths."

## Related Concepts

- [[many-shot-jailbreaking]] — Base attack being composed
- [[gcg]] — White-box method that can be composed
- [[power-law-scaling]] — Affected by composition
- [[alignment-finetuning]] — Mitigations countered by composition