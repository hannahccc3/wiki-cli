---
type: source
title: "Friend or Foe: How LLMs' Safety Mind Gets Fooled by Intent Shift Attack"
authors: ["Peng Ding", "Jun Kuang", "Wen Sun", "Zongyu Wang", "Xuezhi Cao", "Xunliang Cai", "Jiajun Chen", "Shujian Huang"]
year: 2025
url: "https://github.com/NJUNLP/ISA"
venue: preprint
tags: ["LLM bezpečnost", "jailbreak útoky", "intent inference", "adversarial attacks", "bezpečnostní alignment"]
related: ["intent-shift-attack", "person-shift", "tense-shift", "voice-shift", "mood-shift", "question-shift", "jailbreak-utoky", "advbench", "maliciousinstruct", "gcg", "autodan", "pair", "renellm", "deepinception", "self-reminder", "ia-intent-analysis", "sage", "smoothllm"]
sources: ["Ding 等 - 2025 - Friend or Foe How LLMs' Safety Mind Gets Fooled by Intent Shift Attack.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Friend or Foe: How LLMs' Safety Mind Gets Fooled by Intent Shift Attack

## Přehled

Tento článek představuje **ISA (Intent Shift Attack)**, novou metodu jailbreak útoku, která využívá minimální jazykové úpravy k transformaci škodlivých dotazů na zdánlivě neškodné požadavky. Výzkum ukazuje, že ISA dosahuje více než 70% zlepšení úspěšnosti útoku oproti přímým škodlivým promptům napříč různými LLM modely.

## Autoři

- [[peng-ding]]
- [[jun-kuang]]
- [[wen-sun]]
- [[zongyu-wang]]
- [[xuezhi-cao]]
- [[xunliang-cai]]
- [[jiajun-chen]]
- [[shujian-huang]]

## Instituce

- [[nanjing-university]]
- [[national-key-laboratory-for-novel-software-technology]]
- [[meituan-inc]]

## Hlavní přínosy

1. **Nový přístup k jailbreak útokům**: ISA legitimizuje škodlivý záměr původního požadavku prostřednictvím minimálních jazykových úprav
2. **Vysoká úspěšnost**: ISA dosahuje více než 70% zlepšení úspěšnosti útoku oproti přímým škodlivým promptům
3. **Kritické zjištění**: Jemné ladění modelů pouze na neškodná data reformulovaná pomocí ISA šablon zvyšuje úspěšnost útoků na téměř **100 %**
4. **Evaluace obran**: Stávající obranné mechanismy jsou nedostatečné proti ISA

## Taxonomie transformací ISA

ISA využívá pět typů jazykových transformací:

- [[person-shift]] — Změna první osoby na třetí osobu
- [[tense-shift]] — Změna času z přítomného/budoucího na minulý
- [[voice-shift]] — Změna aktivního hlasu na pasivní
- [[mood-shift]] — Použití podmiňovacího nebo konjunktivního způsobu
- [[question-shift]] — Změna otázek „jak na to" na otázky „proč/co"

## Experimentální výsledky

### Úspěšnost útoku (ASR) na různých modelech

| Model | Vanilla | ISA (nejlepší) | ASR Gain |
|-------|---------|----------------|----------|
| Qwen-2.5 | 2% | 86% | 84% |
| Llama-3.1 | 0% | 74% | 74% |
| GPT-4.1 | 0% | 72% | 72% |
| Claude-4-Sonnet | 0% | 70% | 70% |
| DeepSeek-R1 | 4% | 82% | 78% |

### Nejúčinnější transformace

Nejúčinnějšími typy transformací jsou **Mood Shift** a **Question Shift**, které dosahují nejvyšších hodnot ASR napříč modely.

## Obranné mechanismy

### Vyhodnocené obrany

- **Paraphrase** (mutace založená na parafrázi)
- **IA (Intent Analysis)** — detekce založená na analýze záměru
- **Self-Reminder** — systémové bezpečnostní prompty
- **SAGE** — paradigmus „posouzení před generováním"

### Zjištění

Žádný jednotlivý obranný mechanismus neposkytuje konzistentní ochranu proti ISA útokům napříč různými architekturami modelů.

## Etické aspekty

Tento výzkum má za cíl posílit bezpečnost LLM odhalením zranitelností v inferenci záměru. Autoři zdůrazňují, že zjištění by měla být využita ke zlepšení bezpečnostních mechanismů, nikoli k maliciousnímu zneužití.

## Související stránky

- [[intent-shift-attack]]
- [[jailbreak-utoky]]
- [[bezpecnostni-alignment]]
- [[attack-success-rate]]
- [[fine-tuning]]