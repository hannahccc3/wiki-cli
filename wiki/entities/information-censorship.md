---
type: concept
title: "Λογοκρισία Πληροφορίας (Information Censorship)"
tags: ["defense mechanism", "LLM security", "information theory", "safety guarantees"]
related: ["information-censorship-mechanism", "inferential-adversaries", "safety-utility-tradeoff", "impermissible-information-leakage"]
sources: ["Glukhov 等 - 2025 - BREACH BY A THOUSAND LEAKS UNSAFE INFORMA- TION LEAKAGE IN ‘SAFE’ AI RESPONSES.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Λογοκρισία Πληροφορίας (Information Censorship)

## Επισκόπηση

Η **Λογοκρισία Πληροφορίας** είναι ένας αμυντικός μηχανισμός που οριοθετεί την αναμενόμενη διαρροή απαγορευμένης πληροφορίας (Exp-IIL). Αποτελεί μια συνθήκη που πρέπει να πληρούν οι μηχανισμοί άμυνας για να εγγυηθούν ασφάλεια έναντι υποθετικών αντιπάλων.

## Μηχανισμός Λογοκρισίας (Censorship Mechanism)

### Ορισμός

Ένας **Μηχανισμός Λογοκρισίας** M: X × P(Y) → P(Y) είναι μια τυχαιοποιημένη συνάρτηση που εξάγει μια νέα κατανομή επί των απαντήσεων που επιστρέφονται στον χρήστη.

### Στόχος

Ο μηχανισμός M επιδιώκει να διασφαλίσει ότι οι απαντήσεις ικανοποιούν ένα κριτήριο ασφαλείας ανάλογα με το υποθετικό μοντέλο απειλής.

## Μηχανισμός Λογοκρισίας Πληροφορίας (ICM)

### Ορισμός ((k, ε)-ICM)

Για μια συλλογή προηγούμενων αντιπάλων Φ, μια κακόβουλη ερώτηση q ∈ Q, ένα όριο διαρροής ε > 0, και k πιθανές αλληλεπιδράσεις, ένα **(k, ε)-ICM** M διασφαλίζει ότι:

```
sup I_Aq(p_adv(·|q); H_qi^k) ≤ ε
```

για όλες τις κατανομές αντιπάλων και τα σύνολα ερωτήσεων.

## Συνθετικά Όρια

### Μη-Προσαρμοστική Συνθεσιμότητα

Το ICM για μία αλληλεπίδραση (1, ε)-ICM μπορεί να παρέχει όρια για k αλληλεπιδράσεις:

```
sup I_Aq ≤ kε + Σ I_Aq((qj, aj); H_qi^(j-1) | p_adv(·|q))
```

Το άθροισμα παραμένει kε αν οι έξοδοι είναι ντετερμινιστικές ή ανεξάρτητες.

## Σχετικές Σελίδες

- [[inferential-adversaries]]
- [[impermissible-information-leakage]]
- [[safety-utility-tradeoff]]
- [[randomized-response]]