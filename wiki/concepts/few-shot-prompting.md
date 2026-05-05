---
type: concept
title: "Az Örnekli Öğrenme (Few-shot Prompting)"
tags: ["Büyük Dil Modelleri", "İpromptlama", "Makine Öğrenmesi"]
related: ["chain-of-thought", "parcali-ipromptlama"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Az Örnekli Öğrenme (Few-shot Prompting)

## Genel Bakış

Few-shot prompting, Büyük Dil Modelleri'ne (LLM) yalnızca birkaç örnek ile görevleri öğretme yöntemidir. 2020 yılında Brown ve arkadaşları tarafından GPT-3 ile popüler hale getirilmiştir.

## Temel Kavramlar

### In-context Learning
Model, prompt içinde verilen örneklerden örüntüleri çıkararak yeni girdiler için sonuç üretir. Model ağırlıkları değiştirilmez.

### Zero-shot, One-shot, Few-shot
- **Zero-shot**: Hiç örnek verilmez
- **One-shot**: Bir örnek verilir
- **Few-shot**: Birkaç (genellikle 2-10) örnek verilir

## DECOMP ile İlişkisi

DECOMP, few-shot prompting'in karmaşık görevlerdeki zayıflıklarını gidermek için tasarlanmıştır:
- **Alt görev işleyiciler** daha zengin ve geniş örnekler gösterilmesine olanak tanır
- Her alt görev kendi özel prompt'u ile optimize edilebilir

## İlgili Sayfalar

- [[chain-of-thought]] - Düşünce zinciri
- [[parcali-ipromptlama]] - Parçalı İpromptlama