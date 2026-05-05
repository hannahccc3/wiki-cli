---
type: concept
title: "In-context Learning (ICL)"
tags: ["machine learning", "LLM capabilities", "few-shot learning", "in-context learning", "large language models", "emergent capabilities", "LLM capability"]
related: ["many-shot-jailbreaking", "power-laws", "safety-alignment", "induction-heads", "alignment-finetuning", "few-shot-jailbreaking", "power-law-scaling"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# In-context Learning (ICL)

## Overview

In-context Learning (ICL) is the ability of large language models to learn from examples provided in the prompt without explicit parameter updates. This capability is central to the Many-shot Jailbreaking attack.

## Role in MSJ

Many-shot Jailbreaking exploits ICL by providing hundreds of demonstrations of undesirable behavior in the context. The model learns from these examples and adopts the demonstrated behavior, even for harmful queries it would normally refuse.

## Power Law Scaling

The Many-shot Jailbreaking research found that ICL effectiveness follows power laws:

- **Power Law Formula**: `-E[log P(harmful resp. | n-shot MSJ)] = C n^(-α) + K`
- Power laws are ubiquitous in ICL across various tasks
- The same mechanisms that govern ICL on general tasks also govern MSJ

## Model Size and ICL Speed

Larger models tend to have faster ICL speeds:

- Larger models learn faster in context
- Faster ICL correlates with higher susceptibility to MSJ
- Larger power law exponents indicate faster learning from demonstrations

## Connection to Safety

The Many-shot Jailbreaking research suggests that circuits responsible for MSJ also underlie general ICL. This implies that protecting against MSJ without compromising benign ICL performance may be challenging.

## Related Pages

- [[many-shot-jailbreaking]] - Attack that exploits ICL
- [[power-law-scaling]] - Mathematical relationship
- [[few-shot-jailbreaking]] - Related attack