---
type: concept
title: "Düşünce Zinciri (Chain-of-Thought)"
tags: ["Büyük Dil Modelleri", "İpromptlama", "Akıl Yürütme", "Çok Adımlı Çıkarım"]
related: ["parcali-ipromptlama", "few-shot-prompting", "least-to-most-prompting"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Düşünce Zinciri (Chain-of-Thought)

## Genel Bakış

Düşünce Zinciri (CoT) prompting, Büyük Dil Modelleri'nin karmaşık akıl yürütme görevlerini çözmesini sağan bir tekniktir. Ara akıl yürütme adımlarını göstererek modelin problem çözme kapasitesini artırır.

## Temel Özellikler

### Çalışma Prensibi
CoT prompting, örneklerde yalnızca girdi-sonuç çiftleri vermek yerine, aradaki düşünce adımlarını da gösterir. Bu, modelin problemi nasıl çözdüğünü anlamasına yardımcı olur.

### Örnek
```
Soru: Üç arabanın her birinde 4 tekerlek var. Toplam kaç tekerlek var?
Düşünce: Her arabanın 4 tekeri var. 3 araba var. 3 × 4 = 12
Cevap: 12
```

## DECOMP ile İlişkisi

DECOMP, CoT'nin sınırlamalarını aşmak için tasarlanmıştır:
- CoT, karmaşık görevlerde yeterli demonstrasyon sağlamakta zorlanabilir
- DECOMP, görevi alt görevlere bölerek her birinin ayrı prompt'larla öğretilmesini sağlar

## Sınırlamalar

1. **Karmaşıklık Artışı**: Görev karmaşıklaştıkça, tüm akıl yürütme adımlarını tek bir prompt'ta göstermek zorlaşır
2. **Uzunluk Genelleştirmesi**: Eğitim örneklerinden daha uzun girdilere genelleme yapmakta zorlanabilir
3. **Alt Görev Zorluğu**: Bazı ara adımların kendisi, few-shot prompting ile öğrenmesi zor olabilir

## İlgili Sayfalar

- [[parcali-ipromptlama]] - Parçalı İpromptlama
- [[few-shot-prompting]] - Az örnekli öğrenme
- [[least-to-most-prompting]] - En azdan en çoğa prompting