---
type: source
title: "Πρόκληση Υψηλής Ενεργειακής Καθυστέρησης Μεγάλων Μοντέλων Όρασης-Γλώσσας με Λεπτομερείς Εικόνες"
tags:
  - Μοντέλα Όρασης-Γλώσσας
  - Ενεργειακή Καθυστέρηση
  - Αντιευαίσθητες Επιθέσεις
  - Λεπτομερείς Εικόνες
  - Πολυτροπική Μάθηση
related:
  - verbose-images
  - vision-language-models
  - blip
  - blip-2
  - instructblip
  - minigpt-4
  - gpt-4
  - delayed-eos-loss
  - uncertainty-loss
  - token-diversity-loss
  - temporal-weight-adjustment-algorithm
  - projected-gradient-descent
authors:
  - "Kuofeng Gao"
  - "Yang Bai"
  - "Jindong Gu"
  - "Shu-Tao Xia"
  - "Philip Torr"
  - "Zhifeng Li"
  - "Wei Liu"
year: 2024
url: "https://github.com/KuofengGao/Verbose_Images"
venue: ""
sources: ["Gao 等 - 2024 - Inducing High Energy-Latency of Large Vision-Language Models with Verbose Images.md"]
created: 2024-01-01
updated: 2024-12-15
---
# Πρόκληση Υψηλής Ενεργειακής Καθυστέρησης Μεγάλων Μοντέλων Όρασης-Γλώσσας με Λεπτομερείς Εικόνες

## Επισκόπηση

Αυτή η εργασία παρουσιάζει τις **Λεπτομερείς Εικόνες (Verbose Images)**, μια μέθοδο δημιουργίας αντιευαίσθητων διαταραχών που αναγκάζουν τα Μοντέλα Όρασης-Γλώσσας (VLMs) να παράγουν εξαιρετικά μακρές ακολουθίες κειμένου. Ο στόχος είναι να αυξηθεί η κατανάλωση ενέργειας και ο χρόνος καθυστέρησης κατά τη συμπερασματολογία, προκαλώντας εξάντληση υπολογιστικών πόρων.

## Κύρια Συνεισφορά

Οι συγγραφείς παρατηρούν ότι η κατανάλωση ενέργειας και ο χρόνος καθυστέρησης σχετίζονται θετικά γραμμικά με το μήκος των παραγόμενων ακολουθιών. Για να μεγιστοποιήσουν το μήκος, σχεδίασαν τρεις συναρτήσεις απώλειας:

1. **Απώλεια Καθυστέρησης EOS**: Ελαχιστοποιεί την πιθανότητα εμφάνισης του token τέλους ακολουθίας
2. **Απώλεια Αβεβαιότητας**: Μεγιστοποιεί την εντροπία για κάθε token
3. **Απώλεια Ποικιλομορφίας Tokens**: Μεγιστοποιεί τον πυρήνα της μήτρας κρυφών καταστάσεων

Επιπλέον, προτείνουν έναν **Αλγόριθμο Χρονικής Προσαρμογής Βαρών** για την εξισορρόπηση των τριών απωλειών.

## Πειραματικά Αποτελέσματα

Σε τέσσερα μοντέλα VLM (BLIP, BLIP-2, InstructBLIP, MiniGPT-4) και σε δύο datasets (MS-COCO, ImageNet), οι Λεπτομερείς Εικόνες επιτυγχάνουν:

- **Αύξηση μήκους ακολουθιών έως 7.87×** στο MS-COCO
- **Αύξηση μήκους ακολουθιών έως 8.56×** στο ImageNet

## Σχετικές Σελίδες

- [[verbose-images]]
- [[vision-language-models]]
- [[blip]]
- [[blip-2]]
- [[instructblip]]
- [[minigpt-4]]
- [[gpt-4]]
- [[delayed-eos-loss]]
- [[uncertainty-loss]]
- [[token-diversity-loss]]
- [[temporal-weight-adjustment-algorithm]]
- [[projected-gradient-descent]]
- [[sponge-samples]]
- [[nicgslowdown]]
- [[hallucination]]