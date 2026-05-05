---
type: entity
title: "Claude 3.5 Sonnet"
tags: ["target-model", "closed-source", "anthropic", "LLM", "API", "safety-aligned"]
related: ["gpt-3.5", "gpt-4o", "llama-2-7b-chat", "vicuna-7b", "qwen-2.5-7b-instruct", "llama-3-8b-chat", "gemini-2.0-flash", "harmbench", "jailbreak-r1", "claude-2.0", "claude-2.1", "claude-3-haiku", "claude-3-sonnet", "claude-3-opus", "jailbreaking"]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md", "Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Claude 3.5 Sonnet

## Επισκόπηση

Το Claude 3.5 Sonnet είναι ένα από τα πιο πρόσφατα μοντέλα της Anthropic με προηγμένη ευθυγράμμιση ασφαλείας.

## Ευπάθεια σε Επιθέσεις

| Μέθοδος | Ποσοστό Επιτυχίας |
|---------|-------------------|
| **Προτροπή + Transfer από GPT-4** | **96%** |
| **Προτροπή + Επίθεση Prefilling** | **100%** |

## Σημαντική Παρατήρηση

Η επίθεση prefilling επιτυγχάνει 100% ποσοστό επιτυχίας ακόμη και χωρίς τυχαία αναζήτηση.

## Σχετικές Σελίδες

- [[claude-2.0]]
- [[claude-2.1]]
- [[claude-3-haiku]]
- [[claude-3-sonnet]]
- [[claude-3-opus]]
- [[jailbreaking]]
- [[transfer-attack]]
- [[prefilling-attack]]
- [[anthropic]]