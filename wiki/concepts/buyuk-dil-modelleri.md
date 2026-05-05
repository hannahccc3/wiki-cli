---
type: concept
title: "Büyük Dil Modelleri (Large Language Models)"
tags: ["Yapay Zeka", "Derin Öğrenme", "Doğal Dil İşleme"]
related: ["parcali-ipromptlama", "few-shot-prompting", "chain-of-thought"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Büyük Dil Modelleri (Large Language Models)

## Genel Bakış

Büyük Dil Modelleri (LLM), büyük metin verileri üzerinde eğitilmiş ve çeşitli dil görevlerini gerçekleştirebilen derin öğrenme modelleridir.

## Temel Özellikler

### In-context Learning
LLM'ler, prompt içinde verilen örneklerden örüntüleri çıkararak yeni görevleri öğrenebilir.

### Çoklu Görev Yeteneği
Tek bir model, çeviri, özetleme, soru cevaplama gibi birçok farklı görevi gerçekleştirebilir.

## DECOMP Kullanılan Modeller

Çalışmada çeşitli LLM'ler kullanılmıştır:
- GPT-3 (text-davinci-002)
- Codex (code-davinci-002)
- Flan-T5 ailesi

## İlgili Sayfalar

- [[parcali-ipromptlama]] - Parçalı İpromptlama
- [[few-shot-prompting]] - Az örnekli öğrenme
- [[chain-of-thought]] - Düşünce zinciri