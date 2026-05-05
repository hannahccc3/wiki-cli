---
type: entity
title: "ROCKET (Real-wOrld attaCK based on hEurisTic rules)"
tags: ["attack", "heuristic", "black-box", "adversarial"]
related: [["advbench"], ["heuristic-rules"], ["black-box-attack"], ["adversarial-samples"], ["deepwordbug"]]
sources: ["Chen 等 - 2022 - Why Should Adversarial Perturbations be Imperceptible Rethink the Research Paradigm in Adversarial.md"]
created: 2024-01-15
updated: 2024-01-15
---
# ROCKET

## Επισκόπηση

Το **ROCKET** (Real-wOrld attaCK based on hEurisTic rules) είναι μια απλή μέθοδος επίθεσης που προτάθηκε για την προσομοίωση πραγματικών επιθέσεων σε συστήματα NLP ασφαλείας. Η μέθοδος βασίζεται σε ευριστικούς κανόνες που συνοψίζονται από διάφορες πηγές, συμπεριλαμβανομένων πραγματικών δεδομένων χρηστών, εμπειρίας ειδικών, και αναφορών από διαγωνισμούς ασφαλείας.

## Κανόνες Διαταραχής

Η μέθοδος ROCKET χρησιμοποιεί **6 βασικούς ευριστικούς κανόνες**:

| Κανόνας | Περιγραφή | Παράδειγμα |
|---------|-----------|------------|
| (1) Εισαγωγή Κενού | Τυχαία εισαγωγή κενού | foolish → foo lish |
| (2) Εισαγωγή Άσχετου | Τυχαία εισαγωγή χαρακτήρα | foolish → foo^lish |
| (3) Διαγραφή | Τυχαία διαγραφή χαρακτήρα | foolish → foolih |
| (4) Ανταλλαγή | Ανταλλαγή δύο γειτονικών χαρακτήρων | foolish → foolihs |
| (5) Υποκατάσταση | Τυχαία υποκατάσταση χαρακτήρα | foolish → foo1ish |
| (6) Προσθήκη Αποσπάσματος | Προσθήκη αποσπασματικής πρότασης | fuck! → fuck peace!! |

## Αλγόριθμος Αναζήτησης

Η ROCKET λειτουργεί σε **ρύθμιση black-box** όπου μόνο οι αποφάσεις των μοντέλων-θυμάτων είναι προσβάσιμες:

1. Εφαρμογή κανόνα (6) στην αρχική πρόταση
2. Διήθηση stop words για λήψη σημασιολογικής λίστας λέξεων L
3. Επανάληψη της διαδικασίας διαταραχής λέξεων μέχρι να εξαπατηθεί το μοντέλο

## Απόδοση

Σε σύγκριση με άλλες μεθόδους όπως TextFooler, PWWS, BERT-Attack, SememePSO και DeepWordBug, η ROCKET δείχνει υπεροχή σε:

- **Ποσοστό Επιτυχίας Επίθεσης (ASR)**: Επιτυγχάνει υψηλότερα ποσοστά σε πολλές εργασίες
- **Αποδοτικότητα Ερωτημάτων**: Απαιτεί σημαντικά λιγότερα ερωτήματα
- **Εγκυρότητα**: Διατηρεί καλά το επιθετικό νόημα

## Σχετικές Σελίδες

- [[advbench]]
- [[heuristic-rules]]
- [[black-box-attack]]
- [[adversarial-samples]]
- [[deepwordbug]]
- [[textfooler]]
- [[bert-attack]]