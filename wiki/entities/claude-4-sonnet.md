---
type: entity
title: "Claude-4-Sonnet"
tags: ["LLM model", "komerční", "closed-source"]
related: ["qwen-2.5", "llama-3.1", "gpt-4.1", "deepseek-r1", "intent-shift-attack", "anthropic"]
sources: ["Ding 等 - 2025 - Friend or Foe How LLMs' Safety Mind Gets Fooled by Intent Shift Attack.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Claude-4-Sonnet

## Přehled

Claude-4-Sonnet je komerční velký jazykový model vyvinutý společností Anthropic. Model je součástí rodiny Claude 4 a je známý svými silnými bezpečnostními vlastnostmi a schopnostmi dlouhodobého uvažování.

## ISA experimenty

V článku o [[intent-shift-attack]] byl Claude-4-Sonnet testován jako cílový model. Výsledky ukázaly:

| Benchmark | Vanilla ASR | ISA ASR (nejlepší) | ASR Gain |
|-----------|-------------|---------------------|----------|
| AdvBench | 0% | 70% (Question Shift) | 70% |
| MaliciousInstruct | 1% | 63% (Mood Shift) | 62% |

## Klíčová zjištění

- Claude-4-Sonnet je nejodolnější model vůči standardním jailbreak útokům (0% ASR vůči baselines)
- Přesto je vysoce zranitelný vůči ISA (až 70% ASR)
- Toto odhaluje fundamentální slabinu v schopnosti modelu správně inferovat záměr

## Související stránky

- [[intent-shift-attack]]
- [[anthropic]]
- [[qwen-2.5]]
- [[llama-3.1]]
- [[gpt-4.1]]
- [[deepseek-r1]]
- [[question-shift]]
- [[mood-shift]]