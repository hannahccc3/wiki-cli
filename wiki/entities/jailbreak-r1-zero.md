---
type: entity
title: "JAILBREAK-R1-Zero"
tags: [proposed-method, red-teaming, reinforcement-learning, adversarial]
related: [jailbreak-r1, harmbench, tap, pair, gpo, auto Dan-turbo, red-teaming, reinforcement-learning]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md"]
created: 2025-01-15
updated: 2025-01-15
---
# JAILBREAK-R1-Zero

## Overview

**JAILBREAK-R1-Zero** is a variant of JAILBREAK-R1 that explores the jailbreak capabilities of LLMs without prior jailbreak knowledge. It omits the cold start stage and relies solely on the model's inherent jailbreak space.

## Key Difference from JAILBREAK-R1

| Aspect | JAILBREAK-R1 | JAILBREAK-R1-Zero |
|--------|-------------|-------------------|
| Cold Start | ✓ Included | ✗ Omitted |
| Base Model | Qwen2.5-7B-Instruct | Qwen2.5-7B-Instruct |
| ASR | 65.19% | 55.87% |
| Diversity | 0.970 | 0.871 |

## Purpose

JAILBREAK-R1-Zero is designed to explore:
- The inherent jailbreak ability of the base model itself
- Whether reinforcement learning can discover jailbreak strategies without prior knowledge
- The upper bound of "zero-shot" jailbreak capabilities

## Findings

The paper finds that without prior jailbreak knowledge:
- Reinforcement learning tends to converge on local optima
- Attack success rate is reduced by 10.1%
- Diversity is reduced by 10.7%

This demonstrates that cold start enriches jailbreak knowledge and generates more adversarial attacks.

## Performance

On Harmbench, JAILBREAK-R1-Zero achieved:
- Average ASR: 55.87%
- Average Diversity: 0.871
- Jailbreak Efficiency: 1.72 attempts (best among all methods)

## Related Pages

- [[jailbreak-r1]] - Main proposed method
- [[harmbench]] - Evaluation benchmark
- [[qwen-2.5-7b-instruct]] - Base model
- [[cold-start]] - Omitted training stage
- [[red-teaming]] - Related concept
- [[reinforcement-learning]] - Methodology