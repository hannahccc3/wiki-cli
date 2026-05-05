---
type: concept
title: "Cautionary Warning Defense (CWD)"
tags: ["defense", "prompt-based", "safety", "jailbreaking mitigation", "prompt-based defense", "LLM security", "LLM safety"]
related: ["many-shot-jailbreaking", "in-context-defense", "safety-alignment", "in-context-learning", "alignment-finetuning"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Cautionary Warning Defense (CWD)

## Overview

Cautionary Warning Defense (CWD) is a prompt-based mitigation strategy that prepends and appends natural language warning texts to caution the assistant model against being jailbroken.

## Mechanism

CWD works by:
1. Adding warning text at the beginning of the prompt
2. Adding reinforcing text at the end of the prompt
3. Aiming to make the model more vigilant against manipulation attempts

## Effectiveness Against MSJ

The research evaluated CWD against Many-shot Jailbreaking:

### Results

- **Attack success rate**: Lowered to approximately 2%
- **Effectiveness**: Significantly more effective than [[in-context-defense]] (ICD)
- **Comparison**: ICD reduced success from 61% to 54%; CWD reduced to 2%

## Limitations

While more effective than ICD, CWD still has limitations:
- May impact model helpfulness on legitimate tasks
- Requires careful testing of safety-capability trade-offs
- May not be foolproof against all attack variations

## Related Pages

- [[many-shot-jailbreaking]]
- [[in-context-defense]]