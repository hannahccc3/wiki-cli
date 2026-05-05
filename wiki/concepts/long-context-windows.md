---
type: concept
title: "Long Context Windows"
tags: ["context windows", "LLM architecture", "capabilities", "attack surface"]
related: ["many-shot-jailbreaking", "in-context-learning", "power-laws"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Long Context Windows

## Overview

**Long Context Windows** refer to the expanded input capacity of modern large language models, growing from approximately 4,000 tokens (short essay length) to 10 million tokens (multiple novels or codebases) during 2023. This expansion, enabled by companies like [[anthropic]], [[openai]], and [[google-deepmind]], creates new attack surfaces for adversarial methods like [[many-shot-jailbreaking]].

## Context Window Evolution

| Year | Context Window | Analogous To |
|------|---------------|--------------|
| Early 2023 | ~4,000 tokens | Long essay |
| Late 2023 | 10M tokens | Multiple novels/codebases |

## Attack Surface Expansion

### New Vulnerabilities

Longer context windows enable:
- **[[many-shot-jailbreaking]]**: Hundreds to thousands of demonstrations
- **Full power law exploitation**: Extended scaling behavior
- **Topic-mismatched attacks**: Diverse demonstrations from different domains
- **Universal jailbreaks**: Potential with sufficiently diverse demonstrations

### Context Length Requirements

[[many-shot-jailbreaking]] effectiveness:
- Few-shot (5 shots): Ineffective
- 256 shots: Consistent jailbreaking success
- Up to 70,000 tokens: No observed plateau in harmful response rate

## Model Implementations

### Supporting Models

| Model | Max Context | MSJ Susceptibility |
|-------|-------------|-------------------|
| [[claude-2.0]] | Extended | High |
| [[gpt-4]] | Extended | High |
| [[gpt-3.5]] | Extended | High |
| [[llama-2-70b]] | 4,096 tokens | Limited by context |
| [[mistral-7b]] | Extended | High |

Note: Llama 2's limited context (4,096 tokens) restricts the number of shots available for attacks.

## Capability vs. Safety Trade-off

### Benefits of Long Context

- Better understanding of complex documents
- Improved multi-document reasoning
- Enhanced code completion
- Superior conversation memory

### Safety Concerns

- Expanded attack surface for jailbreaks
- More demonstrations for manipulation
- Difficulty of content moderation at scale
- [[alignment-finetuning]] may not scale with context

## Mitigation Challenges

Long context creates unique challenges:
- [[in-context-defense]] and [[cautionary-warning-defense]] may need scaling
- Content filtering becomes computationally expensive
- Context length constraints impact model utility
- [[power-laws]] suggest attacks will remain effective regardless of length

## Future Implications

As context windows continue to grow:
- [[many-shot-jailbreaking]] may become more effective
- Need for context-aware defense mechanisms
- Architecture-level solutions may be necessary
- [[induction-heads]] research becomes increasingly relevant