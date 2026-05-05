---
type: source
title: "Many-shot Jailbreaking"
authors: ["Cem Anil", "Esin Durmus", "Mrinank Sharma", "Joe Benton", "Sandipan Kundu", "Joshua Batson", "Nina Rimsky", "Meg Tong", "Jesse Mu", "Daniel Ford", "Francesco Mosconi", "Rajashree Agrawal", "Rylan Schaeffer", "Naomi Bashkansky", "Samuel Svenningsen", "Mike Lambert", "Ansh Radhakrishnan", "Carson Denison", "Evan J Hubinger", "Yuntao Bai", "Trenton Bricken", "Timothy Maxwell", "Nicholas Schiefer", "Jamie Sully", "Alex Tamkin", "Tamera Lanham", "Karina Nguyen", "Tomasz Korbak", "Jared Kaplan", "Deep Ganguli", "Samuel R. Bowman", "Ethan Perez", "Roger Grosse", "David Duvenaud"]
year: 2024
url: ""
venue: ""
tags: ["jailbreaking", "LLM security", "adversarial attacks", "in-context learning", "context windows", "alignment", "safety", "power laws", "large language models", "red teaming", "LLM safety", "model security"]
related: ["many-shot-jailbreaking", "in-context-learning", "power-laws", "greedy-coordinate-gradient", "in-context-defense", "cautionary-warning-defense", "claude-2.0", "gpt-3.5", "gpt-4", "llama-2-70b", "mistral-7b", "anthropic", "openai", "google-deepmind", "gcg", "alignment-finetuning", "power-law-scaling", "few-shot-jailbreaking"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Many-shot Jailbreaking

## Overview

Many-shot Jailbreaking (MSJ) is a long-context attack technique that uses hundreds of demonstrations of undesirable behavior to steer large language models (LLMs) toward harmful responses. The research demonstrates that MSJ successfully jailbreaks multiple state-of-the-art models including Claude 2.0, GPT-3.5, GPT-4, Llama 2 70B, and Mistral 7B.

## Key Findings

### Effectiveness Across Models

MSJ demonstrates that attack effectiveness follows predictable power laws up to hundreds of shots. The technique successfully jailbreaks models from different developers across various tasks including:

- **Malicious use-cases**: Security and societal impact requests (weapons, disinformation)
- **Malevolent personality evals**: Queries assessing malign personality traits
- **Opportunities to insult**: Benign questions tricked into insulting responses

### Scaling Behavior

The research reveals that:

1. MSJ effectiveness follows predictable **[[power-law-scaling]]** patterns with increasing context length
2. Larger models tend to be more susceptible due to faster **[[in-context-learning]]** speeds
3. The attack is robust to format, style, and subject changes in prompt formatting

### Alignment Limitations

Standard **[[alignment-finetuning]]** techniques (supervised fine-tuning and reinforcement learning) only increase the power law intercept but do not reduce the exponent. This means:

- Attacks remain effective at sufficiently long context lengths
- Simply scaling up RL or SL training will not defend against MSJ at all context lengths

### Composition Attacks

MSJ can be combined with other jailbreak techniques:

- **[[composition-attacks]]** with competing objectives reduce required context length
- Composition with **[[gcg]]** adversarial suffix has mixed effects depending on shot count

## Mitigation Strategies Evaluated

### Prompt-Based Defenses

- **[[in-context-defense]]**: Only marginally reduces attack success rate (61% to 54%)
- **[[cautionary-warning-defense]]**: More effective but not fully protective

### Fine-tuning Approaches

Neither targeted **[[supervised-finetuning]]** nor targeted **[[reinforcement-learning]]** prevent MSJ at arbitrary context lengths, as they only increase intercept without reducing exponent.

## Implications

The findings suggest that **very long contexts present a rich new attack surface for LLMs**. Since the mechanisms underlying MSJ appear to be the same as general in-context learning, protecting against MSJ without harming benign ICL may prove challenging.

## Related Pages

- [[many-shot-jailbreaking]]
- [[in-context-learning]]
- [[gcg]]
- [[alignment-finetuning]]
- [[in-context-defense]]
- [[cautionary-warning-defense]]
- [[power-law-scaling]]
- [[few-shot-jailbreaking]]