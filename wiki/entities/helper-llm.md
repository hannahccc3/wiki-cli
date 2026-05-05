---
type: entity
title: "Helper LLM"
tags: ["component", "RL-JACK component"]
related: ["rl-jack", "target-llm", "unaligned-llm"]
sources: ["Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Helper LLM

## Overview

The Helper LLM is a component of the RL-JACK system that generates jailbreaking prompts based on strategies selected by the RL agent. It leverages in-context learning to produce diverse prompt modifications.

## Role in RL-JACK

### Function
The Helper LLM receives instructions from the RL agent (in the form of predefined action templates) and generates jailbreaking prompts following those strategies.

### Action Templates
The system provides 10 predefined action templates:
- 7 context-creating strategies (role-play, scenarios, etc.)
- 3 direct modification strategies (paraphrasing, appending)

### Example Workflow
1. Agent selects action "create role-play scenario"
2. Helper LLM receives instruction + harmful question
3. Helper LLM generates context-wrapped jailbreaking prompt
4. Prompt is sent to Target LLM

## Design Rationale

The Helper LLM design addresses the challenge of excessive action space in token-level approaches. Instead of the agent selecting individual tokens (60,000+ options), it selects from 10 strategies, dramatically reducing search space complexity.

## Related Pages

- [[rl-jack]] - The complete system
- [[target-llm]] - The model being attacked
- [[unaligned-llm]] - Used for reward computation
- [[in-context-learning]] - The technique used by Helper LLM