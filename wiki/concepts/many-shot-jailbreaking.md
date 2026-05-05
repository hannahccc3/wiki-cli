---
type: concept
title: "Many-shot Jailbreaking (MSJ)"
tags: ["adversarial attacks", "jailbreaking", "LLM safety", "in-context learning", "context windows", "LLM security", "safety", "long-context"]
related: ["in-context-learning", "few-shot-jailbreaking", "safety-alignment", "adaptive-attacks", "adversarial-suffix", "composition-attack", "power-laws", "in-context-defense", "cautionary-warning-defense", "greedy-coordinate-gradient", "claude-2.0", "gpt-4", "power-law-scaling", "composition-attacks", "gcg", "alignment-finetuning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Many-shot Jailbreaking (MSJ)

## Overview

Many-shot Jailbreaking (MSJ) is a simple long-context attack technique that uses hundreds of demonstrations of undesirable behavior to steer large language models (LLMs) toward harmful responses. It extends the concept of **[[few-shot-jailbreaking]]** into the newly feasible regime of very long context windows (up to millions of tokens).

## How It Works

MSJ operates by conditioning an LLM on a large number of harmful question-answer pairs:

1. The attacker generates compliant query-response pairs using a "helpful-only" model
2. These pairs are formatted to resemble standard dialogue between user and assistant
3. The pairs are randomized and formatted as fictional dialogue
4. The target query is appended to the end
5. The entire dialogue is sent as a single query

## Key Characteristics

### Robustness

MSJ is robust to:
- Format changes (swapping user/assistant tags)
- Style changes (translating to different languages)
- Subject changes (diverse demonstrations work even when target topic differs)

### Power Law Scaling

Attack effectiveness follows predictable **[[power-law-scaling]]** patterns:
```
-ℰ[log P(harmful response | n-shot MSJ)] = Cn^(-α) + K
```

This enables forecasting of attack success at various context lengths.

### Model Susceptibility

Larger models tend to be more susceptible because:
- They learn faster in context
- They have larger power law exponents
- Alignment training increases intercept but not exponent

## Related Concepts

- [[in-context-learning]] — MSJ exploits the same mechanisms as general ICL
- [[few-shot-jailbreaking]] — Precursor attack using fewer demonstrations
- [[composition-attacks]] — Combining MSJ with other jailbreaks
- [[gcg]] — Greedy Coordinate Gradient for adversarial suffixes
- [[alignment-finetuning]] — Standard defenses that MSJ bypasses

## Related Defenses

- [[in-context-defense]] — Prepends refusal demonstrations
- [[cautionary-warning-defense]] — Uses natural language warnings