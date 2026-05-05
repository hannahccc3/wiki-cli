---
type: source
title: "Parçalı İpromptlama: Karmaşık Görevleri Çözmek İçin Modüler Bir Yaklaşım"
authors: ["Tushar Khot", "Harsh Trivedi", "Matthew Finlayson", "Yao Fu", "Kyle Richardson", "Peter Clark", "Ashish Sabharwal"]
year: 2023
url: ""
venue: "arXiv"
tags: ["Büyük Dil Modelleri", "İpromptlama", "Chain-of-Thought", "Görev Ayrıştırma", "Modüler Sistemler", "Çok Adımlı Akıl Yürütme"]
related: ["chain-of-thought", "few-shot-prompting", "least-to-most-prompting", "parcali-ipromptlama"]
sources: ["Khot 等 - 2023 - Decomposed Prompting A Modular Approach for Solving Complex Tasks.md"]
created: 2024-01-15
updated: 2024-01-15
---
# Parçalı İpromptlama: Karmaşık Görevleri Çözmek İçin Modüler Bir Yaklaşım

## Genel Bakış

Bu çalışma, **Parçalı İpromptlama (Decomposed Prompting - DECOMP)** yöntemini sunmaktadır. Yöntem, karmaşık görevleri daha basit alt görevlere ayırarak çözen yeni bir yaklaşımdır. Büyük Dil Modelleri'nin (LLM) few-shot prompting ile öğrenme sınırlamalarını aşmak için tasarlanmıştır.

## Temel Özellikler

### Modüler Yapı
DECOMP, her alt göreve özgü prompt'ların optimize edilmesine, alt görevlerin daha da ayrıştırılmasına ve sembolik sistemlerle entegrasyona olanak tanıyan modüler bir yapı kullanmaktadır.

### Ayrıştırıcı ve Alt Görev İşleyiciler
- **Ayrıştırıcı (Decomposer)**: Karmaşık görev için üst düzey programı tanımlar ve alt görevleri ilgili işleyicilere delege eder
- **Alt Görev İşleyiciler (Sub-task Handlers)**: Bağımsız optimize edilebilen, değiştirilebilen ve paylaşılabilen modüler bileşenlerdir

### Üç Temel Ayrıştırma Stratejisi

1. **Hiyerarşik Ayrıştırma**: Alt görevlerin daha da basit alt görevlere ayrıştırılması
2. **Özyinelemeli Ayrıştırma**: Girdi boyutu arttığında görevin aynı görevle ancak daha küçük girdilerle özyinelemeli olarak ayrıştırılması
3. **Dış API Entegrasyonu**: Alt görevleri çözmek için Elasticsearch gibi sembolik sistemlerin entegre edilmesi

## Deneysel Sonuçlar

DECOMP, çeşitli görevlerde Chain-of-Thought prompting'i düzenli olarak geride bırakmıştır:

| Görev | Karşılaştırma | Sonuç |
|-------|--------------|-------|
| Sembolik manipülasyon | CoT karşılaştırması | Üstün performans |
| Uzun bağlamlı QA | CoT karşılaştırması | %15-20 iyileşme |
| Açık domain çok adımlı QA | CoT karşılaştırması | Önemli iyileşmeler |

## İlgili Sayfalar

- [[parcali-ipromptlama]] - Ana kavram sayfası
- [[chain-of-thought]] - Akıl yürütme zinciri
- [[few-shot-prompting]] - Az örnekli öğrenme
- [[tushar-khot]] - Yazarlar
- [[allen-institute-for-ai]] - Kurum