---
type: entity
title: "GPT-4o"
tags: ["target-model", "closed-source", "openai", "LLM", "API", "safety-aligned"]
related: ["gpt-3.5", "claude-3.5-sonnet", "llama-2-7b-chat", "vicuna-7b", "qwen-2.5-7b-instruct", "llama-3-8b-chat", "gemini-2.0-flash", "harmbench", "jailbreak-r1", "gpt-3.5-turbo", "gpt-4-turbo", "openai", "jailbreaking"]
sources: ["Guo 等 - 2025 - Jailbreak-R1 Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning.md", "Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# GPT-4o

## Επισκόπηση

Το GPT-4o είναι ένα από τα πιο πρόσφατα μοντέλα της OpenAI, σχεδιασμένο με προηγμένες δυνατότητες κατανόησης και παραγωγής πολυμέσων.

## Αποτελέσματα Έρευνας

Η έρευνα έδειξε ότι το προεπιλεγμένο prompt template ήταν εντελώς αναποτελεσματικό:

| Μέθοδος | ASR |
|---------|-----|
| Prompt | 0% |
| Custom Prompt | 72% |
| **Custom + RS + Self-Transfer** | **100%** |

## Τεχνικές Λεπτομέρειες

Χρειάστηκε προσαρμογή του prompt template σε system και user parts, καθώς και εκτεταμένη βελτιστοποίηση με random search.

## Σχετικές Σελίδες

- [[openai]]
- [[gpt-3.5-turbo]]
- [[gpt-4-turbo]]
- [[jailbreaking]]
- [[random-search]]
- [[self-transfer]]