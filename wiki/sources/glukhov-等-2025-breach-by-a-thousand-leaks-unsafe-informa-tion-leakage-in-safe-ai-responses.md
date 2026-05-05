---
type: source
title: "BREACH BY A THOUSAND LEAKS: UNSAFE INFORMATION LEAKAGE IN 'SAFE' AI RESPONSES"
authors: ["David Glukhov", "Ziwen Han", "Vardan Papyan", "Nicolas Papernot", "Ilia Shumailov"]
year: 2025
url: ""
venue: ""
tags: ["AI safety", "LLM security", "information leakage", "jailbreaking", "decomposition attacks", "inferential adversaries", "information theory"]
related: ["decomposition-attacks", "inferential-adversaries", "security-adversaries", "impermissible-information-leakage", "information-censorship", "safety-utility-tradeoff", "david-glukhov", "ziwen-han", "vardan-papyan", "nicolas-papernot", "ilia-shumailov", "university-of-toronto", "vector-institute", "university-of-oxford"]
sources: ["Glukhov 等 - 2025 - BREACH BY A THOUSAND LEAKS UNSAFE INFORMA- TION LEAKAGE IN ‘SAFE’ AI RESPONSES.md"]
created: 2025-01-01
updated: 2025-01-01
---
# BREACH BY A THOUSAND LEAKS: UNSAFE INFORMATION LEAKAGE IN 'SAFE' AI RESPONSES

## Επισκόπηση

Αυτή η ερευνητική εργασία του 2025 αποκαλύπτει μια κρίσιμη ευπάθεια στα προηγμένα γλωσσικά μοντέλα (LLMs), όπου οι αντίπαλοι μπορούν να εξαγάγουν επικίνδυνη γνώση μέσω φαινομενικά ακίνδυνων υποερωτήσεων χωρίς να ενεργοποιούν παραδοσιακές άμυνες.

## Βασικά Ευρήματα

### Επιθέσεις Αποσύνθεσης (Decomposition Attacks)

Οι συγγραφείς εισάγουν τις **Επιθέσεις Αποσύνθεσης** ως μια αυτοματοποιημένη μέθοδο που υπερτερεί των παραδοσιακών τεχνικών jailbreaking. Η επίθεση:

- Αποσυνθέτει κακόβουλες ερωτήσεις σε ακίνδυνα υποερωτήματα
- Υποβάλλει τα υποερωτήματα στο θύμα LLM
- Συγκεντρώνει τις απαντήσεις για να απαντήσει στην αρχική κακόβουλη ερώτηση

### Μοντέλο Απειλής: Υποθετικοί Αντίπαλοι (Inferential Adversaries)

Η εργασία διακρίνει μεταξύ δύο τύπων αντιπάλων:

1. **Υποθετικοί Αντίπαλοι**: Επιδιώκουν να συλλέξουν απαγορευμένη γνώση από τις εξόδους του θύματος
2. **Αντίπαλοι Ασφαλείας**: Επιδιώκουν να αναγκάσουν το θύμα να παράγει συγκεκριμένες απαγορευμένες εξόδους

### Πλαίσιο Αξιολόγησης

Οι συγγραφείς αναπτύσσουν ένα πλαίσιο θεωρίας πληροφοριών που περιλαμβάνει:

- **Impermissible Information Leakage (IIL)**: Μετρική για την ποσοτικοποίηση του κινδύνου ασφαλείας
- **Information Censorship**: Αμυντικός μηχανισμός για τον περιορισμό της διαρροής απαγορευμένης πληροφορίας

## Συμπεράσματα

Η εργασία υποστηρίζει ότι η ευρωστία (robustness) είναι θεμελιωδώς ανεπαρκής για την επίτευξη στόχων ασφάλειας. Οι αποτελεσματικές άμυνες περιορίζουν αναπόφευκτα τη χρησιμότητα τόσο για κακόβουλους όσο και για καλοήθεις χρήστες.

## Σχετικές Σελίδες

- [[decomposition-attacks]]
- [[inferential-adversaries]]
- [[security-adversaries]]
- [[impermissible-information-leakage]]
- [[information-censorship]]
- [[safety-utility-tradeoff]]
- [[david-glukhov]]
- [[nicolas-papernot]]
- [[ilia-shumailov]]
- [[university-of-toronto]]
- [[vector-institute]]
- [[university-of-oxford]]