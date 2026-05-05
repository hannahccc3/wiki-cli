---
type: entity
title: "Target LLM"
tags: ["component", "RL-JACK component", "victim model"]
related: ["rl-jack", "helper-llm", "safety-alignment"]
sources: ["Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Target LLM

## Overview

The Target LLM is the victim model in the RL-JACK attack system. It is a safety-aligned large language model that the attacker attempts to jailbreak by crafting specific prompts.

## Role in RL-JACK

### Attack Process
1. Target LLM receives jailbreaking prompts from the system
2. Target LLM generates responses to these prompts
3. Responses are evaluated for successful jailbreaking

### Expected Behavior (Before Attack)
Safety-aligned models should refuse harmful queries with responses like:
- "I'm sorry, I cannot fulfill this request."
- "I cannot help with that."

### Attack Goal
Force the Target LLM to provide actual answers to harmful questions, bypassing safety alignment.

## Target Models in Evaluation

The RL-JACK paper tested against:
- Llama2-70b
- GPT-3.5
- ChatGPT
- Bard

## Related Pages

- [[rl-jack]] - The attack system
- [[helper-llm]] - Generates the prompts
- [[safety-alignment]] - The defense being bypassed
- [[jailbreaking]] - The attack category
- [[llama2-70b]] - Specific target model
- [[gpt-3.5]] - Specific target model