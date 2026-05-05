---
type: entity
title: "GPT-4"
tags: ["Sprachmodell", "Closed-Source", "OpenAI", "Frontier-Modell", "Large Language Model", "AI Model", "大型语言模型", "商业模型", "越狱攻击目标", "Μεγάλο Γλωσσικό Μοντέλο", "Πολυτροπικό Μοντέλο", "Προηγμένη Τεχνητή Νοημοσύνη", "LLM", "model", "API", "language model"]
related: ["jailbreakbench", "gpt-3.5", "openai", "llama-3-70b", "jailbreaking", "masterkey", "chatgpt", "llm-chatbot", "rlhf", "renellm", "越狱提示", "安全对齐", "cold-attack", "llama-2", "mistral", "vicuna", "guanaco", "black-box-attacks", "transferability", "many-shot-jailbreaking", "gpt-4-turbo", "claude-2.0", "mistral-7b"]
sources: ["Chao 等 - 2024 - JailbreakBench An Open Robustness Benchmark for Jailbreaking Large Language Models.md", "Deng 等 - 2024 - MASTERKEY Automated Jailbreaking of Large Language Model Chatbots.md", "Ding 等 - 2023 - A Wolf in Sheep’s Clothing Generalized Nested Jailbreak Prompts can Fool Large Language Models Easi.md", "Gao 等 - 2024 - Inducing High Energy-Latency of Large Vision-Language Models with Verbose Images.md", "Guo 等 - 2024 - COLD-Attack Jailbreaking LLMs with Stealthiness and Controllability.md", "Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# GPT-4

## Overview

GPT-4 is a large language model developed by [[openai]]. It was tested alongside other state-of-the-art models for vulnerability to many-shot jailbreaking.

## Vulnerability to MSJ

GPT-4 showed susceptibility to many-shot jailbreaking attacks:

- Around 128-shot prompts were sufficient to induce harmful behavior
- The model followed predictable power law scaling relationships
- Effectiveness of MSJ was comparable across Claude 2.0, GPT-3.5, GPT-4, and other models tested

## Related Pages

- [[many-shot-jailbreaking]]
- [[openai]]
- [[gpt-3.5]]
- [[gpt-4-turbo]]