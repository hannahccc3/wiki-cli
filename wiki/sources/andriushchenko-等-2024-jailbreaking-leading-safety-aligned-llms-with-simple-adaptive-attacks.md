---
type: source
title: "Αποδιάρρηξη Κορυφαίων LLM με Ευθυγράμμιση Ασφαλείας μέσω Απλών Προσαρμοστικών Επιθέσεων"
authors: ["Maksym Andriushchenko", "Francesco Croce", "Nicolas Flammarion"]
year: 2024
url: "https://github.com/tml-epfl/llm-adaptive-attacks"
venue: ""
tags: ["Jailbreaking", "Ασφάλεια LLM", "Αντιπαραθετικές Επιθέσεις", "Ευθυγράμμιση Ασφαλείας", "LLM security", "adversarial attacks", "safety alignment", "red-teaming", "random search", "adaptive attacks", "prompt injection", "trojan detection", "language models", "LLM safety", "large language models"]
related: ["jailbreaking", "adaptive-attacks", "safety-alignment", "random-search", "self-transfer", "transfer-attacks", "prefilling-attack", "trojan-detection", "llm-security", "transfer-attack", "advbench", "gcg", "pair", "logprobs", "harmbench", "deepwordbug", "bert-attack", "epfl", "tap", "llama-2-chat-7b", "llama-3-instruct-8b", "gemma-7b", "gpt-3.5-turbo", "gpt-4o", "claude-2.0", "claude-3.5-sonnet", "r2d2-7b"]
sources: ["Andriushchenko 等 - 2024 - Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks.md"]
created: 2024-01-01
updated: 2024-01-01
---
# Αποδιάρρηξη Κορυφαίων LLM με Ευθυγράμμιση Ασφαλείας μέσω Απλών Προσαρμοστικών Επιθέσεων

## Επισκόπηση

Η εργασία αυτή καταδεικνύει ότι τα πιο πρόσφατα Μεγάλα Γλωσσικά Μοντέλα (LLM) με ευθυγράμμιση ασφαλείας δεν είναι ανθεκτικά σε απλές προσαρμοστικές επιθέσεις αποδιάρρηξης (jailbreaking). Οι συγγραφείς επιτυγχάνουν 100% ποσοστό επιτυχίας επίθεσης σε μοντέλα όπως Llama-2/3, GPT-3.5/4o, Claude και R2D2.

## Βασικά Ευρήματα

- **100% Ποσοστό Επιτυχίας**: Κανένα από τα κορυφαία LLM με ευθυγράμμιση ασφαλείας δεν είναι ανθεκτικό στις προτεινόμενες προσαρμοστικές επιθέσεις
- **Κρίσιμη Σημασία της Προσαρμοστικότητας**: Διαφορετικά μοντέλα είναι ευάλωτα σε διαφορετικά πρότυπα προτροπών
- **Απλότητα Μεθόδων**: Δεν απαιτούνται πληροφορίες κλίσεων ή βοηθητικά LLM

## Μεθοδολογία

Οι επιθέσεις βασίζονται σε:
1. **Πρότυπα Προτροπών**: Χειροποίητα σχεδιασμένα πρότυπα για κάθε μοντέλο
2. **Τυχαία Αναζήτηση**: Βελτιστοποίηση επιθημάτων σε επίθεμα (suffix) χωρίς κλίσεις
3. **Self-Transfer**: Αρχικοποίηση με επιτυχημένα επιθήματα από απλούστερα αιτήματα
4. **Επίθεση Prefilling**: Συμπλήρωση εκ των προτέρων της απόκρισης του LLM

## Στοχευόμενα Μοντέλα

| Μοντέλο | Εταιρεία | Ποσοστό Επιτυχίας |
|---------|----------|-------------------|
| Llama-2-Chat-7B | Meta | 100% |
| Llama-2-Chat-13B | Meta | 100% |
| Llama-2-Chat-70B | Meta | 100% |
| Llama-3-Instruct-8B | Meta | 100% |
| Gemma-7B | Google | 100% |
| GPT-3.5 Turbo | OpenAI | 100% |
| GPT-4o | OpenAI | 100% |
| Claude 2.0 | Anthropic | 100% |
| Claude 3.5 Sonnet | Anthropic | 100% |
| R2D2-7B | CAIS | 100% |

## Σχετικές Σελίδες

- [[jailbreaking]]
- [[safety-alignment]]
- [[adaptive-attacks]]
- [[random-search]]
- [[self-transfer]]
- [[prefilling-attack]]
- [[transfer-attack]]
- [[advbench]]
- [[gcg]]
- [[llama-2-chat-7b]]
- [[gpt-4o]]
- [[claude-3.5-sonnet]]
- [[r2d2-7b]]
- [[maksym-andriushchenko]]
- [[francesco-croce]]
- [[nicolas-flammarion]]
- [[epfl]]