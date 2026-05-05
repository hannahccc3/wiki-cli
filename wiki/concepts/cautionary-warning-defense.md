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

Cautionary Warning Defense (CWD) is a prompt-based mitigation that uses natural language warnings prepended and appended to prompts to caution the assistant model against being jailbroken.

## Mechanism

CWD works by:
1. Prepending natural language warnings to prompts
2. Appending additional warnings after the prompt
3. Using cautionary language to deter harmful compliance

## Effectiveness

Research shows CWD is **more effective** than **[[in-context-defense]]**:

| Metric | Without Defense | CWD |
|--------|-----------------|-----|
| Attack success rate (deception) | 61% | 2% |
| Reduction | - | ~59% |

### Comparison

| Defense | Effectiveness | Mechanism |
|---------|---------------|-----------|
| ICD | ~7% reduction | Refusal demonstrations |
| CWD | ~59% reduction | Warning messages |

## Limitations

Despite higher effectiveness, CWD:
1. Does not fully prevent MSJ at arbitrary context lengths
2. May impact model usefulness if warnings are too aggressive
3. Requires careful tuning of warning language

## Related Concepts

- [[many-shot-jailbreaking]] — Attack being defended against
- [[in-context-defense]] — Less effective alternative
- [[alignment-finetuning]] — Does not replace prompt-based defenses