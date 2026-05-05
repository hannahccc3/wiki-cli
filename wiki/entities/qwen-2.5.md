---
type: entity
title: "Qwen-2.5"
tags: ["LLM model", "open-source"]
related: ["llama-3.1", "gpt-4.1", "claude-4-sonnet", "deepseek-r1", "intent-shift-attack"]
sources: ["Ding 等 - 2025 - Friend or Foe How LLMs' Safety Mind Gets Fooled by Intent Shift Attack.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Qwen-2.5

## Přehled

Qwen-2.5 je open-source velký jazykový model vyvinutý společností Alibaba Cloud. Model je součástí rodiny Qwen a je dostupný v různých velikostech (např. 7B, 14B, 72B parametrů).

## ISA experimenty

V článku o [[intent-shift-attack]] byl Qwen-2.5-7B-Instruct testován jako cílový model. Výsledky ukázaly:

| Benchmark | Vanilla ASR | ISA ASR (nejlepší) | ASR Gain |
|-----------|-------------|---------------------|----------|
| AdvBench | 2% | 86% (Question Shift) | 84% |
| MaliciousInstruct | 2% | 77% (Mood Shift) | 75% |

## Klíčová zjištění

- ISA dosahuje vysoké úspěšnosti i na menších modelech
- Nejúčinnější transformace: **Question Shift** (86%) a **Mood Shift** (77%)
- Výrazné zlepšení ASR oproti vanilla promptům

## Související stránky

- [[intent-shift-attack]]
- [[llama-3.1]]
- [[gpt-4.1]]
- [[claude-4-sonnet]]
- [[deepseek-r1]]
- [[question-shift]]
- [[mood-shift]]