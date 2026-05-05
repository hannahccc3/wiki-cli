---
type: entity
title: "Unaligned LLM"
tags: ["component", "RL-JACK component", "reference model"]
related: ["rl-jack", "reward-function"]
sources: ["Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Unaligned LLM

## Overview

The Unaligned LLM is a component of the RL-JACK reward function design. It is a language model that has NOT undergone safety alignment and thus provides actual responses to harmful questions.

## Role in RL-JACK

### Purpose
The Unaligned LLM serves as a reference model to generate ground truth answers to harmful questions.

### Reward Computation
The reward function compares:
1. Target LLM's response to a harmful question
2. Unaligned LLM's response to the same question

Using cosine similarity between their text embeddings, the system determines if the Target LLM has been successfully jailbroken.

### Why This Works
- Unaligned LLM provides answers without refusal
- High similarity indicates Target LLM is answering the question
- Low similarity indicates refusal or unrelated content

## Design Rationale

This approach provides dense, continuous rewards rather than sparse keyword matching. It also specifically measures whether the response is semantically related to the harmful question, not just whether it contains refusal keywords.

## Related Pages

- [[rl-jack]] - The complete system
- [[reward-function]] - The mechanism that uses Unaligned LLM
- [[target-llm]] - The model being evaluated
- [[helper-llm]] - Generates the prompts