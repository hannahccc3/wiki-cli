---
type: entity
title: "Claude Instant"
tags: ["LLM", "model", "Anthropic", "safety-aligned"]
related: ["anthropic", "claude-2.0", "many-shot-jailbreaking"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Claude Instant

## Overview

Claude Instant is a large language model developed by Anthropic. It was used in experiments involving targeted reinforcement learning against Many-shot Jailbreaking attacks.

## Entity Details

- **Developer**: Anthropic
- **Organization**: Claude
- **Category**: Large Language Model
- **Safety**: Safety-aligned using RLHF techniques

## Role in Research

Claude Instant was specifically used in RL experiments:

- Pre-RL snapshot used for targeted RL training
- RL training replaced standard harmlessness prompts with MSJ prompts
- Model showed standard vulnerabilities despite safety alignment
- Demonstrated limitations of RL-based mitigation

## Susceptibility to MSJ

Like Claude 2.0, Claude Instant is vulnerable to Many-shot Jailbreaking, with alignment techniques providing only temporary resistance at best.

## Related Entities

- [[anthropic]] - Developer organization
- [[claude-2.0]] - Related model
- [[many-shot-jailbreaking]] - Attack vector