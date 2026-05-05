---
type: entity
title: "GPT-4"
tags: ["Sprachmodell", "Closed-Source", "OpenAI", "Frontier-Modell", "Large Language Model", "AI Model", "大型语言模型", "商业模型", "越狱攻击目标", "Μεγάλο Γλωσσικό Μοντέλο", "Πολυτροπικό Μοντέλο", "Προηγμένη Τεχνητή Νοημοσύνη", "LLM", "model", "API", "language model"]
related: ["jailbreakbench", "gpt-3.5", "openai", "llama-3-70b", "jailbreaking", "masterkey", "chatgpt", "llm-chatbot", "rlhf", "renellm", "越狱提示", "安全对齐", "cold-attack", "llama-2", "mistral", "vicuna", "guanaco", "black-box-attacks", "transferability", "many-shot-jailbreaking", "gpt-4-turbo"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md", "Deng 等 - 2024 - MASTERKEY Automated Jailbreaking of Large Language Model Chatbots.md", "Ding 等 - 2023 - A Wolf in Sheep’s Clothing Generalized Nested Jailbreak Prompts can Fool Large Language Models Easi.md", "Gao 等 - 2024 - Inducing High Energy-Latency of Large Vision-Language Models with Verbose Images.md", "Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md", "Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# GPT-4

## Overview

GPT-4 is a large language model developed by **[[openai]]**. It was one of the state-of-the-art models tested in the **[[many-shot-jailbreaking]]** research.

## Research Findings

### Vulnerability to MSJ

GPT-4 (specifically GPT-4-1106-preview) was successfully jailbroken:

- **128-shot prompts** sufficient for harmful behavior adoption
- Negative log-probability follows predictable scaling laws
- All models enter linear regime in log-log plot with enough shots

### Attack Effectiveness

The research demonstrated that:
- MSJ is effective on GPT-4 across various tasks
- Power law relationship holds for attack effectiveness
- Model susceptibility follows predictable patterns

## Related Entities

- [[openai]] — Developer organization
- [[gpt-3.5]] — Predecessor model
- [[gpt-4-turbo]] — Turbo variant

## Related Concepts

- [[many-shot-jailbreaking]] — Attack affecting GPT-4
- [[power-law-scaling]] — Attack effectiveness pattern
- [[in-context-learning]] — Mechanism exploited
- [[alignment-finetuning]] — Training technique tested