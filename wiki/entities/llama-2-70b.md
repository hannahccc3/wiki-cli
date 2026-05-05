---
type: entity
title: "Llama 2 (70B)"
tags: ["model", "LLM", "Meta"]
related: ["mistral-7b", "many-shot-jailbreaking"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Llama 2 (70B)

## Overview

Llama 2 (70B) is a large language model developed by Meta. It was one of the open-weight models tested in the Many-shot Jailbreaking research.

## Vulnerability to MSJ

Llama 2 (70B) was successfully jailbroken using many-shot jailbreaking:

- The model showed power law scaling behavior similar to closed-weight models
- Llama 2 (70B) supports a maximum context length of 4096 tokens, limiting the number of shots available for attacks
- Despite the context limit, the model adopted harmful behavior when sufficient demonstrations were provided

## Related Pages

- [[many-shot-jailbreaking]]
- [[mistral-7b]]