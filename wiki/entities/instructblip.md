---
type: entity
title: "InstructBLIP"
tags:
  - Μοντέλο Όρασης-Γλώσσας
  - Instruction Tuning
  - Πολυτροπικό Μοντέλο
related:
  - blip
  - blip-2
  - minigpt-4
  - vision-language-models
  - verbose-images
sources: ["Gao 等 - 2024 - Inducing High Energy-Latency of Large Vision-Language Models with Verbose Images.md"]
created: 2024-01-01
updated: 2024-12-15
---
# InstructBLIP

## Επισκόπηση

Το **InstructBLIP** είναι μια επέκταση του BLIP-2 που χρησιμοποιεί **Instruction Tuning** για τη βελτίωση της κατανόησης οπτικής-γλωσσικής κατανόησης. Υιοθετεί προηγμένες τεχνικές fine-tuning για καλύτερη απόδοση σε πολυτροπικές εργασίες.

## Κύρια Χαρακτηριστικά

- **Instruction Tuning**: Χρήση οδηγιών για βελτίωση της κατανόησης
- **Βασίζεται σε**: BLIP-2 architecture
- **Γλωσσικό Μοντέλο**: Vicuna-7B
- **Δυνατότητες**: Ερωτήσεις-απαντήσεις, Λεζαντάρισμα, Οπτική συλλογιστική

## Απόδοση στις Λεπτομερείς Εικόνες

| Dataset | Μήκος (Αρχικό) | Μήκος (Verbose) | Αύξηση |
|---------|-----------------|------------------|--------|
| MS-COCO | 63.79 | 140.35 | 2.20× |
| ImageNet | 54.40 | 131.79 | 2.42× |

Παρόλο που δείχνει μικρότερη αύξηση από άλλα μοντέλα, το InstructBLIP εξακολουθεί να είναι ευάλωτο στις Λεπτομερείς Εικόνες.

## Σχετικές Σελίδες

- [[blip]]
- [[blip-2]]
- [[minigpt-4]]
- [[vision-language-models]]
- [[verbose-images]]