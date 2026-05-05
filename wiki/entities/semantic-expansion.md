---
type: entity
title: "Semantic Expansion -menetelmä"
tags: ["semantiikka", "jailbreak", "LLM-turvallisuus", "sanaston-laajennus"]
related: ["ice-jailbreak-menetelma", "hierarchical-split", "reasoning-mask", "distilbert", "wordnet", "jailbreak-hyökkäykset"]
sources: ["Cui 等 - 2025 - Exploring Jailbreak Attacks on LLMs through Intent Concealment and Diversion.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Semantic Expansion -menetelmä

## Yleiskatsaus

**Semantic Expansion** on ICE-menetelmän toinen vaihe, jossa alkuperäistä kehotetta laajennetaan semanttisella tiedolla. Menetelmä käyttää useita tekniikoita lisätäkseen hyökkäysvektorin tehoa ja laajentaakseen avainsanojen kattavuutta.

## Menetelmän vaiheet

### Vaihe 1: Verbi- ja substantiivijoukon rakentaminen
- **Verbijoukko V**: Sisältää kaikki verbit syötteestä S
- **Substantiivijoukko N**: Sisältää substantiivifraasit ja yksittäiset substantiivit

### Vaihe 2: Sentimenttianalyysi
Käytetään DistilBERT-mallia (esikoulutettu sentimenttianalyysiin) ennustamaan syötteen S sentimenttiluokka e_S:
```
e_S = DistilBERT(S)
```

### Vaihe 3: Synonyymien haku
- Valitaan satunnaisesti verbi v ∈ V
- Haetaan WordNetistä semanttisesti samankaltaisia sanoja (synonyymejä)
- Valitaan yksi liittyvä sana r_v

### Vaihe 4: Määritelmien analyysi
- Valitaan satunnaisesti substantiivi n ∈ N
- Haetaan WordNetistä substantiivin määritelmä
- Valitaan edustava substantiivifraasi t_n

### Vaihe 5: Toksiivisuusanalyysi
Käytetään LLM:ää tunnistamaan myrkyllisin sana ja generoimaan kuvailusanoja:
```
O, d = LLM(V ∪ N)
```
- O: Joukon sisältävä kaksi sanaa, jotka kuvaavat myrkyllisimmän sanan koostumusta
- d: Yksittäinen sana, joka kuvaa sen toksisuutta

## Lähtömuoto

Semanttisen laajennuksen tulos on joukko:
```
E = {e_S} ∪ {r_v} ∪ {t_n} ∪ O ∪ {d}
```

## Tarkoitus

Semantic Expansion mahdollistaa:
- Alkuperäisen kehotteen semanttisen laajentamisen
- Hyökkäysvektorin vahvistamisen lisäämällä kontekstisidonnaisia termejä
- Vastauksen rakeisuuden parantamisen monipuolisemmalla sanastolla

## Käytetyt työkalut

- **DistilBERT**: Kevyt BERT-malli sentimenttianalyysiin
- **WordNet**: Lexikaalinen tietokanta semanttisten suhteiden analysointiin
- **LLM**: Suuri kielimalli myrkyllisyyden tunnistamiseen

## Aiheeseen liittyvät sivut

- [[ice-jailbreak-menetelma]]
- [[hierarchical-split]]
- [[reasoning-mask]]
- [[distilbert]]
- [[wordnet]]
- [[jailbreak-hyökkäykset]]
- [[bisceneeval-tietokanta]]
- [[toxigen]]
- [[hatexplain]]