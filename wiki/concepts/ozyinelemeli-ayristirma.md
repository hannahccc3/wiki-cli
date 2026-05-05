---
type: concept
title: "Özyinelemeli Ayrıştırma (Recursive Decomposition)"
tags: ["Görev Ayrıştırma", "Algoritmalar", "Büyük Dil Modelleri"]
related: ["parcali-ipromptlama", "hierarsik-ayristirma"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Özyinelemeli Ayrıştırma (Recursive Decomposition)

## Genel Bakış

Özyinelemeli ayrıştırma, bir problemin aynı türde ancak daha küçük girdilerle özyinelemeli olarak ayrıştırılmasını sağlayan bir stratejidir. Parçalı İpromptlama'nın uzunluk genelleştirmesi sağlayan bileşenidir.

## Çalışma Mekanizması

Bazı problemler doğal olarak daha küçük aynı formdaki problemlere bölünebilir. Bu yaklaşım, birleştirme sıralaması gibi özyinelemeli algoritmalardan ilham almaktadır.

### Örnek: Liste Tersine Çevirme
1. Listeyi ikiye böl
2. Her yarıyı tersine çevir (özyinelemeli olarak)
3. Yarıları ters sırada birleştir

Bu yaklaşım, modelin yalnızca 3 elemanlı listeleri doğru tersine çevirebilmesi durumunda bile, keyfi uzunluktaki listeleri tersine çevirmesini sağlar.

## Avantajları

- **Uzunluk Genelleştirmesi**: Eğitim örneklerinden çok daha uzun girdilere genelleme yapabilir
- **Ölçek Bağımsızlığı**: Girdi boyutundan bağımsız olarak çalışır
- **Temel Durum Kullanımı**: Modelin kesin olarak bildiği basit durumlara indirgeme

## İlgili Sayfalar

- [[parcali-ipromptlama]] - Parçalı İpromptlama
- [[hierarsik-ayristirma]] - Hiyerarşik ayrıştırma