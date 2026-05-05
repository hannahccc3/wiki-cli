---
type: entity
title: "RL-JACK"
tags: ["jailbreaking attack", "reinforcement learning", "LLM security", "tool"]
related: ["jailbreaking", "safety-alignment", "reinforcement-learning", "black-box-attack", "pair", "autodan", "gcg", "helper-llm", "target-llm"]
sources: ["Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md"]
created: 2024-01-15
updated: 2024-01-15
---
# RL-JACK

## Overview

**RL-JACK** (Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs) is a novel black-box jailbreaking attack framework that uses deep reinforcement learning to automatically generate prompts that bypass safety alignment in large language models. It was developed by researchers at Purdue University and University of California, Santa Barbara.

## Key Features

- **Deterministic Search**: Uses RL as a deterministic search strategy, more effective than stochastic genetic methods
- **Black-box Setting**: Only requires querying the target LLM and observing responses
- **LLM-facilitated Action Space**: Constrains search to 10 predefined strategies
- **Novel Reward Function**: Cosine similarity between target and unaligned LLM responses

## Components

### RL Agent
A neural network policy that selects optimal jailbreaking strategies at each step.

### Helper LLM
Generates jailbreaking prompts based on the agent's selected strategies.

### Target LLM
The model being attacked; receives generated prompts and produces responses.

## Evaluation Performance

RL-JACK outperforms:
- PAIR (in-context learning-based attack)
- Cipher (encryption-based attack)
- AutoDAN (genetic method-based attack)
- GPTFUZZER (genetic method-based attack)
- GCG (white-box attack)

Tested against:
- Llama2-70b
- GPT-3.5
- ChatGPT
- Bard

## Related Pages

- [[jailbreaking]] - The attack technique category
- [[black-box-attack]] - Attack scenario definition
- [[safety-alignment]] - The defense being bypassed
- [[pair]] - Baseline comparison attack
- [[autodan]] - Baseline comparison attack
- [[gcg]] - Baseline comparison attack