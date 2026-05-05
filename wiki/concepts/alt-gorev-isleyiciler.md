---
type: concept
title: "Alt Görev İşleyiciler (Sub-task Handlers)"
tags: ["Modüler Sistemler", "Büyük Dil Modelleri", "İpromptlama"]
related: ["parcali-ipromptlama", "hierarsik-ayristirma", "dis-api-cagrilari"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Alt Görev İşleyiciler (Sub-task Handlers)

## Genel Bakış

Alt görev işleyiciler, Parçalı İpromptlama'nın modüler yapısının temel bileşenleridir. Her biri belirli bir alt görev türünü çözmek için özelleştirilmiş prompt'lar veya sistemler içerir.

## İşleyici Türleri

### 1. Prompt Tabanlı İşleyiciler
LLM tabanlı standart prompting kullanır. Her alt görev için ayrı few-shot prompt'lar içerir.

### 2. Ayrıştırılmış İşleyiciler
Kendi içlerinde daha fazla alt göreve ayrıştırılabilen işleyicilerdir.

### 3. Sembolik İşleyiciler
LLM yerine sembolik sistemler (hesaplayıcı, arama motoru vb.) kullanan işleyicilerdir.

## Yazılım Mühendisliği Analojisi

Alt görev işleyiciler, yazılım kütüphanelerindeki fonksiyonlar gibi tasarlanmıştır:
- **Modüler**: Bağımsız olarak test edilebilir
- **Hata Ayıklanabilir**: Sorunlar izole edilebilir
- **Yükseltilebilir**: Daha iyi implementasyonlarla değiştirilebilir
- **Paylaşılabilir**: Farklı görevler arasında yeniden kullanılabilir

## İlgili Sayfalar

- [[parcali-ipromptlama]] - Parçalı İpromptlama
- [[hierarsik-ayristirma]] - Hiyerarşik ayrıştırma
- [[dis-api-cagrilari]] - Dış API çağrıları