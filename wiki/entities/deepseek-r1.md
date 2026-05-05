---
type: entity
title: "DeepSeek-R1"
tags: ["LLM model", "reasoning", "open-source"]
related: ["qwen-2.5", "llama-3.1", "gpt-4.1", "claude-4-sonnet", "intent-shift-attack"]
sources: ["Ding 等 - 2025 - Friend or Foe How LLMs' Safety Mind Gets Fooled by Intent Shift Attack.md"]
created: 2025-01-01
updated: 2025-01-01
---
# DeepSeek-R1

## Přehled

DeepSeek-R1 je open-source velký jazykový model vyvinutý společností DeepSeek AI, který se specializuje na reasoning schopnosti. Model využívá reinforcement learning pro zlepšení svých reasoningových kapacit.

## ISA experimenty

V článku o [[intent-shift-attack]] byl DeepSeek-R1 testován jako cílový model. Výsledky ukázaly:

| Benchmark | Vanilla ASR | ISA ASR (nejlepší) | ASR Gain |
|-----------|-------------|---------------------|----------|
| AdvBench | 4% | 82% (Mood Shift) | 78% |
| MaliciousInstruct | 3% | 80% (Mood Shift) | 77% |

## Klíčová zjištění

- DeepSeek-R1, přes své explicitní reasoning schopnosti, vykazuje vysokou zranitelnost vůči ISA
- Nejúčinnější transformace: **Mood Shift** (82% ASR)
- Model systematicky misinterpretuje transformované požadavky jako neškodné

## Související stránky

- [[intent-shift-attack]]
- [[qwen-2.5]]
- [[llama-3.1]]
- [[gpt-4.1]]
- [[claude-4-sonnet]]
- [[mood-shift]]