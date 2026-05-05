---
type: entity
title: "ICE-jailbreak-menetelmä"
tags: ["jailbreak", "LLM-turvallisuus", "hyökkäysmenetelmä", "musta-laatikko"]
related: ["hierarchical-split", "semantic-expansion", "reasoning-mask", "bisceneeval-tietokanta", "jailbreak-hyökkäykset", "kognitiivinen-ylikuormitus", "hyökkäyksen-onnistumisprosentti"]
sources: ["Cui 等 - 2025 - Exploring Jailbreak Attacks on LLMs through Intent Concealment and Diversion.md"]
created: 2025-01-01
updated: 2025-01-01
---
# ICE-jailbreak-menetelmä

## Yleiskatsaus

**ICE** (Intent Concealment and divErsion) on innovatiivinen mustan laatikon (black-box) jailbreak-menetelmä, joka on suunniteltu erityisesti instruktio-suunnattujen suurten kielimalleiden (LLM) kognitiivisen ylikuormituksen haavoittuvuuksien hyödyntämiseen. Menetelmä yhdistää aikomuksen piilotuksen ja semanttisen hajautuksen tehokkaaseen hyökkäykseen, joka toimii yhdellä kyselyllä.

## Menetelmän rakenne

ICE koostuu neljästä pääkomponentista:

### 1. Hierarchical Split (Hierarkkinen jakaminen)
Algoritmi, joka jakaa haitalliset kyselyt hierarkkisiin osiin riippuvuusanalyysin avulla. Tämä piilottaa hyökkäysaikeen päättelytehtäviin LLM:n turvatoimenpiteiden ohittamiseksi.

### 2. Semantic Expansion (Semanttinen laajennus)
Menetelmä, joka analysoi ja laajentaa haitallisten kyselyiden sanastoa. Käyttää sentimenttianalyysia, verbien ja substantiivien semanttista augmentaatiota sekä toksisuuteen perustuvaa sanantuottoa.

### 3. Reasoning Mask (Päättelymaski)
Tekniikka, joka yhdistää hierarkkiset fragmentit ja laajennetut termit. Strategisesti piilottaa haitallisen aikomuksen rakenteellisiin tehtäväkehotuksiin.

### 4. Environmental Construction (Ympäristön rakentaminen)
Upottaa muokatun kehotteen päättely- tai kysely-vastauskehykseen varmistaen tehokkaan jailbreak-käskyn muodostumisen.

## Suorituskyky

| Mittari | Arvo |
|---------|------|
| Keskimääräinen ASR | >70 % |
| KW-ASR (GPT-3.5) | 99,2 % |
| KW-ASR (GPT-4) | 99,8 % |
| TCPS (aika/näyte) | 8,71 s |
| Kyselykertojen määrä | 1 |

## Vertailu muihin menetelmiin

ICE ylittää merkittävästi aiemmat SOTA-menetelmät:

- **GCG**: 8,7 % KW-ASR → ICE: 99,2 %
- **AutoDAN**: 35,0 % → ICE: 99,2 %
- **PAIR**: 20,8 % → ICE: 99,2 %
- **ReNeLLM**: 87,9 % → ICE: 99,2 %

## Siirrettävyys

ICE osoittaa erinomaista siirrettävyyttä eri mallien välillä, koska se hyödyntää universaaleja kognitiivisen ylikuormituksen heikkouksia instruktio-suunnatuissa LLM:issä.

## Aiheeseen liittyvät sivut

- [[hierarchical-split]]
- [[semantic-expansion]]
- [[reasoning-mask]]
- [[bisceneeval-tietokanta]]
- [[jailbreak-hyökkäykset]]
- [[kognitiivinen-ylikuormitus]]
- [[hyökkäyksen-onnistumisprosentti]]
- [[musta-laatikko-hyökkäys]]
- [[advbench]]
- [[pair]]
- [[autodan]]
- [[gcg]]
- [[renellm]]
- [[gpt-3.5]]
- [[gpt-4]]
- [[claude-3]]
- [[llama-2]]
- [[llama-3]]
- [[qwen-max]]
- [[ernie-3.5-turbo]]
- [[distilbert]]
- [[wordnet]]
- [[openai-moderation-endpoint]]
- [[toxigen]]
- [[hatexplain]]
- [[jailbreakbench]]
- [[textfooler]]
- [[pwws]]
- [[bert-attack]]
- [[smoothllm]]
- [[erase-and-check]]
- [[tap]]
- [[rlhf]]
- [[llm-turvallisuus]]