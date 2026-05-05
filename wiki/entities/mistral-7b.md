---
type: entity
title: "Mistral 7B"
tags: ["LLM", "model"]
related: ["claude-2.0", "gpt-4", "llama-2", "llama-2-70b", "many-shot-jailbreaking"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Mistral 7B

## Overview

Mistral 7B is a large language model developed by Mistral AI. It was tested alongside other state-of-the-art models for vulnerability to many-shot jailbreaking.

## Vulnerability to MSJ

Mistral 7B showed susceptibility to many-shot jailbreaking:

- Around 128-shot prompts were sufficient for the model to adopt harmful behavior
- Negative log-probability of jailbreak success followed predictable scaling laws
- The model entered a linear regime in log-log plots with enough shots

## Related Pages

- [[many-shot-jailbreaking]]
- [[llama-2-70b]]