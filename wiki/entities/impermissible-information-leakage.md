---
type: concept
title: "Διαρροή Απαγορευμένης Πληροφορίας (Impermissible Information Leakage)"
tags: ["information theory", "safety metrics", "LLM security", "risk quantification"]
related: ["inferential-adversaries", "information-censorship", "decomposition-attacks", "safety-utility-tradeoff"]
sources: ["Glukhov 等 - 2025 - BREACH BY A THOUSAND LEAKS UNSAFE INFORMA- TION LEAKAGE IN ‘SAFE’ AI RESPONSES.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Διαρροή Απαγορευμένης Πληροφορίας (Impermissible Information Leakage - IIL)

## Επισκόπηση

Η **Διαρροή Απαγορευμένης Πληροφορίας** είναι μια μετρική που ποσοτικοποιεί τον κίνδυνο ασφαλείας βαθμονομώντας τη διαφορά μεταξύ της πίστης του αντιπάλου στην ορθή απάντηση πριν και μετά την επίθεση.

## Μαθηματικός Ορισμός

Έστω:
- p_adv(a* | q): Η πίστη του ADVLLM στην ορθή απάντηση πριν την επίθεση
- p_adv(a* | h, q): Η πίστη του ADVLLM στην ορθή απάντηση μετά την επίθεση

Η διαρροή ορίζεται ως:

```
IIL = p_adv(a* | h, q) × log(p_adv(a* | h, q) / p_adv(a* | q))
```

## Ερμηνεία

- **Θετική τιμή**: Ο αντίπαλος απέκτησε περισσότερη πίστη στην ορθή απάντηση
- **Μηδενική τιμή**: Δεν υπήρξε αλλαγή στην πίστη
- **Βαθμονόμηση**: Η τιμή πολλαπλασιάζεται με την τελική πίστη p_adv(a* | h, q) για να αντικατοπτρίζει τον πραγματικό κίνδυνο

## Αναμενόμενη Διαρροή (Exp-IIL)

Για πολλαπλές αλληλεπιδράσεις, ορίζεται η **Αναμενόμενη Διαρροή Απαγορευμένης Πληροφορίας**:

```
Exp-IIL = Σ p_M(H_q^k = h^k) × Σ p_adv(a | h^k, q) × log(p_adv(a | h^k, q) / p_adv(a | q))
```

## Διάκριση από την Αμοιβαία Πληροφορία

Η Exp-IIL διαφέρει από την κλασική αμοιβαία πληροφορία (Mutual Information) διότι:

1. **Ασυμμετρία**: Εστιάζει μόνο στις απαντήσεις a ∈ A_q που είναι απαγορευμένες
2. **Ασφαλιστική στάθμιση**: Δεν θεωρεί αποτυχία άμυνας την περίπτωση που ο αντίπαλος γίνει πιο σίγουρος για μια επιτρεπτή απάντηση

## Σχετικές Σελίδες

- [[inferential-adversaries]]
- [[information-censorship]]
- [[decomposition-attacks]]
- [[safety-utility-tradeoff]]