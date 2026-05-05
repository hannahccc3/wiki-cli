---
type: entity
title: "JAILBREAK-R1"
tags: [proposed-method, red-teaming, reinforcement-learning, adversarial]
related: [jailbreak-r1-zero, harmbench, tap, pair, gpo, auto Dan-turbo, arrattack, red-teaming, reinforcement-learning, curriculum-learning]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2025-01-15
updated: 2025-01-15
---
# JAILBREAK-R1

## Overview

**JAILBREAK-R1** is a novel automated red teaming training framework proposed by Guo et al. (2025) that utilizes reinforcement learning to automatically explore and generate diverse attack prompts while balancing effectiveness. It is designed to help red-team models think effectively and generate more adversarial attacks.

## Architecture

JAILBREAK-R1 employs a three-stage training pipeline:

1. **Cold Start**: Imitation learning using existing jailbreak strategies to generate thought processes and attack prompts
2. **Adaptive Warm-up**: Training with consistency and diversity rewards for diverse strategy exploration
3. **Curriculum-based Learning**: Progressive introduction of degraded target models for enhanced jailbreaking

## Key Features

- **Thought Process Integration**: Leverages thinking mechanisms to enrich planning and strategy execution
- **Reward Modeling**: Combines consistency rewards, diversity rewards, and training rewards
- **Curriculum Learning**: Uses 3 intermediate degraded models (n=3) for stable reward signals
- **Base Model**: Qwen2.5-7B-Instruct

## Performance

JAILBREAK-R1 achieved the highest attack success rate (65.19%) and highest diversity scores (0.970) among all compared methods on Harmbench:

| Metric | JAILBREAK-R1 | AutoDAN-Turbo | GPO | TAP |
|--------|-------------|---------------|-----|-----|
| ASR | 65.19% | 52.31% | 43.55% | 45.63% |
| DIV | 0.970 | 0.921 | 0.878 | 0.779 |

## Comparison with JAILBREAK-R1-Zero

JAILBREAK-R1 includes a cold start stage that enriches jailbreak knowledge, while [[jailbreak-r1-zero]] omits this stage. JAILBREAK-R1 shows:
- 10.1% higher attack success rate
- 10.7% higher diversity score

## Related Pages

- [[jailbreak-r1-zero]] - Variant without cold start
- [[harmbench]] - Evaluation benchmark
- [[qwen-2.5-7b-instruct]] - Base model
- [[tap]] - Baseline comparison
- [[pair]] - Baseline comparison
- [[gpo]] - Baseline comparison
- [[auto Dan-turbo]] - Baseline comparison
- [[red-teaming]] - Related concept
- [[reinforcement-learning]] - Methodology
- [[curriculum-learning]] - Training approach