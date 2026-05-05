---
type: concept
title: "Bit-flip Attack (Επίθεση Αναστροφής Bit)"
tags: ["AI_security", "Hardware_security", "Fault_injection", "Model_vulnerabilities", "Adversarial_ML"]
related: ["jailbreaking", "rowhammer", "prlsonbreak-attack", "hardware-aware-search", "hardware-agnostic-search", "exponent-bits"]
sources: ["Coalson 等 - 2025 - PrisonBreak Jailbreaking Large Language Models with at Most Twenty-Five Targeted Bit-flips.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Bit-flip Attack (Επίθεση Αναστροφής Bit)

## Ορισμός

Η **επίθεση αναστροφής bit (Bit-flip Attack)** είναι μια επίθεση που αναστρέφει στοιχειώδη bits στις παραμέτρους του μοντέλου για αλλαγή της συμπεριφοράς του. Αποτελεί μορφή έγχυσης σφαλμάτων (fault injection) που εκμεταλλεύεται τη φυσική αρχιτεκτονική της μνήμης.

## Βασικές Έννοιες

### Half-precision Floating-point (Float16)
Τα μοντέλα γλώσσας χρησιμοποιούν μορφή IEEE754 half-precision:
- **1 bit** πρόσημου (sign)
- **5 bits** εκθέτη (exponent)
- **10 bits** mantissa

### Exponent Bits (Bits Εκθέτη)
Τα bits του εκθέτη είναι ιδιαίτερα αποτελεσματικά:
- Αναστροφή mantissa bit: μικρή αλλαγή (π.χ. -1.75×2^-4 → -1.87×2^-4)
- Αναστροφή exponent bit: μεγάλη αλλαγή (π.χ. -1.75×2^-4 → -1.75×2^12)

## Bit-flip Onion Effect

**Φαινόμενο φλοιού αναστροφής bit**: Δύο flips που είναι ατομικά ωφέλιμα μπορεί να μην παραμένουν έτσι όταν εφαρμόζονται μαζί. Αυτό καθιστά την one-shot αναζήτηση ακατάλληλη.

## Μέθοδοι Αναζήτησης

### 1. One-shot Search
- Εκτίμηση σημασίας κάθε βάρους
- Ταυτόχρονη αναστροφή όλων των επιλεγμένων bits
- **Πρόβλημα**: Bit-flip onion effect

### 2. Progressive Search (Προοδευτική Αναζήτηση)
- Επαναληπτική επιλογή και αναστροφή **ενός bit** τη φορά
- Υιοθετείται από το PRISONBREAK

## Τεχνικές Επιτάχυνσης

1. **Gradient Sign**: Παράβλεψη bits με αντίθετο πρόσημο κλίσης
2. **Exponent Bits Focus**: Εστίαση στα 3 σημαντικότερα bits του εκθέτη
3. **0→1 Direction**: Προτίμηση αναστροφών 0→1 (μεγαλύτερες αλλαγές)

## Εφαρμογή σε LLM

Το **PRISONBREAK** επιτυγχάνει:
- **5-25 bit-flips** για 80-98% ASR
- **10^7-10^9 λιγότερες** τροποποιήσεις από άλλες επιθέσεις
- **-2.3%** μέση μεταβολή ακρίβειας

## Σχετικές Σελίδες

- [[jailbreaking]] - Jailbreaking γενικά
- [[prlsonbreak-attack]] - Η επίθεση PRISONBREAK
- [[rowhammer]] - Rowhammer ως μέθοδος αναστροφής
- [[exponent-bits]] - Bits εκθέτη
- [[progressive-bit-search]] - Προοδευτική αναζήτηση bit
- [[hardware-aware-search]] - Αναζήτηση με γνώση υλικού