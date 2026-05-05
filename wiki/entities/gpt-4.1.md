---
type: entity
title: "GPT-4.1"
tags: ["LLM model", "komerční", "closed-source"]
related: ["qwen-2.5", "llama-3.1", "claude-4-sonnet", "deepseek-r1", "intent-shift-attack", "openai"]
sources: ["Ding 等 - 2025 - Friend or Foe How LLMs' Safety Mind Gets Fooled by Intent Shift Attack.md"]
created: 2025-01-01
updated: 2025-01-01
---
# GPT-4.1

## Přehled

GPT-4.1 je komerční velký jazykový model vyvinutý společností [[openai]]. Jedná se o pokročilý model optimalizovaný pro různé úkoly včetně programování, analytiky a konverzačních aplikací.

## ISA experimenty

V článku o [[intent-shift-attack]] byl GPT-4.1 testován jako cílový model. Výsledky ukázaly:

| Benchmark | Vanilla ASR | ISA ASR (nejlepší) | ASR Gain |
|-----------|-------------|---------------------|----------|
| AdvBench | 0% | 72% (Person/Question) | 72% |
| MaliciousInstruct | 1% | 73% (Mood/Question) | 72% |

## Klíčová zjištění

- GPT-4.1 je zranitelný vůči ISA i přes pokročilé bezpečnostní mechanismy
- Nejúčinnější transformace: **Person Shift**, **Mood Shift** a **Question Shift**
- ISA dosahuje 72% ASR i na komerčních modelech

## Související stránky

- [[intent-shift-attack]]
- [[openai]]
- [[qwen-2.5]]
- [[llama-3.1]]
- [[claude-4-sonnet]]
- [[deepseek-r1]]