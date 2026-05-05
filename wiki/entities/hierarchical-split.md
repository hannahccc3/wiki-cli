---
type: entity
title: "Hierarchical Split -algoritmi"
tags: ["algoritmi", "jailbreak", "LLM-turvallisuus", "riippuvuusanalyysi"]
related: ["ice-jailbreak-menetelma", "semantic-expansion", "reasoning-mask", "jailbreak-hyökkäykset", "kognitiivinen-ylikuormitus"]
sources: ["Cui 等 - 2025 - Exploring Jailbreak Attacks on LLMs through Intent Concealment and Diversion.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Hierarchical Split -algoritmi

## Yleiskatsaus

**Hierarchical Split** on ICE-menetelmän ensimmäinen vaihe, jossa haitalliset kyselyt jaetaan hierarkkisiin fragmentteihin käyttäen riippuvuusanalyysiä. Algoritmi hyödyntää syntaktisia ja semanttisia piirteitä piilottaakseen hyökkäysaikeen päättelytehtäviin.

## Algoritmin kuvaus

### Vaihe 1: Riippuvuusgraafin rakentaminen
Annettuna alkuperäinen kehote S = {w₁, w₂, ..., wₙ}, jossa wᵢ on i:s sana lauseessa:
1. Rakennetaan riippuvuusgraafi G = (S, E)
2. E = {(wᵢ, wⱼ, r)} edustaa suunnattuja reunoja sanojen välillä
3. r kuvaa riippuvuussuhdetta

### Vaihe 2: Verbien tunnistaminen
Tunnistetaan ei-juurieverbit, joilla on sekä vanhempi- että lapsisolmut:
```
W_verbs = {wᵢ ∈ S | posᵢ = VERB, P_wᵢ ≠ ∅, C_wᵢ ≠ ∅}
```

### Vaihe 3: Riippuvuussuhteiden muokkaaminen
Valitusta verbijoukosta muokataan riippuvuussuhteita. Säilytetään vain tietyt suhteet:
- neg, fixed, compound, amod, advmod, nmod

### Vaihe 4: Hierarkiatason päivitys
- Verbin hierarkiataso l_j kasvatetaan yhdellä
- Muutos propagoituu rekursiivisesti lapsisolmuihin

### Vaihe 5: Katkaisupisteiden tunnistaminen
Katkaistaan joko oletusarvot (0 ja n) tai keskipisteet peräkkäisten eri tason sanojen välillä.

### Vaihe 6: Tason normalisointi
Käytetään järjestyskuvausta (Rank Mapping) tasojen normalisointiin:
```
lᵢ ← f(lᵢ), f: vanhat tasot → {1, 2, ..., m}
```

## Lähtömuoto

Hierarkkisen jakamisen tulos on lista:
```
L = {(wᵢ, lᵢ) | wᵢ ∈ S, lᵢ ∈ {1, 2, ..., m}}
```

## Tarkoitus

Hierarchical Split mahdollistaa:
- Haitallisen aikomuksen piilottamisen monitasoisiin päättelyfragmentteihin
- Turvafilttereiden ohittamisen hajauttamalla hyökkäys useaan osaan
- Päättelykyvyttömyyden hyödyntämisen LLM:ien monivaiheisessa päättelyssä

## Aiheeseen liittyvät sivut

- [[ice-jailbreak-menetelma]]
- [[semantic-expansion]]
- [[reasoning-mask]]
- [[jailbreak-hyökkäykset]]
- [[kognitiivinen-ylikuormitus]]
- [[normalisoitu-kompressioetäisyys]]
- [[bisceneeval-tietokanta]]