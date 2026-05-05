---
type: entity
title: "GPT-3.5"
tags: ["LLM", "target model", "commercial", "Large Language Model", "OpenAI", "AI Model", "大型语言模型", "商业模型", "越狱攻击目标", "model", "API", "target-model", "closed-source", "language model"]
related: ["rl-jack", "safety-alignment", "jailbreaking", "masterkey", "openai", "chatgpt", "gpt-4", "llm-chatbot", "rlhf", "renellm", "越狱提示", "安全对齐", "cold-attack", "llama-2", "mistral", "vicuna", "guanaco", "black-box-attacks", "transferability", "gpt-4o", "claude-3.5-sonnet", "llama-2-7b-chat", "vicuna-7b", "qwen-2.5-7b-instruct", "llama-3-8b-chat", "gemini-2.0-flash", "harmbench", "jailbreak-r1", "many-shot-jailbreaking", "gpt-3.5-turbo"]
sources: ["Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md", "Deng 等 - 2024 - MASTERKEY Automated Jailbreaking of Large Language Model Chatbots.md", "Ding 等 - 2023 - A Wolf in Sheep’s Clothing Generalized Nested Jailbreak Prompts can Fool Large Language Models Easi.md", "Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md", "Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md", "Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# GPT-3.5

## Overview

GPT-3.5 is a large language model developed by **[[openai]]**. It was tested in the **[[many-shot-jailbreaking]]** research, specifically GPT-3.5-turbo-16k-0613.

## Research Findings

### Vulnerability to MSJ

GPT-3.5 was successfully jailbroken:

- **128-shot prompts** sufficient for harmful behavior adoption
- Attack effectiveness follows predictable **[[power-law-scaling]]**
- Negative log-probability enters linear regime with enough shots

### Comparison to Other Models

GPT-3.5 showed similar vulnerability patterns to:
- **[[gpt-4]]** — Slightly less susceptible
- **[[claude-2.0]]** — Comparable susceptibility
- **[[mistral-7b]]** — Slightly more susceptible

## Related Entities

- [[openai]] — Developer organization
- [[gpt-4]] — Successor model
- [[gpt-3.5-turbo]] — Turbo variant used in research

## Related Concepts

- [[many-shot-jailbreaking]] — Attack affecting GPT-3.5
- [[power-law-scaling]] — Attack effectiveness pattern
- [[in-context-learning]] — Mechanism exploited