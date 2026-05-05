---
type: source
title: "PRISONBREAK: Jailbreaking Μεγάλων Μοντέλων Γλώσσας με Πολλά Είκοσι-Πέντε Στοχευμένα Bit-flips"
authors: ["Zachary Coalson", "Jeonghyun Woo", "Chris S. Lin", "Joyce Qu", "Yu Sun", "Shiyang Chen", "Lishang Yang", "Gururaj Saileshwar", "Prashant J. Nair", "Bo Fang", "Sanghyun Hong"]
year: 2025
url: ""
venue: "Oregon State University, University of British Columbia, University of Toronto, George Mason University, Rutgers University, University of Texas at Arlington"
tags: ["AI_security", "LLM_jailbreaking", "Bit-flip_attacks", "Rowhammer", "Fault_injection", "Model_safety", "Adversarial_ML", "Hardware_security", "Alignment_bypass", "Deep_learning_vulnerabilities"]
related: ["jailbreaking", "bit-flip-attack", "rowhammer", "prlsonbreak-attack", "gradient-based-ranking", "progressive-bit-search", "hardware-aware-search", "hardware-agnostic-search", "vicuna-13b-v1.5", "llama-2", "llama-3-70b"]
sources: ["Coalson 等 - 2025 - PrisonBreak Jailbreaking Large Language Models with at Most Twenty-Five Targeted Bit-flips.md"]
created: 2025-01-15
updated: 2025-01-15
---
# PRISONBREAK: Jailbreaking Μεγάλων Μοντέλων Γλώσσας με Πολλά Είκοσι-Πέντε Στοχευμένα Bit-flips

## Επισκόπηση

Η εργασία παρουσιάζει το **PRISONBREAK**, μια επαναστατική επίθεση που αφαιρεί την ασφαλειακή ευθυγράμμιση (jailbreak) από μεγάλα μοντέλα γλώσσας αναστρέφοντας μόλις **5-25 bits** στις παραμέτρους τους. Η επίθεση επιτυγχάνει ποσοστά επιτυχίας (ASR) της τάξης του **80-98%** με ελάχιστη επίδραση στη χρησιμότητα του μοντέλου.

## Βασικά Ευρήματα

### Αποτελεσματικότητα Επίθεσης
- Τα μοντέλα γλώσσας μπορούν να υποστούν jailbreak με μόλις **5-25 bit-flips**
- Απαιτούνται **10^7-10^9 λιγότερες** τροποποιήσεις παραμέτρων σε σύγκριση με άλλες επιθέσεις
- Τα **exponent bits** και τα **value projection layers** είναι δυσανάλογα ευάλωτα
- Η επίθεση λειτουργεί μηχανιστικά διαφορετικά από prompt-based jailbreaks

### Rowhammer σε GPU
- Εφαρμογή της επίθεσης με **Rowhammer σε GPU GDDR6**
- Επίτευξη **ASR 69-91%** με μόλις **δύο φυσικές θέσεις bit**
- Χρήση τεχνικών όπως memory templating και massaging

### Αντίκτυπος στη Χρησιμότητα
- Μέση μεταβολή ακρίβειας: **-2.3%** (ελάχιστη υποβάθμιση)
- Τα μοντέλα με ασθενέστερη post-training alignment απαιτούν λιγότερα bit-flips

## Μεθοδολογία

### Προοδευτική Αναζήτηση Bit (Progressive Bit-Search)
1. Αναγνώριση κρίσιμων βαρών βάσει κλίσεων
2. Επαναληπτική επιλογή και αναστροφή ενός bit τη φορά
3. Αξιολόγηση με βάση το **jailbreaking score** και το **utility score**

### Τεχνικές Επιτάχυνσης
- **Gradient sign**: Παράβλεψη bits με αντίθετο πρόσημο
- **Exponent bits**: Εστίαση στα πιο σημαντικά bits του εκθέτη
- **0→1 flip direction**: Προτίμηση αναστροφών 0→1

### Λειτουργία Δύο Λειτουργιών
- **Hardware-agnostic**: Αναζήτηση χωρίς περιορισμούς υλικού
- **Hardware-aware**: Αναζήτηση με γνώση ευάλωτων φυσικών θέσεων μνήμης

## Αξιολόγηση

### Δοκιμασμένα Μοντέλα
Η επίθεση δοκιμάστηκε σε **10 ανοιχτού κώδικα μοντέλα** από 5 οικογένειες:
- VICUNA (7B, 13B)
- LLAMA2 CHAT (7B, 13B)
- LLAMA3 INSTRUCT (8B, 70B)
- TULU3 (8B)
- QWEN2 INSTRUCT (1.5B, 7B)

### Σύγκριση με Άλλες Επιθέσεις
| Επίθεση | Μέσο ASR | Τροποποιημένες Παράμετροι |
|---------|----------|---------------------------|
| PRISONBREAK | 89.6% | 5-25 bits |
| ORTHO | 79.8% | 0.7-23.4 δισ. παράμετροι |
| BASELINE BFA | 67.3% | 2-25 bits |
| GCG-M | 51.9% | Prompt-based |

## Σχετικές Σελίδες

- [[jailbreaking]] - Η έννοια του jailbreaking
- [[bit-flip-attack]] - Επιθέσεις αναστροφής bit
- [[rowhammer]] - Τεχνική έγχυσης σφαλμάτων
- [[progressive-bit-search]] - Προοδευτική αναζήτηση bit
- [[gradient-based-ranking]] - Κατάταξη βάσει κλίσεων
- [[hardware-aware-search]] - Αναζήτηση με γνώση υλικού
- [[hardware-agnostic-search]] - Αναζήτηση χωρίς περιορισμούς
- [[victim-llms]] - Μοντέλα-στόχοι της επίθεσης
- [[prlsonbreak-attack]] - Η επίθεση PRISONBREAK