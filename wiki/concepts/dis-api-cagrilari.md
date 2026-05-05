---
type: concept
title: "Dış API Çağrıları (External API Calls)"
tags: ["Entegrasyon", "Bilgi Erişim", "Büyük Dil Modelleri", "Sembolik Sistemler"]
related: ["parcali-ipromptlama", "alt-gorev-isleyiciler"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Dış API Çağrıları (External API Calls)

## Genel Bakış

Dış API çağrıları, Parçalı İpromptlama'da LLM'lerin zorlandığı alt görevleri çözmek için sembolik sistemlerin entegre edilmesini sağlayan bir özelliktir.

## Kullanım Alanları

### Bilgi Erişimi
Büyük bilgi tabanlarından veya Wikipedia'dan bilgi çekme görevleri için sembolik arama sistemleri (Elasticsearch gibi) kullanılabilir.

### Hesaplama
Matematiksel hesaplamalar için hesaplayıcı fonksiyonlar entegre edilebilir.

## Avantajları

- **Ölçeklenebilirlik**: Çok büyük veri kümelerinde arama yapılabilir
- **Doğruluk**: Sembolik sistemler, LLM'lerin hata yapabileceği hesaplamalarda daha güvenilirdir
- **Hibrit Yaklaşım**: LLM'lerin güçlü yönleri ile sembolik sistemlerin güçlü yönlerini birleştirir

## Örnek: Elasticsearch Entegrasyonu

```
Alt Görev: "Lost Gravity hangi şirket tarafından üretildi?"
↓
API Çağrısı: Elasticsearch'e sorgu
↓
Sonuç: "Mack Rides"
```

## İlgili Sayfalar

- [[parcali-ipromptlama]] - Parçalı İpromptlama
- [[alt-gorev-isleyiciler]] - Alt görev işleyiciler