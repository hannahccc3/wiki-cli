---
type: concept
title: "Supervised Fine-tuning (SL)"
tags: ["training", "alignment", "machine learning", "safety", "LLM"]
related: ["safety-alignment", "many-shot-jailbreaking", "reinforcement-learning", "alignment-pipeline"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Supervised Fine-tuning (SL)

## Overview

Supervised Fine-tuning (SL) is a training technique used in LLM alignment pipelines where models are trained on human or AI-generated demonstration data.

## Effectiveness Against MSJ

The Many-shot Jailbreaking research evaluated SL as a mitigation:

### Effects on Power Laws

- **Intercept**: SL increases the power law intercept
- **Exponent**: SL does NOT reduce the power law exponent
- **Result**: Zero-shot probability decreases, but attacks remain effective at longer context lengths

### Key Finding

> Supervised finetuning to mitigate MSJ attacks is ineffective against protecting against MSJ with arbitrarily large context lengths. SL does not prevent the model from learning harmful behaviors from in-context patterns.

### Targeted SL Experiments

Training on datasets containing MSJ prompts with benign responses:
- Increased intercept (reduced zero-shot harm)
- Exponent remained largely unaffected
- Did not prevent in-context scaling of harmful behaviors

## Implications

Simply scaling up SL training will not defend against MSJ attacks at all context lengths. The fundamental vulnerability persists.

## Related Pages

- [[many-shot-jailbreaking]]
- [[alignment-pipeline]]
- [[reinforcement-learning]]