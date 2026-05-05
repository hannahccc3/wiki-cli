---
type: source
title: "REINFORCE Αντίπαλοι Επιθέσεις σε Μεγάλα Γλωσσικά Μοντέλα: Ένα Προσαρμοστικό, Κατανομικό και Σημασιολογικό Στόχος"
authors: ["Simon Geisler", "Tom Wollschläger", "M. H. I. Abdalla", "Vincent Cohen-Addad", "Johannes Gasteiger", "Stephan Günnemann"]
year: 2025
url: ""
venue: ""
tags: ["adversarial attacks", "LLM security", "jailbreaking", "REINFORCE", "policy gradient", "alignment", "HarmBench", "GCG", "PGD", "machine learning safety"]
related: ["gcg", "reinforce", "jailbreaking", "harmbench", "circuit-breaker-defense", "llama-3-8b", "llama-2-7b", "gemma-1.1-2b", "gemma-1.1-7b", "vicuna-1.5-7b"]
sources: ["Geisler 等 - 2025 - REINFORCE Adversarial Attacks on Large Language Models An Adaptive, Distributional, and Semantic Ob.md"]
created: 2025-01-01
updated: 2025-01-01
---
# REINFORCE Αντίπαλοι Επιθέσεις σε Μεγάλα Γλωσσικά Μοντέλα: Ένα Προσαρμοστικό, Κατανομικό και Σημασιολογικό Στόχος

## Επισκόπηση

Αυτή η εργασία παρουσιάζει μια νέα προσέγγιση για επιθέσεις jailbreaking σε Μεγάλα Γλωσσικά Μοντέλα (LLMs), χρησιμοποιώντας τον αλγόριθμο REINFORCE ως μηχανισμόό βελτιστοποίησης. Η μέθοδος αντιμετωπίζει τις αδυναμίες του παραδοσιακού **affirmative response objective** που δεν είναι προσαρμοστικό ούτε συνεπές.

## Κύρια Συνεισφορά

Οι συγγραφείς προτείνουν ένα νέο αντικειμενικό στόχο που είναι:
- **Προσαρμοστικό**: Προσαρμόζεται στο μοντέλο-στόχο
- **Κατανομικό**: Βελτιστοποιεί την κατανομή πιθανοτήτων επιβλαβών αποκρίσεων
- **Σημασιολογικό**: Στοχεύει την επιβλαβή σημασιολογία αντί για προκαθορισμένες λέξεις

## Βασικά Ευρήματα

| Μοντέλο | Affirmative ASR@512 | REINFORCE ASR@512 |
|---------|---------------------|-------------------|
| Llama 3 8B | 0.35 | 0.73 |
| Gemma 1.1 7B | 0.63 | 0.87 |
| Llama 2 7B | 0.32 | 0.56 |

Το REINFORCE objective **διπλασιάζει** το ποσοστό επιτυχίας επίθεσης (ASR) σε σύγκριση με το affirmative objective.

## Circuit Breaker Defense

Έναντι της άμυνας Circuit Breaker:
- Affirmative objective: 2% ASR@512
- REINFORCE: 23% ASR@512
- REINFORCE με βελτιστοποιημένο seed: 50% ASR@512

## Σχετικές Σελίδες

- [[gcg]] - Greedy Coordinate Gradient
- [[reinforce]] - REINFORCE Algorithm
- [[jailbreaking]] - Jailbreaking Attacks
- [[harmbench]] - HarmBench Benchmark
- [[circuit-breaker-defense]] - Circuit Breaker Defense
- [[policy-gradient]] - Policy Gradient Methods
- [[rloo-estimator]] - RLOO Estimator