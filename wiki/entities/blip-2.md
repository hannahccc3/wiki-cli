---
type: entity
title: "BLIP-2"
tags:
  - Μοντέλο Όρασης-Γλώσσας
  - Πολυτροπικό Μοντέλο
  - Query Transformer
related:
  - blip
  - instructblip
  - minigpt-4
  - vision-language-models
  - verbose-images
sources: ["Gao 等 - 2024 - Inducing High Energy-Latency of Large Vision-Language Models with Verbose Images.md"]
created: 2024-01-01
updated: 2024-12-15
---
# BLIP-2

## Επισκόπηση

Το **BLIP-2** είναι μια εξέλιξη του BLIP που εισάγει τον **Query Transformer** για να γεφυρώσει το χάσμα μεταξύ του Vision Transformer και του Μεγάλου Γλωσσικού Μοντέλου (LLM). Αποτελεί ένα από τα πιο προηγμένα μοντέλα όρασης-γλώσσας που χρησιμοποιούνται σε αυτή την έρευνα.

## Κύρια Καινοτομία

Η βασική καινοτομία του BLIP-2 είναι ο **Query Transformer (Q-Former)**, ο οποίος:

- Εξάγει οπτικά χαρακτηριστικά από ένα pretrained vision encoder
- Λειτουργεί ως μεσάζων μεταξύ encoder και LLM
- Μειώνει το υπολογιστικό κόστος σύγκριση με πλήρη fine-tuning

## Πειραματική Ρύθμιση

Στην εργασία χρησιμοποιείται το BLIP-2 με:

- **Vision Encoder**: Vision Transformer
- **Γλωσσικό Μοντέλο**: OPT-2.7B
- **Μέγιστο μήκος ακολουθίας**: 512 tokens

## Απόδοση στις Λεπτομερείς Εικόνες

| Dataset | Μήκος (Αρχικό) | Μήκος (Verbose) | Αύξηση |
|---------|-----------------|------------------|--------|
| MS-COCO | 8.82 | 226.72 | 25.70× |
| ImageNet | 8.11 | 250.72 | 30.91× |

## Σχετικές Σελίδες

- [[blip]]
- [[instructblip]]
- [[minigpt-4]]
- [[vision-language-models]]
- [[verbose-images]]