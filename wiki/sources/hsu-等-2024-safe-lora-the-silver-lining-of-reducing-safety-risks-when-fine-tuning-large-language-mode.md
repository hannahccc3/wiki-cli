---
type: source
title: "Safe LoRA: the Silver Lining of Reducing Safety Risks when Fine-tuning Large Language Models"
authors: ["Chia-Yi Hsu", "Yu-Lin Tsai", "Chih-Hsun Lin", "Pin-Yu Chen", "Chia-Mu Yu", "Chun-Ying Huang"]
year: 2024
url: "https://github.com/IBM/SafeLoRA"
venue: "arXiv preprint"
tags: ["large language models", "LLM safety", "fine-tuning", "LoRA", "parameter-efficient fine-tuning", "AI alignment", "safety guardrails", "adversarial attacks", "model security", "jailbreak prevention", "post-hoc projection"]
related: ["lora", "safety-alignment", "alignment-matrix", "projection-operator", "llama-2-7b-chat", "llama-3-8b-instruct", "safeinstr", "bea-backdoor-enhanced-alignment"]
sources: ["Hsu 等 - 2024 - Safe LoRA the Silver Lining of Reducing Safety Risks when Fine-tuning Large Language Models.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Safe LoRA: η Ασημένια Ευκαιρία για Μείωση Κινδύνων Ασφαλείας κατά το Fine-tuning Μεγάλων Γλωσσικών Μοντέλων

## Περίληψη

Η μέθοδος **Safe LoRA** είναι μια προσέγγιση που προβάλλει τα βάρη LoRA σε έναν χώρο ευθυγράμμισης ασφαλείας για να αποτρέψει την υποβάθμιση της ασφάλειας κατά το fine-tuning μεγάλων γλωσσικών μοντέλων (LLMs). Η μέθοδος αυτή δεν απαιτεί επιπλέον δεδομένα εκπαίδευσης ή εκπαιδευτική διαδικασία.

## Βασικά Ευρήματα

- Το fine-tuning LLMs με LoRA μπορεί να αποδυναμώσει σημαντικά τις δικλείδες ασφαλείας ακόμη και με καλοήθη δεδομένα
- Το Safe LoRA προβάλλει τα βάρη LoRA στον υποχώρο ευθυγράμμισης όταν οι βαθμοί ομοιότητας πέφτουν κάτω από ένα κατώφλι
- Το Llama-2 απαιτεί προβολή ~11% των επιπέδων, ενώ το Llama-3 απαιτεί ~35%
- Η προσέγγιση υπερτερεί των μεθόδων SafeInstr και BEA στην ισορροπία ασφάλειας και χρηστικότητας

## Σύνδεση με Άλλες Σελίδες

- [[lora]]
- [[safety-alignment]]
- [[alignment-matrix]]
- [[projection-operator]]
- [[llama-2-7b-chat]]
- [[llama-3-8b-instruct]]
- [[safeinstr]]
- [[bea-backdoor-enhanced-alignment]]
- [[purebad-dataset]]
- [[dialog-summary-dataset]]
- [[alpaca-dataset]]
- [[asr-attack-success-rate]]
- [[harmfulness-score]]
- [[parameter-efficient-fine-tuning]]