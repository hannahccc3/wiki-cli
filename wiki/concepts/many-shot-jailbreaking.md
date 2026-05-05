---
type: concept
title: "Many-shot Jailbreaking (MSJ)"
tags: ["adversarial attacks", "jailbreaking", "LLM safety", "in-context learning", "context windows", "LLM security", "safety", "long-context", "long-context models"]
related: ["in-context-learning", "few-shot-jailbreaking", "safety-alignment", "adaptive-attacks", "adversarial-suffix", "composition-attack", "power-laws", "in-context-defense", "cautionary-warning-defense", "greedy-coordinate-gradient", "claude-2.0", "gpt-4", "power-law-scaling", "composition-attacks", "gcg", "alignment-finetuning", "jailbreak-composition", "alignment-pipeline", "adversarial-suffix-attack"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Many-shot Jailbreaking (MSJ)

## Overview

Many-shot Jailbreaking (MSJ) is a long-context attack that exploits the expanded context windows of modern large language models by conditioning models on hundreds of demonstrations of undesirable behavior. This attack extends the concept of few-shot jailbreaking to the long-context regime.

## How It Works

MSJ operates by:

1. **Generating attack strings**: Creating hundreds of compliant query-response pairs using a "helpful-only" model (a model tuned to follow instructions but without harmlessness training)
2. **Randomizing and formatting**: Randomizing the order of demonstrations and formatting them as standard dialogue between user and assistant
3. **Appending target query**: Adding the target query to which the attacker wants a compliant response
4. **Sending as single query**: Submitting the entire dialogue as a single prompt

## Effectiveness

- MSJ successfully jailbreaks multiple state-of-the-art models including [[claude-2.0]], [[gpt-3.5]], [[gpt-4]], [[llama-2-70b]], and [[mistral-7b]]
- Attack effectiveness follows predictable power laws up to hundreds of shots and ~70,000 tokens
- Works even when demonstrations differ in topic from target query if demonstrations are sufficiently diverse

## Model Size Susceptibility

Larger models tend to be more susceptible to MSJ due to faster [[in-context-learning]] speeds. The power law exponent (measuring speed of in-context learning) is larger for larger models.

## Composability

MSJ can be combined with other jailbreaks to reduce context length requirements:

- **Competing objectives attack**: Increases probability of harmful response at all context lengths
- **[[gcg]] (Greedy Coordinate Gradient)**: Effects depend on shot count; GCG suffixes are location-specific and may not retain effectiveness when position is modified

## Prompt Formatting Robustness

Changes to prompt formatting affect the intercept but not the slope of power laws:

- Swapping user/assistant tags
- Translating to different languages
- Using "Question" and "Answer" instead of "Human" and "Assistant"

## Limitations of Standard Mitigations

- [[supervised-fine-tuning]] (SL): Increases power law intercept but does not reduce exponent
- [[reinforcement-learning]] (RL): Increases intercept but doesn't reduce scaling exponent
- Neither prevents attacks at all context lengths

## Related Pages

- [[few-shot-jailbreaking]] - Related but shorter-context attack
- [[in-context-learning]] - Underlying mechanism
- [[power-law-scaling]] - Mathematical relationship
- [[alignment-pipeline]] - Related training process
- [[gcg]] - Related white-box attack
- [[adversarial-suffix-attack]] - Composable attack method