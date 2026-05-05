---
type: concept
title: "En Azdan En Çoğa İpromptlama (Least-to-Most Prompting)"
tags: ["İpromptlama", "Çok Adımlı Akıl Yürütme", "Büyük Dil Modelleri"]
related: ["parcali-ipromptlama", "chain-of-thought"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# En Azdan En Çoğa İpromptlama (Least-to-Most Prompting)

## Genel Bakış

Least-to-most prompting, karmaşık soruları daha basit alt sorulara ayırarak çözen bir prompting tekniğidir. Zhou ve arkadaşları tarafından 2023 yılında önerilmiştir.

## Parçalı İpromptlama ile Farklılıkları

| Özellik | Least-to-Most | Parçalı İpromptlama |
|---------|---------------|---------------------|
| Ayrıştırma Yapısı | Doğrusal | Doğrusal olmayan |
| Soru Üretimi | Tek seferde | Yinelemeli |
| Alt Görev Ataması | Sabit | Özelleştirilebilir |

DECOMP, least-to-most prompting'den farklı olarak:
- Doğrusal olmayan ayrıştırma yapılarına izin verir
- Alt görevlere farklı prompt'lar veya sembolik sistemler atayabilir
- Yinelemeli olarak yeni sorular üretir

## İlgili Sayfalar

- [[parcali-ipromptlama]] - Parçalı İpromptlama
- [[chain-of-thought]] - Düşünce zinciri