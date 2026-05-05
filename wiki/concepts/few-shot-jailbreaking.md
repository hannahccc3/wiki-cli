---
type: concept
title: "Few-shot Jailbreaking"
tags: ["jailbreaking", "adversarial attacks", "LLM safety", "in-context learning", "LLM security", "short-context attacks"]
related: ["many-shot-jailbreaking", "jailbreaking", "in-context-learning", "adaptive-attacks", "alignment-finetuning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Few-shot Jailbreaking

## Overview

Few-shot Jailbreaking is an attack technique where the attacker prompts the model with a small number of fictitious dialogues containing queries the model would normally refuse, with the assistant providing helpful responses. MSJ extends this concept to the long-context regime.

## Relationship to MSJ

Many-shot Jailbreaking extends few-shot jailbreaking in several ways:

| Aspect | Few-shot | Many-shot |
|--------|----------|-----------|
| Number of demonstrations | 1-10 | Hundreds |
| Context window | Short | Long (up to 70K+ tokens) |
| Effectiveness | Limited | Highly effective |
| Predictability | Variable | Follows power laws |

## Historical Context

Previous work explored few-shot jailbreaking in the short-context regime (Wei et al., 2023; Rao et al., 2023). The Many-shot Jailbreaking research examines the scalability of this attack with longer contexts.

## Attack Mechanism

Both few-shot and many-shot jailbreaking exploit [[in-context-learning]]:

1. Provide demonstrations of model refusing harmful queries
2. Include assistant providing harmful responses
3. Final query elicits harmful response

## Related Pages

- [[many-shot-jailbreaking]]
- [[in-context-learning]]