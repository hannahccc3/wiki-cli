---
type: concept
title: "In-Context Defense (ICD)"
tags: ["defense", "prompt-based", "safety", "jailbreaking mitigation", "prompt-based defense", "in-context learning", "LLM security", "LLM safety"]
related: ["many-shot-jailbreaking", "cautionary-warning-defense", "safety-alignment", "in-context-learning", "alignment-finetuning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# In-Context Defense (ICD)

## Overview

In-Context Defense (ICD) is a prompt-based mitigation that prepends demonstrations of refusals to harmful questions. It is designed to counter **[[many-shot-jailbreaking]]** by showing the model examples of appropriate refusal behavior.

## Mechanism

ICD works by:
1. Prepending incoming prompts with refusal demonstrations
2. Showing model examples of refusing harmful requests
3. Using in-context learning to encourage refusal behavior

## Effectiveness

Research shows ICD has **limited effectiveness** against MSJ:

| Metric | Without ICD | With ICD |
|--------|-------------|----------|
| Attack success rate (deception) | 61% | 54% |
| Reduction | - | ~7% |

### Limitations

1. Only marginally reduces attack success rate
2. Does not fundamentally prevent the attack
3. Attack remains effective at long enough context lengths

## Comparison to Other Defenses

ICD is less effective than **[[cautionary-warning-defense]]**, which achieves 98% reduction in effectiveness. However, neither defense fully prevents MSJ at arbitrary context lengths.

## Related Concepts

- [[many-shot-jailbreaking]] — Attack being defended against
- [[cautionary-warning-defense]] — More effective alternative
- [[alignment-finetuning]] — Does not replace prompt-based defenses