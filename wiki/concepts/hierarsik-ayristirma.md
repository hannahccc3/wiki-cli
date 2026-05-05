---
type: concept
title: "Hiyerarşik Ayrıştırma (Hierarchical Decomposition)"
tags: ["Görev Ayrıştırma", "Modüler Sistemler", "Büyük Dil Modelleri"]
related: ["parcali-ipromptlama", "ozyinelemeli-ayristirma", "alt-gorev-isleyiciler"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Hiyerarşik Ayrıştırma (Hierarchical Decomposition)

## Genel Bakış

Hiyerarşik ayrıştırma, karmaşık bir alt görevin daha da basit alt görevlere bölünmesini sağlayan bir stratejidir. Parçalı İpromptlama'nın temel bileşenlerinden biridir.

## Çalışma Mekanizması

Bazı alt görevler, kendilerine özel prompt'lar ile bile çözülemezler. Bu durumda, alt görev daha da küçük parçalara ayrıştırılır.

### Örnek
**Orijinal Alt Görev**: "Bir kelimenin k. harfini bulma"
**Ayrıştırılmış Alt Görevler**:
1. Kelimeyi harflere ayır
2. Dizinin k. elemanını seç

## Avantajları

- **Öğrenme Kolaylığı**: Küçük alt görevler, büyük görevlere göre daha kolay öğrenilir
- **Modülerlik**: Ayrıştırılmış parçalar yeniden kullanılabilir
- **Genelleştirme**: Model, küçük bileşenleri öğrendikten sonra yeni kombinasyonlara genelleştirebilir

## İlgili Sayfalar

- [[parcali-ipromptlama]] - Parçalı İpromptlama
- [[ozyinelemeli-ayristirma]] - Özyinelemeli ayrıştırma
- [[alt-gorev-isleyiciler]] - Alt görev işleyiciler