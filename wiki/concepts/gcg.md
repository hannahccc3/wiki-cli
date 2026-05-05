---
type: concept
title: "Greedy Coordinate Gradient (GCG)"
tags: ["adversarial attacks", "white-box attacks", "adversarial suffix", "optimization", "LLM security"]
related: ["many-shot-jailbreaking", "composition-attacks", "adversarial-suffix-attack"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Greedy Coordinate Gradient (GCG)

## Overview

Greedy Coordinate Gradient (GCG) is a white-box attack method that optimizes adversarial suffixes to increase the likelihood of models giving compliant (potentially harmful) answers.

## Role in MSJ Research

The research investigated composing MSJ with GCG to reduce context length requirements for successful attacks.

## Composition with MSJ

### Findings

The effect of composing MSJ with GCG depends on the number of shots:

- **Zero-shot**: GCG suffix drastically increases probability of harmful responses
- **Longer contexts**: Effect becomes much smaller
- **Location-specific**: GCG suffixes are heavily optimized for specific positions within attack strings

### Analysis

The researchers speculate that GCG doesn't retain effectiveness when its position is modified with the addition of each few-shot demonstration. However, it may be possible to optimize GCG suffixes specifically for MSJ composition.

## Technical Details

GCG uses gradient information to find optimal adversarial suffixes:
- Requires access to model gradients (white-box setting)
- Iteratively optimizes suffix tokens
- Goal: Maximize probability of compliant response

## Related Pages

- [[many-shot-jailbreaking]]
- [[adversarial-suffix-attack]]