---
type: concept
title: "Parçalı İpromptlama (Decomposed Prompting)"
tags: ["Büyük Dil Modelleri", "İpromptlama", "Modüler Sistemler", "Görev Ayrıştırma"]
related: ["chain-of-thought", "few-shot-prompting", "least-to-most-prompting", "alt-gorev-isleyiciler"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Parçalı İpromptlama (Decomposed Prompting)

## Genel Bakış

Parçalı İpromptlama (DECOMP), karmaşık görevleri daha basit alt görevlere ayırarak çözen bir yaklaşımdır. 2023 yılında Khot ve arkadaşları tarafından geliştirilmiştir. Büyük Dil Modelleri'nin (LLM) karmaşık görevleri few-shot prompting ile çözmedeki sınırlamalarını aşmak için tasarlanmıştır.

## Temel Kavramlar

### Ayrıştırıcı (Decomposer)
Karmaşık bir sorguyu alır ve bunu bir dizi alt göreve böler. Her alt görev, uygun alt görev işleyicisine yönlendirilir.

### Alt Görev İşleyiciler
Her alt görev türü için özelleştirilmiş prompt'lar içeren modüler bileşenlerdir. Bunlar:
- Standart prompting tabanlı LLM'ler
- Daha fazla ayrıştırılmış alt görev prompt'ları
- Sembolik fonksiyonlar (örneğin, hesaplayıcı veya bilgi erişim sistemleri)

## Ayrıştırma Stratejileri

### 1. Hiyerarşik Ayrıştırma
Alt görevlerin daha da basit alt görevlere bölünmesini sağlar. Örneğin, "bir kelimenin k. harfini bulma" görevi, "harflere ayırma" ve "k. elemanı seçme" alt görevlerine ayrıştırılabilir.

### 2. Özyinelemeli Ayrıştırma
Girdi boyutu arttığında, görev aynı türde ancak daha küçük girdilerle özyinelemeli olarak ayrıştırılır. Bu yaklaşım, uzun listelerin tersine çevrilmesi gibi görevlerde uzunluk genelleştirmesini sağlar.

### 3. Dış API Entegrasyonu
LLM'lerin zorlandığı görevler (örneğin, büyük bilgi tabanlarından bilgi çekme) için sembolik sistemler (Elasticsearch gibi) entegre edilebilir.

## Avantajları

- **Modülerlik**: Alt görev işleyiciler bağımsız olarak optimize edilebilir
- **Yeniden Kullanılabilirlik**: Alt görev işleyiciler farklı karmaşık görevler arasında paylaşılabilir
- **Hata Ayıklama Kolaylığı**: Her alt görev izole olarak test edilebilir
- **Esneklik**: Alt görev işleyiciler kolayca değiştirilebilir veya yükseltilebilir

## İlgili Sayfalar

- [[chain-of-thought]] - Düşünce zinciri
- [[few-shot-prompting]] - Az örnekli öğrenme
- [[least-to-most-prompting]] - En azdan en çoğa prompting
- [[alt-gorev-isleyiciler]] - Alt görev işleyiciler
- [[hierarsik-ayristirma]] - Hiyerarşik ayrıştırma
- [[ozyinelemeli-ayristirma]] - Özyinelemeli ayrıştırma