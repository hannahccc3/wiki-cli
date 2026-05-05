---
type: concept
title: "Progressive Bit-Search (Προοδευτική Αναζήτηση Bit)"
tags: ["AI_security", "Optimization", "Bit-flip_attacks", "Search_algorithms"]
related: ["bit-flip-attack", "prlsonbreak-attack", "gradient-based-ranking", "jailbreaking-score", "utility-score"]
sources: ["Coalson 等 - 2025 - PrisonBreak Jailbreaking Large Language Models with at Most Twenty-Five Targeted Bit-flips.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Progressive Bit-Search (Προοδευτική Αναζήτηση Bit)

## Ορισμός

Η **προοδευτική αναζήτηση bit** είναι μια διαδικασία επαναληπτικής επιλογής και αναστροφής ενός bit τη φορά. Αποτελεί βασικό συστατικό της επίθεσης PRISONBREAK για την αναγνώριση κρίσιμων θέσεων bit.

## Διαδικασία

1. **Αναγνώριση κρίσιμων βαρών**: Επιλογή βαρών με υψηλή σημασία (gradient-based ranking)
2. **Αναστροφή ενός bit**: Δοκιμή κάθε bit ξεχωριστά
3. **Αξιολόγηση**: Μέτρηση επίδρασης στο adversarial objective
4. **Επιλογή**: Επιλογή του πιο αποτελεσματικού bit
5. **Επανάληψη**: Συνέχεια μέχρι επίτευξη στόχου ASR

## Γιατί Progressive αντί One-shot

### One-shot Πρόβλημα: Bit-flip Onion Effect
- Δύο ατομικά ωφέλιμα flips μπορεί να μην παραμένουν ωφέλιμα μαζί
- Η συμπεριφορά του μοντέλου αλλάζει μετά από κάθε flip
- Καθιστά ταυτόχρονη αναστροφή αναξιόπιστη

### Progressive Πλεονεκτήματα
- Προσαρμοστική επιλογή βάσει τρέχουσας κατάστασης
- Μεγαλύτερη ακρίβεια στόχευσης
- Αποφυγή αρνητικών αλληλεπιδράσεων

## Βελτιστοποιήσεις Ταχύτητας

### 1. Gradient Sign Check
```
Αν sign(Δw) = sign(∇w) → Παράβλεψη (αύξηση loss)
Αλλιώς → Εξέταση
```
Μείωση bits προς εξέταση: ~50%

### 2. Exponent Bits Focus
- Εστίαση στα 3 σημαντικότερα bits του εκθέτη
- Παράδειγμα: ~1.5 bits ανά critical weight

### 3. 0→1 Direction Preference
- Μικρές τιμές βαρών → 0→1 flips δημιουργούν μεγαλύτερες αλλαγές
- Μείωση σε ~1 bit ανά weight

### Συνολική Επιτάχυνση
- **~20×** ταχύτερη από naive προσέγγιση
- Παράδειγμα: 177 ημέρες → ~9 ημέρες για LLAMA2-7B

## Σχετικές Σελίδες

- [[bit-flip-attack]] - Επίθεση αναστροφής bit
- [[prlsonbreak-attack]] - Η επίθεση PRISONBREAK
- [[gradient-based-ranking]] - Κατάταξη βάσει κλίσεων
- [[jailbreaking-score]] - Jailbreaking score
- [[utility-score]] - Utility score
- [[critical-weights]] - Κρίσιμα βάρη