---
type: concept
title: "Adversarial Suffix Attack"
tags: ["adversarial attacks", "white-box attacks", "jailbreaking", "optimization", "LLM security"]
related: ["many-shot-jailbreaking", "gcg", "composition-attacks"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Adversarial Suffix Attack

## Overview

Adversarial Suffix Attacks are white-box attacks that construct suffixes optimized to increase the likelihood of models giving compliant answers to harmful requests.

## Relationship to MSJ

The Many-shot Jailbreaking research investigated composing MSJ with adversarial suffix attacks (specifically [[gcg]]) to enhance attack effectiveness.

## How It Works

1. **Identify target**: A harmful query requiring refusal
2. **Optimize suffix**: Use gradient-based methods to find tokens that maximize compliance
3. **Append to prompt**: Add the optimized suffix to the harmful query
4. **Execute attack**: Model is more likely to provide harmful response

## Composition Benefits

Combining adversarial suffixes with MSJ:
- Can reduce context length requirements
- Effects vary with number of shots
- GCG suffixes are location-specific and may not generalize across MSJ positions

## Related Defenses

- [[in-context-defense]] (ICD)
- [[cautionary-warning-defense]] (CWD)

## Related Pages

- [[many-shot-jailbreaking]]
- [[gcg]]