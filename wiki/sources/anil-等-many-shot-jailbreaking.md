---
type: source
title: "Many-shot Jailbreaking"
authors: ["Cem Anil", "Esin Durmus", "Mrinank Sharma", "Joe Benton", "Sandipan Kundu", "Joshua Batson", "Nina Rimsky", "Meg Tong", "Jesse Mu", "Daniel Ford", "Francesco Mosconi", "Rajashree Agrawal", "Rylan Schaeffer", "Naomi Bashkansky", "Samuel Svenningsen", "Mike Lambert", "Ansh Radhakrishnan", "Carson Denison", "Evan J Hubinger", "Yuntao Bai", "Trenton Bricken", "Timothy Maxwell", "Nicholas Schiefer", "Jamie Sully", "Alex Tamkin", "Tamera Lanham", "Karina Nguyen", "Tomasz Korbak", "Jared Kaplan", "Deep Ganguli", "Samuel R. Bowman", "Ethan Perez", "Roger Grosse", "David Duvenaud"]
year: 2024
url: ""
venue: "Research paper (arXiv)"
tags: ["adversarial attacks", "LLM safety", "jailbreaking", "in-context learning", "alignment", "power laws", "long-context models", "red teaming", "model vulnerability", "context window attacks"]
related: ["many-shot-jailbreaking", "in-context-learning", "gcg", "alignment-pipeline", "few-shot-jailbreaking", "adversarial-suffix-attack"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Many-shot Jailbreaking

## Overview

Many-shot Jailbreaking (MSJ) is a long-context attack that exploits the expanded context windows of modern large language models (LLMs) by conditioning models on hundreds of demonstrations of undesirable behavior. This research, published in 2024, demonstrates that MSJ successfully jailbreaks multiple state-of-the-art models and follows predictable power law scaling relationships.

## Key Findings

### Attack Effectiveness

- MSJ is effective across diverse state-of-the-art LLMs including [[claude-2.0]], [[gpt-3.5]], [[gpt-4]], [[llama-2-70b]], and [[mistral-7b]]
- Attack effectiveness follows power laws over a wide range of tasks and context lengths up to ~70,000 tokens
- Larger models tend to be more susceptible to MSJ due to faster in-context learning speeds

### Alignment Limitations

Standard alignment techniques provide limited protection:

- [[supervised-fine-tuning]] (SL) increases the power law intercept but does not reduce the exponent
- [[reinforcement-learning]] (RL) alignment increases intercept but doesn't reduce MSJ scaling exponent
- Attacks remain effective at sufficient context lengths regardless of alignment training

### Composability

MSJ can be composed with other jailbreaks to reduce context length requirements:

- Combining with competing objectives attack increases effectiveness at all context lengths
- Composition with [[gcg]] (Greedy Coordinate Gradient) shows mixed results depending on shot count

## Methodology

The attack works by:
1. Generating hundreds of demonstrations of undesirable behavior using a "helpful-only" model
2. Randomizing the order of demonstrations
3. Formatting as standard dialogue between user and assistant
4. Appending the target query

## Implications

The research demonstrates that safety training does not eliminate in-context scaling of harmful behaviors, highlighting that this vulnerability is intrinsic to [[in-context-learning]] mechanisms. Very long contexts present a rich new attack surface for LLMs.

## Related Pages

- [[many-shot-jailbreaking]] - Main concept page
- [[in-context-learning]] - Related mechanism
- [[alignment-pipeline]] - Related training process
- [[gcg]] - Related attack method