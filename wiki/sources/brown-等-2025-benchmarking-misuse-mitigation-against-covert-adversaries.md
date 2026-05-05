---
type: source
title: "Benchmarking Misuse Mitigation Against Covert Adversaries"
authors: ["Davis Brown", "Mahdi Sabbaghi", "Luze Sun", "Alexander Robey", "George J. Pappas", "Eric Wong", "Hamed Hassani"]
year: 2025
url: ""
venue: ""
tags: ["AI safety", "LLM security", "misuse mitigation", "covert attacks", "decomposition attacks", "stateful defenses", "red teaming", "jailbreaking", "threat modeling", "benchmarking", "Ασφάλεια LLM", "Κατάχρηση Μοντέλων", "Επιθέσεις Αποσύνθεσης", "Jailbreaks", "Καταστάσεις Άμυνας", "Μετάδοση Κατάχρησης", "LLM safety", "covert adversaries", "adversarial attacks", "AI security", "model alignment"]
related: ["bsd-pipeline", "decomposition-attacks", "stateful-defenses", "misuse-uplift", "frontier-models", "open-weight-models", "jailbreaks", "threat-model", "bsd", "["benchmarks-for-stateful-defenses", "jailbreaking", "red-teaming"]]
sources: ["Brown 等 - 2025 - Benchmarking Misuse Mitigation Against Covert Adversaries.md"]
created: 2025-01-15
updated: 2025-01-15
---
# Benchmarking Misuse Mitigation Against Covert Adversaries

## Επισκόπηση

Αυτή η εργασία παρουσιάζει το **Benchmarks for Stateful Defenses (BSD)**, ένα pipeline δημιουργίας συνθετικών δεδομένων για την αυτοματοποιημένη μέτρηση του **misuse uplift** (ανύψωση κατάχρησης) και της ανιχνευσιμότητας κρυφών επιθέσεων σε μοντέλα γλωσσικής τεχνητής νοημοσύνης. Οι συγγραφείς αποδεικνύουν ότι οι **επιθέσεις αποσύνθεσης** (decomposition attacks) είναι ιδιαίτερα αποτελεσματικές στην ανύψωση της κατάχρησης μοντέλων, ξεπερνώντας τα state-of-the-art jailbreaks, και ότι οι **stateful defenses** (αμυντικές με κατάσταση) προσφέρουν μια υποσχόμενη αντίμετρο αλλά δεν είναι πλήρως αποτελεσματικές έναντι προσαρμοστικών επιθέσεων.

## Βασικά Ευρήματα

### 1. Αδυναμίες Υφιστάμενων Benchmarks

Τα υπάρχοντα benchmarks ασφαλείας αξιολόγησης εστιάζουν σε φανερές επιθέσεις και απλές εργασίες χαμηλού κινδύνου. Ωστόσο, οι ρεαλιστικοί επιτιθέμενοι μπορούν να παρακάμψουν τα τρέχοντα μέτρα ασφαλείας:

- **Χρήση ανοιχτών μοντέλων**: Τα open-weight μοντέλα (π.χ. Qwen2.5-7B) μπορούν εύκολα να fine-tune για αφαίρεση μηχανισμών άρνησης
- **Αναζήτηση στο διαδίκτυο**: Για πολλές επιβλαβείς πληροφορίες, οι απλές αναζητήσεις επαρκούν
- **Ανίχνευση jailbreaks**: Οι παραδοσιακές επιθέσεις απόδρασης είναι εύκολα ανιχνεύσιμες

### 2. Επιθέσεις Αποσύνθεσης (Decomposition Attacks)

Η βασική επίθεση που μελετάται είναι η **αποσύνθεση επιβλαβών εργασιών** σε φαινομενικά καλοήθη υποερωτήματα:

1. Ένας επιτιθέμενος αποσυνθέτει μια επιβλαβή ερώτηση σε απλές, ακίνδυνες υποερωτήσεις
2. Οι υποερωτήσεις αποστέλλονται σε ισχυρά αλλά ευθυγραμμισμένα μοντέλα (π.χ. Claude-3.5-Sonnet, GPT-4o)
3. Οι απαντήσεις συντίθενται από αδύναμα αλλά μη ευθυγραμμισμένα μοντέλα
4. Αυτό αποφεύγει την ανίχνευση καθώς τα ισχυρά μοντέλα δεν βλέπουν ποτέ ρητά επιβλαβείς ερωτήσεις

### 3. Αποτελέσματα Αξιολόγησης

Ο πίνακας αποτελεσμάτων δείχνει σημαντική αύξηση του misuse rate (ποσοστό κατάχρησης) με επιθέσεις αποσύνθεσης:

| Μοντέλο | Άμεσο Ερώτημα | Επίθεση Αποσύνθεσης |
|---------|---------------|---------------------|
| Claude-3.5-Sonnet | 0.03 | 0.39 |
| Claude-3.7-Sonnet | 0.15 | 0.43 |
| GPT-4o | 0.58 | 0.65 |
| o3-mini | 0.84 | 0.81 |
| o3 | 0.09 | 0.51 |

### 4. Stateful Defenses

Οι αμυντικές στρατηγικές με κατάσταση παρακολουθούν ακολουθίες ερωτήσεων χρηστών για ανίχνευση κακόβουλων μοτίβων. Η μέθοδος περιλαμβάνει:

- Διατήρηση ενός "buffer" με τα πιο ύποπτα ερωτήματα
- Χρήση in-context learning για αναγνώριση μοτίβων κατάχρησης
- Σημαντική βελτίωση στην ανίχνευση σε σύγκριση με μεμονωμένες αναλύσεις

## Συμπεράσματα

1. Οι επιθέσεις αποσύνθεσης υπερτερούν σημαντικά των παραδοσιακών jailbreaks
2. Τα υφιστάμενα benchmarks είναι πολύ εύκολα και δεν μετρούν ρεαλιστικές απειλές
3. Οι stateful defenses δείχνουν υπόσχεση αλλά δεν είναι πλήρως αποτελεσματικές
4. Η κλιμάκωση του αριθμού αποσυνθέσεων βελτιώνει σταθερά την ακρίβεια των επιθέσεων

## Σχετικές Σελίδες

- [[benchmarks-for-stateful-defenses]]
- [[decomposition-attacks]]
- [[misuse-uplift]]
- [[stateful-defenses]]
- [[jailbreaking]]
- [[red-teaming]]