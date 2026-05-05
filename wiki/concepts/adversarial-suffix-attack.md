---
type: concept
title: "Adversarial Suffix Attack"
tags: ["adversarial attacks", "white-box attacks", "jailbreaking", "optimization"]
related: ["many-shot-jailbreaking", "gcg", "composition-attacks"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Adversarial Suffix Attack

## Overview

Adversarial suffix attacks are white-box attacks that optimize text suffixes to increase the likelihood of harmful responses. These attacks use gradient-based optimization to find optimal suffix strings.

## Mechanism

1. **Candidate token selection**: Identify potential suffix tokens
2. **Gradient computation**: Calculate gradients with respect to tokens
3. **Coordinate ascent**: Find optimal suffix through iterative optimization
4. **Target**: Maximize probability of compliant (harmful) answers

## Relationship to MSJ

**[[many-shot-jailbreaking]]** can be composed with adversarial suffix attacks:

### GCG Method

**[[gcg]]** (Greedy Coordinate Gradient) is a specific implementation:
- Uses gradient-based coordinate ascent
- Requires white-box access (model weights)
- Highly location-specific within attack strings

### Composition Effects

- Zero-shot: Drastic increase in harmful response probability
- With many shots: Smaller effect due to position changes
- May be optimizable for better MSJ composition

## Related Concepts

- [[gcg]] — Specific implementation method
- [[many-shot-jailbreaking]] — Attack that can incorporate suffixes
- [[composition-attacks]] — Combining attack techniques
- [[adversarial attacks]] — General category