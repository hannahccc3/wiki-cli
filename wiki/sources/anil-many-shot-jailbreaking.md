---
type: source
title: "Many-shot Jailbreaking"
authors: ["Cem Anil", "Esin Durmus", "Mrinank Sharma", "Joe Benton", "Sandipan Kundu", "Joshua Batson", "Nina Rimsky", "Meg Tong", "Jesse Mu", "Daniel Ford", "Francesco Mosconi", "Rajashree Agrawal", "Rylan Schaeffer", "Naomi Bashkansky", "Samuel Svenningsen", "Mike Lambert", "Ansh Radhakrishnan", "Carson Denison", "Evan J Hubinger", "Yuntao Bai", "Trenton Bricken", "Timothy Maxwell", "Nicholas Schiefer", "Jamie Sully", "Alex Tamkin", "Tamera Lanham", "Karina Nguyen", "Tomasz Korbak", "Jared Kaplan", "Deep Ganguli", "Samuel R. Bowman", "Ethan Perez", "Roger Grosse", "David Duvenaud"]
year: 2024
url: ""
venue: ""
tags: ["jailbreaking", "LLM security", "adversarial attacks", "in-context learning", "context windows", "alignment", "safety", "power laws", "large language models", "red teaming", "LLM safety", "model security", "model scaling"]
related: ["many-shot-jailbreaking", "in-context-learning", "power-laws", "greedy-coordinate-gradient", "in-context-defense", "cautionary-warning-defense", "claude-2.0", "gpt-3.5", "gpt-4", "llama-2-70b", "mistral-7b", "anthropic", "openai", "google-deepmind", "gcg", "alignment-finetuning", "power-law-scaling", "few-shot-jailbreaking", "jailbreak-composition", "llama-2"]
sources: ["Anil 等 - Many-shot Jailbreaking.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Many-shot Jailbreaking

## Overview

Many-shot Jailbreaking (MSJ) is a long-context adversarial attack that exploits hundreds of demonstrations of undesirable behavior to override safety guardrails in large language models. The research demonstrates that this technique effectively jailbreaks state-of-the-art LLMs including Claude 2.0, GPT-4, Llama 2, and Mistral 7B, and that attack effectiveness follows predictable power laws with the number of demonstrations.

## Key Findings

### Attack Effectiveness

- MSJ successfully jailbreaks multiple prominent LLMs across various tasks
- Attack effectiveness follows predictable power laws up to hundreds of shots
- Larger models are more susceptible due to faster in-context learning rates
- The attack works across diverse topics including weapons instructions, insults, and deceptive content

### Scaling Behavior

The researchers discovered that the effectiveness of MSJ follows a power law relationship:

```
-E[log P(harmful response | n-shot MSJ)] = Cn^(-α) + K
```

Where:
- `n` is the number of demonstrations
- `α` is the power law exponent (learning rate)
- `C` and `K` are constants

### Alignment Limitations

Standard alignment techniques (supervised learning and reinforcement learning) only affect the intercept but not the exponent of the power law. This means they delay but cannot prevent attacks at arbitrary context lengths. The key insight is that:

- **Intercept changes**: RL and SL reduce zero-shot probability of harmful behavior
- **Exponent remains constant**: The rate at which attacks become more effective with more shots does not decrease

## Methods Used

### Attack Construction
- Generated using "helpful-only" models (models without harmlessness training)
- Hundreds of compliant query-response pairs are randomized and formatted as dialogue
- The target query is appended to trigger the harmful response

### Composition with Other Attacks
MSJ can be combined with:
- **Competing objectives attacks**: Pits two conflicting objectives in prompts
- **GCG suffixes**: White-box adversarial suffix optimization

These combinations reduce the context length required for successful attacks.

## Defenses Evaluated

| Defense | Effectiveness | Notes |
|---------|---------------|-------|
| Supervised Learning | Limited | Only affects intercept, not exponent |
| Reinforcement Learning | Limited | Only affects intercept, not exponent |
| In-Context Defense (ICD) | Partial | Reduces success from 61% to 54% with 205 shots |
| Cautionary Warning Defense (CWD) | Better | Reduces effectiveness to 2% |

## Implications

1. **Context Windows as Attack Surface**: The expansion of LLM context windows from ~4,000 tokens to 10M tokens presents new vulnerabilities
2. **Safety Concerns for Large Models**: Larger models may be more susceptible to MSJ due to faster in-context learning
3. **Fundamental Challenge**: Protecting against MSJ without compromising benign ICL performance may be difficult since both appear to share underlying mechanisms

## Related Pages

- [[in-context-learning]]
- [[power-law-scaling]]
- [[alignment-finetuning]]
- [[gcg]]
- [[jailbreak-composition]]
- [[anthropic]]
- [[openai]]
- [[google-deepmind]]
- [[claude-2.0]]
- [[gpt-4]]
- [[mistral-7b]]
- [[llama-2]]
- [[induction-heads]]
- [[in-context-defense]]