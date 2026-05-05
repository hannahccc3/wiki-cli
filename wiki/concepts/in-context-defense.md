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

In-Context Defense (ICD) is a prompt-based mitigation strategy that prepends incoming prompts with demonstrations of refusals to harmful questions.

## Mechanism

ICD works by providing the model with examples of appropriate refusal behavior before the potentially adversarial content, encouraging the model to follow similar patterns.

## Effectiveness Against MSJ

The research evaluated ICD against Many-shot Jailbreaking:

### Results

- **Attack success rate (deception category, 205-shot MSJ)**: Reduced from 61% to 54%
- **Impact**: Only slight reduction in attack effectiveness
- **Conclusion**: Limited effectiveness against many-shot jailbreaking

### Limitations

- Does not fundamentally address the in-context learning vulnerability
- May not scale with increasing context lengths
- Demonstrations of refusals may be "overwritten" by hundreds of harmful demonstrations

## Comparison with Other Defenses

ICD was compared with [[cautionary-warning-defense]] (CWD), which showed better effectiveness (reducing attack success to 2% in some cases).

## Related Pages

- [[many-shot-jailbreaking]]
- [[cautionary-warning-defense]]