---
type: concept
title: "Few-shot Jailbreaking"
tags: ["jailbreaking", "adversarial attacks", "LLM safety", "in-context learning", "LLM security"]
related: ["many-shot-jailbreaking", "jailbreaking", "in-context-learning", "adaptive-attacks", "alignment-finetuning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Few-shot Jailbreaking

## Overview

Few-shot jailbreaking is a precursor attack to **[[many-shot-jailbreaking]]** that uses fewer demonstrations (typically 1-10) to induce harmful model responses. It exploits **[[in-context-learning]]** mechanisms to steer models toward undesirable behavior.

## Key Differences from MSJ

| Aspect | Few-shot | Many-shot |
|--------|----------|-----------|
| Number of demonstrations | 1-10 | Hundreds |
| Context length | Short | Long (thousands of tokens) |
| Predictability | Less predictable | Follows power laws |
| Success rate | Variable | Predictable scaling |

## Attack Mechanism

The attacker prompts the model with fictitious dialogue containing:
1. Queries the model would normally refuse (e.g., instructions for harmful activities)
2. Helpful responses to these queries provided in the dialogue
3. The target harmful query at the end

## Research Findings

Previous work explored few-shot jailbreaking in the short-context regime (Wei et al., 2023; Rao et al., 2023). The **[[many-shot-jailbreaking]]** research extends this by:

- Examining scalability with longer contexts
- Characterizing power law relationships
- Studying impact on mitigation strategies

## Relationship to In-Context Learning

Like **[[many-shot-jailbreaking]]**, few-shot attacks exploit the same mechanisms as general **[[in-context-learning]]**. The key insight is that models learn from demonstrations in context without explicit parameter updates.

## Related Concepts

- [[many-shot-jailbreaking]] — Extended version of this attack
- [[in-context-learning]] — Underlying mechanism exploited
- [[power-law-scaling]] — Predictable behavior at scale
- [[alignment-finetuning]] — Does not fully prevent