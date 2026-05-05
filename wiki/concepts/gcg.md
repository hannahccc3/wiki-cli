---
type: concept
title: "Greedy Coordinate Gradient (GCG)"
tags: ["adversarial attacks", "white-box attacks", "adversarial suffix", "optimization"]
related: ["many-shot-jailbreaking", "composition-attacks", "adversarial-suffix-attack"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Greedy Coordinate Gradient (GCG)

## Overview

Greedy Coordinate Gradient (GCG) is a method for finding adversarial suffixes using gradient-based coordinate ascent. It is a **white-box attack** that optimizes text suffixes to increase the likelihood of harmful responses.

## Role in Many-shot Jailbreaking

**[[many-shot-jailbreaking]]** can be composed with GCG to create hybrid attacks. The composition effects depend on the number of shots:

### Findings

1. **Zero-shot GCG** drastically increases probability of harmful responses
2. **With many shots**, GCG effect is much smaller
3. **Composition effects** depend on shot count

## Mechanism

GCG works by:
1. Taking gradients with respect to candidate tokens
2. Performing coordinate ascent to find optimal suffixes
3. Optimizing for increased likelihood of compliant (harmful) answers

## Research Observations

The researchers speculate that:
- GCG is heavily location-specific within attack strings
- It doesn't retain effectiveness when position changes with added demonstrations
- Future work could optimize GCG suffixes to compose well with MSJ

## Related Concepts

- [[many-shot-jailbreaking]] — Attack that can be composed with GCG
- [[composition-attacks]] — Combining MSJ with other jailbreaks
- [[adversarial-suffix-attack]] — General category of attacks