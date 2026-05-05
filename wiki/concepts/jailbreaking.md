---
type: concept
title: "Jailbreaking"
tags: ["Ασφάλεια LLM", "Αντιπαραθετικές Επιθέσεις", "Ευθυγράμμιση Ασφαλείας", "jailbreaking", "LLM security", "adversarial attacks", "LLM safety", "security", "harmful content", "adversarial attack", "safety bypass", "AI_security", "LLM_security", "Model_alignment", "Adversarial_ML"]
related: ["safety-alignment", "adaptive-attacks", "random-search", "transfer-attacks", "prefilling-attack", "llm-security", "self-transfer", "many-shot-jailbreaking", "few-shot-jailbreaking", "adversarial-suffix", "composition-attack", "black-box-attack", "rl-jack", "white-box-attack", "in-context-learning", "genetic-algorithms", "bit-flip-attack", "prlsonbreak-attack", "rowhammer", "alignment-bypass"]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md", "Anil 等 - Many-shot Jailbreaking.md", "Chen 等 - 2024 - RL-JACK Reinforcement Learning-powered Black-box Jailbreaking Attack against LLMs.md", "Coalson 等 - 2025 - PrisonBreak Jailbreaking Large Language Models with at Most Twenty-Five Targeted Bit-flips.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Jailbreaking

## Ορισμός

Το **Jailbreaking** είναι μια μέθοδος αφαίρεσης της ασφαλειακής ευθυγράμμισης από μοντέλα γλώσσας για αποφυγή άρνησης επιβλαβών αιτημάτων. Πρόκειται για τεχνική που επιτρέπει σε έναν αντίπαλο να υποχρεώσει ένα μοντέλο να παράγει περιεχόμενο που κανονικά θα αρνούνταν να δημιουργήσει.

## Τύποι Jailbreaking

### 1. Prompt-based Jailbreaking
- Τροποποίηση των εισόδων (prompts) για παράκαμψη της ευθυγράμμισης
- Παραδείγματα: GCG, AutoDAN, PAIR
- Απαιτεί εξειδικευμένα προθέματα ή επιθέματα

### 2. Parameter-based Jailbreaking
- Τροποποίηση των παραμέτρων του μοντέλου
- Παραδείγματα: ORTHO, PRISONBREAK
- Μόνιμη αφαίρεση της ευθυγράμμισης στη μνήμη

### 3. Bit-flip Jailbreaking
- Αναστροφή ελάχιστων bits στις παραμέτρους
- **PRISONBREAK**: Μόλις 5-25 bit-flips για 80-98% ASR
- Δεν απαιτεί τροποποίηση εισόδων

## Σύγκριση Μεθόδων

| Μέθοδος | ASR | Τροποποιήσεις | Μόνιμη |
|---------|-----|---------------|--------|
| PRISONBREAK | 80-98% | 5-25 bits | Ναι |
| ORTHO | 80-94% | 0.7-23.4B παράμετροι | Ναι |
| GCG | 22-73% | Prompt-based | Όχι |

## Μηχανισμοί Άμυνας

Τα μοντέλα χρησιμοποιούν διάφορες τεχνικές ευθυγράμμισης:
- **SFT** (Supervised Fine-Tuning)
- **RLHF** (Reinforcement Learning from Human Feedback)
- **DPO** (Direct Preference Optimization)

## Σχετικές Σελίδες

- [[bit-flip-attack]] - Επίθεση αναστροφής bit
- [[prlsonbreak-attack]] - Η επίθεση PRISONBREAK
- [[rowhammer]] - Rowhammer ως τεχνική έγχυσης σφαλμάτων
- [[safety-alignment]] - Ασφαλειακή ευθυγράμμιση
- [[alignment-bypass]] - Παράκαμψη ευθυγράμμισης