---
type: concept
title: "Greedy Coordinate Gradient (GCG)"
tags: ["adversarial attacks", "white-box attacks", "optimization", "LLM security"]
related: ["many-shot-jailbreaking", "adversarial-suffix-attack", "alignment-finetuning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Greedy Coordinate Gradient (GCG)

## Overview

**Greedy Coordinate Gradient (GCG)** is a white-box adversarial attack method that constructs optimized text suffixes to increase the likelihood of language models providing compliant (harmful) responses to harmful requests. It is used in [[many-shot-jailbreaking]] composition experiments.

## How GCG Works

### White-box Attack

Unlike black-box attacks, GCG requires:
- Access to model gradients
- Full knowledge of model architecture
- Ability to compute gradient information

### Optimization Process

1. **Candidate generation**: Creates many candidate suffixes
2. **Gradient evaluation**: Uses coordinate gradient ascent to score candidates
3. **Greedy selection**: Chooses highest-scoring modifications
4. **Iteration**: Repeats until optimal suffix found

The adversarial suffix is optimized to increase the probability of the model giving a compliant answer to harmful requests.

## Integration with Many-shot Jailbreaking

### Composition Results

The paper investigates composing [[many-shot-jailbreaking]] with GCG:

| Shots | Baseline NLL | GCG Suffix | Random Suffix |
|-------|-------------|------------|---------------|
| 0 | 30.0 | 12.0 | 35.0 |
| 30 | 6.0 | 4.0 | 10.0 |
| 60 | 2.0 | 1.0 | 2.0 |

### Mixed Effectiveness

- **Zero-shot**: GCG drastically increases harmful response probability
- **Longer contexts**: Effect diminishes significantly
- **Reason**: GCG is heavily location-specific within attack strings

### Challenges

When composed with MSJ:
- Position changes with added demonstrations
- Effectiveness doesn't transfer across positions
- May need position-aware suffix optimization

## Relationship to Other Attacks

### Compared to Black-box Attacks

| Aspect | GCG (White-box) | Competing Objectives (Black-box) |
|--------|-----------------|----------------------------------|
| Gradient access | Required | Not needed |
| Composition with MSJ | Mixed | Effective |
| Location dependence | High | Low |

### Combined Approach

Future work may optimize GCG suffixes specifically for MSJ composition scenarios.

## Implications

- [[many-shot-jailbreaking]] composition can be attack-specific
- White-box and black-box attacks may require different composition strategies
- [[adversarial-suffix-attack]] mechanisms remain important for understanding vulnerabilities