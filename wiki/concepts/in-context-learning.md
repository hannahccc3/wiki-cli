---
type: concept
title: "In-Context Learning (ICL)"
tags: ["machine learning", "LLM capabilities", "few-shot learning", "in-context learning", "large language models", "emergent capabilities"]
related: ["many-shot-jailbreaking", "power-laws", "safety-alignment", "induction-heads", "alignment-finetuning", "few-shot-jailbreaking", "power-law-scaling"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# In-Context Learning (ICL)

## Overview

In-context learning (ICL) is a mechanism where large language models learn from examples provided in the context window without explicit parameter updates. The model observes demonstration pairs and adapts its behavior accordingly.

## Role in Many-shot Jailbreaking

Research demonstrates that **[[many-shot-jailbreaking]]** exploits the **same mechanisms** as general in-context learning. This finding has important implications:

1. The power laws underlying MSJ are not specific to jailbreaking
2. Performance on benign ICL tasks also follows predictable power laws
3. Protecting against MSJ without harming benign ICL may be challenging

## Key Properties

### Power Law Behavior

ICL effectiveness follows power laws as the number of demonstrations increases:

```
Performance ~ C × n^(-α) + K
```

Where:
- n = number of demonstrations
- α = exponent (learning speed)
- C, K = constants

### Model Size Dependence

Larger models tend to:
- Have faster in-context learning speeds
- Exhibit larger power law exponents
- Be more susceptible to ICL-based attacks like MSJ

## Implications for Safety

The connection between MSJ and general ICL suggests that any defense targeting MSJ specifically may also impact legitimate uses of in-context learning. This creates a challenging tradeoff between safety and capability.

## Related Concepts

- [[many-shot-jailbreaking]] — Attack exploiting ICL
- [[few-shot-jailbreaking]] — Smaller-scale variant
- [[power-law-scaling]] — Mathematical relationship observed
- [[alignment-finetuning]] — Does not reduce ICL speed