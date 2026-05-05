---
type: entity
title: "Llama-3.1"
tags: ["LLM model", "open-source"]
related: ["qwen-2.5", "gpt-4.1", "claude-4-sonnet", "deepseek-r1", "intent-shift-attack"]
sources: ["Ding 等 - 2025 - Friend or Foe How LLMs' Safety Mind Gets Fooled by Intent Shift Attack.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Llama-3.1

## Přehled

Llama-3.1 je open-source velký jazykový model vyvinutý společností Meta. Model je součástí rodiny Llama a je dostupný v různých velikostech (např. 8B, 70B parametrů).

## ISA experimenty

V článku o [[intent-shift-attack]] byl Llama-3.1-8B-Instruct testován jako cílový model. Výsledky ukázaly:

| Benchmark | Vanilla ASR | ISA ASR (nejlepší) | ASR Gain |
|-----------|-------------|---------------------|----------|
| AdvBench | 0% | 74% (Mood Shift) | 74% |
| MaliciousInstruct | 2% | 64% (Voice/Mood/Question) | 62% |

## Klíčová zjištění

- ISA úspěšně obchází bezpečnostní mechanismy Llama-3.1
- Nejúčinnější transformace: **Mood Shift** a **Question Shift**
- Model systematicky misinterpretuje transformované požadavky jako neškodné dotazy na obecné znalosti

## Související stránky

- [[intent-shift-attack]]
- [[qwen-2.5]]
- [[gpt-4.1]]
- [[claude-4-sonnet]]
- [[deepseek-r1]]
- [[person-shift]]
- [[tense-shift]]
- [[voice-shift]]
- [[mood-shift]]
- [[question-shift]]