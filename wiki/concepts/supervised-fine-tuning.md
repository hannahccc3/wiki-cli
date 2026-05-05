---
type: concept
title: "Supervised Fine-tuning"
tags: ["training", "alignment", "machine learning", "safety"]
related: ["safety-alignment", "many-shot-jailbreaking", "reinforcement-learning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Supervised Fine-tuning

## Overview

Supervised Fine-tuning (SFT) is a training technique used in LLM alignment where models are trained on curated demonstration data showing appropriate responses to various queries, including those that might be harmful.

## Definition

SFT involves updating model parameters using gradient descent on a dataset of input-output pairs that demonstrate desired behavior.

## Role in Safety Alignment

SFT is a key component of making models safer:
- Models learn from examples of refusing harmful requests
- Can be targeted with specific datasets (e.g., responses to jailbreak attempts)
- Forms the foundation before reinforcement learning

## Effectiveness Against MSJ

Research reveals critical limitations:

1. **Increases Intercept**: Reduces zero-shot susceptibility
2. **Does Not Reduce Exponent**: In-context learning slope remains largely unchanged
3. **Insufficient at Scale**: Attacks succeed with sufficient context length regardless

### Key Finding

> "Supervised fine-tuning to mitigate MSJ attacks is ineffective against protecting against MSJ with arbitrarily large context lengths."

## Targeted SFT Against MSJ

Attempts to specifically train against MSJ (using up to 10-shot examples in training):
- Reduces zero-shot probability of harmful responses
- Power law exponent remains largely unaffected
- Does not prevent model from learning harmful behaviors from in-context patterns

## Related Concepts

- [[safety-alignment]] - Broader context
- [[many-shot-jailbreaking]] - Attack being defended
- [[reinforcement-learning]] - Complementary alignment technique