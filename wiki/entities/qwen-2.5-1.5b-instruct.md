---
type: entity
title: "Qwen2.5-1.5B"
tags: [classification-model, distillation, alibaba]
related: [qwen-2.5-7b-instruct, jailbreak-r1, consistency-reward]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Qwen2.5-1.5B

## Overview

**Qwen2.5-1.5B** (Qwen2.5-1.5B-Instruct) is used as a classification model (M_classify) in the JAILBREAK-R1 framework. Its capabilities are transferred from a teacher model via data distillation.

## Role in JAILBREAK-R1

The classification model M_classify determines whether an attack prompt is consistent with an attack target:

- **Input**: Attack target (x) and attack prompt (y)
- **Output**: Binary classification (0 or 1)
- **Purpose**: Compute consistency reward (R_consis)

```
R_consis(y) = 1.0 if M_classify(x, y) == 1, else 0.0
```

## Data Distillation

Capabilities are transferred from a larger teacher model to Qwen2.5-1.5B through data distillation, enabling efficient consistency checking during training.

## Related Pages

- [[jailbreak-r1]] - Main method using this model
- [[qwen-2.5-7b-instruct]] - Base model and larger sibling
- [[consistency-reward]] - The reward using this model