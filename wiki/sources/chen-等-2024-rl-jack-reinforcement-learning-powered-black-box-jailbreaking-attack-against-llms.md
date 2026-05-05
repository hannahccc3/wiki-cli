---
type: source
title: "RL-JACK: Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs"
authors: ["Xuan Chen", "Yuzhou Nie", "Lu Yan", "Yunshu Mao", "Wenbo Guo", "Xiangyu Zhang"]
year: 2024
url: ""
venue: ""
tags: ["jailbreaking", "LLM security", "reinforcement learning", "black-box attack", "safety alignment"]
related: ["rl-jack", "jailbreaking", "safety-alignment", "reinforcement-learning", "black-box-attack", "pair", "autodan", "gcg"]
sources: ["Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md"]
created: 2024-01-15
updated: 2024-01-15
---
# RL-JACK: Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs

## Overview

**RL-JACK** (Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs) is a novel black-box jailbreaking attack against large language models that uses deep reinforcement learning (DRL) to systematically generate prompts that bypass [[safety-alignment]]. The key innovation is formulating jailbreaking as a deterministic search problem where an RL agent learns to select optimal strategies from a constrained action space, combined with a novel cosine similarity reward function comparing responses to unaligned LLM outputs.

## Key Contributions

1. **Novel DRL Framework**: First DRL-driven black-box jailbreaking attack against LLMs
2. **Deterministic Search**: Demonstrates that RL-based deterministic search is more effective and efficient than stochastic genetic methods
3. **LLM-facilitated Action Space**: Constrains search space to 10 strategies while enabling diverse prompt modifications
4. **Novel Reward Function**: Uses cosine similarity comparing target LLM responses to unaligned LLM outputs for dense feedback
5. **Comprehensive Evaluation**: Outperforms five state-of-the-art attacks across six LLMs

## Methodology

### Problem Formulation

RL-JACK treats jailbreaking prompt generation as a search problem in the prompt space. Given a set of harmful questions Q = {q₁, ..., qₙ}, the goal is to find prompts pᵢ that cause the target LLM to provide actual answers rather than refusal responses.

### System Architecture

The RL system consists of three main components:
- **Target LLM**: The model being attacked
- **RL Agent**: A neural network that selects jailbreaking strategies
- **Helper LLM**: Generates prompts based on the agent's selected strategies

### Action Space Design

Ten jailbreaking strategies are designed:
- Seven strategies involve creating conversation contexts
- Three strategies directly modify prompts without specifying contexts

### Reward Function

Uses cosine similarity between:
- Target LLM's response to harmful question
- Reference response from an unaligned LLM

This provides continuous, dense rewards rather than sparse keyword matching.

## Evaluation Results

RL-JACK was evaluated against six LLMs including:
- Llama2-70b (open-source)
- GPT-3.5 (commercial)

Compared against five baselines:
- PAIR (in-context learning-based)
- Cipher (in-context learning-based)
- AutoDAN (genetic method-based)
- GPTFUZZER (genetic method-based)
- GCG (white-box)

Results show RL-JACK achieves significantly higher attack success rates across all metrics.

## Related Attacks and Defenses

### Baseline Attacks
- [[pair]] - Prompt Automatic Iterative Refinement
- [[autodan]] - Automated jailbreaking attack
- [[gcg]] - Greedy Coordinate Gradient

### Related Concepts
- [[jailbreaking]] - The attack technique category
- [[safety-alignment]] - The defense being bypassed
- [[black-box-attack]] - Attack scenario where only model outputs are accessible

---
*Paper from Purdue University and University of California, Santa Barbara*