---
type: concept
title: "Alignment Pipeline"
tags: ["alignment", "LLM training", "AI safety"]
related: ["many-shot-jailbreaking", "supervised-fine-tuning", "reinforcement-learning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Alignment Pipeline

## Overview

The Alignment Pipeline refers to the training process used to make AI assistants helpful, harmless, and honest. It typically involves supervised fine-tuning and reinforcement learning.

## Pipeline Stages

### 1. Pre-training
- Base model trained on large corpus
- No behavioral conditioning

### 2. Supervised Fine-tuning (SL)
- Training on demonstration data
- Teaches desired response patterns

### 3. Reinforcement Learning (RL)
- RLHF or similar techniques
- Optimizes for human preferences
- Can include harmlessness training

## MSJ Vulnerability Analysis

The Many-shot Jailbreaking research analyzed how each stage affects MSJ susceptibility:

### Key Findings

- **SL and RL increase intercept but not exponent** of power laws
- Attack remains effective at sufficient context lengths regardless of training stage
- Diversity of demonstrations enables cross-topic attacks
- Prompt formatting changes affect intercept but not slope

### Implications

The alignment pipeline does not fundamentally address the in-context learning vulnerability that enables MSJ. This suggests:

1. MSJ is intrinsic to how LLMs learn from context
2. Protecting against MSJ without harming useful ICL may be challenging
3. New mitigation strategies beyond standard alignment may be needed

## Related Pages

- [[many-shot-jailbreaking]]
- [[supervised-fine-tuning]]
- [[reinforcement-learning]]
- [[in-context-learning]]