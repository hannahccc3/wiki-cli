---
type: source
title: "Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks"
authors: ["Maksym Andriushchenko", "Francesco Croce", "Nicolas Flammarion"]
year: 2024
url: "https://github.com/tml-epfl/llm-adaptive-attacks"
venue: "SaTML'24 Trojan Detection Competition"
tags: ["Jailbreaking", "Ασφάλεια LLM", "Αντιπαραθετικές Επιθέσεις", "Ευθυγράμμιση Ασφαλείας", "LLM security", "adversarial attacks", "safety alignment", "red-teaming", "random search", "adaptive attacks", "prompt injection", "trojan detection", "language models", "LLM safety"]
related: ["jailbreaking", "adaptive-attacks", "safety-alignment", "random-search", "self-transfer", "transfer-attacks", "prefilling-attack", "trojan-detection", "llm-security", "transfer-attack", "advbench", "gcg", "pair", "logprobs", "harmbench", "deepwordbug", "bert-attack", "epfl"]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks

## Επισκόπηση

Αυτή η έρευνα από ερευνητές του EPFL αποδεικνύει ότι ακόμη και τα πιο πρόσφατα μοντέλα LLM με ευθυγράμμιση ασφαλείας (safety-aligned) δεν είναι ανθεκτικά σε απλές προσαρμοστικές επιθέσεις jailbreaking. Η μελέτη παρουσιάζει μεθόδους που επιτυγχάνουν 100% ποσοστό επιτυχίας επίθεσης σε όλα τα μοντέλα-στόχους.

## Βασικά Ευρήματα

- **Πλήρης πρόσβαση σε logprobs**: Επιτυγχάνεται 100% ποσοστό επιτυχίας σε μοντέλα όπως Vicuna-13B, Mistral-7B, Llama-2-Chat, GPT-3.5, GPT-4o
- **Μοντέλα Claude**: Χωρίς έκθεση logprobs, παρακάμπτονται με transfer ή prefilling επιθέσεις με 100% επιτυχία
- **Ανίχνευση Trojan**: Μέθοδος τυχαίας αναζήτησης που κέρδισε τον διαγωνισμό SaTML'24 Trojan Detection Competition

## Μέθοδοι Επίθεσης

### Τυχαία Αναζήτηση (Random Search)
Αλγόριθμος βελτιστοποίησης που τροποποιεί τυχαία tokens για να μεγιστοποιήσει την πιθανότητα επιτυχίας της επίθεσης.

### Self-Transfer
Τεχνική που χρησιμοποιεί επιτυχημένα adversarial suffixes από απλούστερες αιτήσεις ως αρχικοποίηση για πιο δύσκολες.

### Transfer Attack
Μεταφορά adversarial strings από ένα μοντέλο σε άλλο.

### Prefilling Attack
Προ-συμπλήρωση της απάντησης του LLM για παράκαμψη ασφαλειών.

## Πίνακας Αποτελεσμάτων

| Μοντέλο | Προηγούμενο ASR | Δικό μας ASR |
|---------|-----------------|--------------|
| Llama-2-Chat-7B | 92% | 100% |
| Llama-3-Instruct-8B | - | 100% |
| Gemma-7B | - | 100% |
| GPT-3.5 Turbo | 94% | 100% |
| Claude 2.0 | 61% | 100% |
| Claude 3.5 Sonnet | 50% | 100% |

## Συμπεράσματα

Η προσαρμοστικότητα είναι κρίσιμη για την αξιολόγηση της ανθεκτικότητας των LLM. Κανένα μεμονωμένο μέθοδος δεν μπορεί να γενικευτεί σε όλα τα μοντέλα-στόχους.

## Σχετικές Σελίδες

- [[jailbreaking]]
- [[safety-alignment]]
- [[adaptive-attacks]]
- [[random-search]]
- [[self-transfer]]
- [[transfer-attack]]
- [[prefilling-attack]]
- [[trojan-detection]]