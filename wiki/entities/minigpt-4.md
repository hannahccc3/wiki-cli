---
type: entity
title: "MiniGPT-4"
tags:
  - Μοντέλο Όρασης-Γλώσσας
  - Πολυτροπικό Μοντέλο
  - GPT-style
related:
  - blip
  - blip-2
  - instructblip
  - vision-language-models
  - verbose-images
sources: ["Gao 等 - 2024 - Inducing High Energy-Latency of Large Vision-Language Models with Verbose Images.md"]
created: 2024-01-01
updated: 2024-12-15
---
# MiniGPT-4

## Επισκόπηση

Το **MiniGPT-4** είναι ένα πολυτροπικό μοντέλο που συνδυάζει ικανότητες όρασης με ένα εξαιρετικά ισχυρό Γλωσσικό Μοντέλο (GPT-style). Έχει σχεδιαστεί για να επιτρέπει προηγμένη αλληλεπίδραση με οπτικά δεδομένα.

## Αρχιτεκτονική

Το MiniGPT-4 χρησιμοποιεί:

- **Vision Encoder**: Για την επεξεργασία εικόνων
- **Γλωσσικό Μοντέλο**: Vicuna-7B
- **Στρατηγική Fine-tuning**: Efficient alignment μεταξύ vision και language

## Απόδοση στις Λεπτομερείς Εικόνες

Το MiniGPT-4 δείχνει την **υψηλότερη κατανάλωση ενέργειας** μεταξύ των μοντέλων-στόχων:

| Dataset | Μήκος (Αρχικό) | Μήκος (Verbose) | Κατανάλωση Ενέργειας (J) |
|---------|-----------------|------------------|--------------------------|
| MS-COCO | 45.29 | 321.35 | 2113.29 |
| ImageNet | 40.93 | 321.24 | 2024.62 |

Το MiniGPT-4 επιδεικνύει εξαιρετική ευπάθεια, με αύξηση μήκους ακολουθιών έως **7.87×** και σημαντική κατανάλωση ενέργειας.

## Σχετικές Σελίδες

- [[blip]]
- [[blip-2]]
- [[instructblip]]
- [[vision-language-models]]
- [[verbose-images]]