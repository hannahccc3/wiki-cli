---
type: source
title: "ICE: Aikomuksen piilotusta ja hajautusta hyödyntävä jailbreak-menetelmä suurille kielimalleille"
authors: ["Tiehan Cui", "Yanxu Mao", "Peipei Liu", "Congying Liu", "Datao You"]
year: 2025
url: ""
venue: ""
tags: ["jailbreak", "LLM-turvallisuus", "tekoälyn turvallisuus", "hyökkäyksen onnistumisprosentti", "kognitiivinen ylikuormitus", "aikomuksen piilotus", "semanttinen laajennus"]
related: ["ice-jailbreak-menetelma", "bisceneeval-tietokanta", "hierarchical-split", "semantic-expansion", "reasoning-mask", "advbench", "gpt-3.5", "gpt-4", "claude-3", "llama-2", "llama-3", "qwen-max", "ernie-3.5-turbo", "distilbert", "wordnet", "openai-moderation-endpoint", "toxigen", "hatexplain", "jailbreak-hyökkäykset", "hyökkäyksen-onnistumisprosentti", "musta-laatikko-hyökkäys", "kognitiivinen-ylikuormitus", "normalisoitu-kompressioetäisyys"]
sources: ["Cui 等 - 2025 - Exploring Jailbreak Attacks on LLMs through Intent Concealment and Diversion.md"]
created: 2025-01-01
updated: 2025-01-01
---
# ICE: Aikomuksen piilotusta ja hajautusta hyödyntävä jailbreak-menetelmä suurille kielimalleille

## Yleiskatsaus

Tutkimus esittelee **ICE-menetelmän** (Intent Concealment and divErsion), joka on tehokas ja yleistettävä jailbreak-menetelmä suurille kielimalleille (LLM). ICE saavuttaa yli 70 % hyökkäyksen onnistumisprosentnin (ASR) käyttämällä aikomuksen piilotusta ja semanttista hajautusta yhden kyselyn avulla.

## Pääasialliset kontribuutiot

### 1. ICE-jailbreak-kehys
ICE on parametriton yleinen jailbreak-menetelmä, joka koostuu neljästä osatekijästä:
- **Hierarchical Split**: Jakaa haitalliset kyselyt hierarkkisiin osiin
- **Semantic Expansion**: Laajentaa sanastoa lisäämällä semanttista tietoa
- **Reasoning Mask**: Yhdistää hierarkkiset fragmentit ja paikkamerkit
- **Environmental Construction**: Upottaa muokatun kehotteen päättelykehykseen

### 2. BiSceneEval-tietokanta
Tutkimuksessa esitellään myös **BiSceneEval-tietokanta**, joka mahdollistaa kattavan arvioinnin sekä kysely-vastaus- että tekstintuottotilanteissa. Tietokanta koostuu:
- **Harmful Inquiries**: Haitallisia kyselyitä 6 kategoriassa (319 kpl)
- **Toxic Responses**: Myrkyllisiä vastauksia 5 kategoriassa (433 kpl)

## Keskeiset tulokset

- ICE saavuttaa **99,2 % KW-ASR:n** GPT-3.5-mallilla AdvBench-tietokannassa
- Keskimääräinen ASR ylittää **70 %** yhdellä kyselyllä
- Aikaa kuluu vain **8,71 sekuntia** näytettä kohden (15,16 kertaa nopeampi kuin ReNeLLM)
- Menetelmä osoittaa ylivoimaista siirrettävyyttä eri mallien välillä

## Kokeelliset tulokset eri malleilla

| Malli | KW-ASR (%) | GPT-ASR (%) |
|-------|------------|-------------|
| GPT-3.5 | 99,2 | 98,3 |
| GPT-4 | 99,8 | 72,6 |
| Claude-1 | 96,9 | 97,9 |
| Claude-2 | 67,3 | 83,2 |
| LLaMA2 | 88,9 | 63,0 |

## Puolustusstrategiat

Tutkimus ehdottaa **kaksivaiheista puolustusstrategiaa**:
1. **Staattiset turvallisuusmekanismit**: Ennakkoon määritetyt turvallisuussäännöt
2. **Dynaaminen semanttinen hajotus**: Reaaliaikainen analyysi ja kehotteen hajotus

## Lähteet

Tämä lähdesivu perustuu alkuperäiseen tutkimusartikkeliin: *Exploring Jailbreak Attacks on LLMs through Intent Concealment and Diversion* (2025), jonka kirjoittajat ovat Tiehan Cui, Yanxu Mao, Peipei Liu, Congying Liu ja Datao You.

## Aiheeseen liittyvät sivut

- [[ice-jailbreak-menetelma]]
- [[bisceneeval-tietokanta]]
- [[hierarchical-split]]
- [[semantic-expansion]]
- [[reasoning-mask]]
- [[advbench]]
- [[gpt-3.5]]
- [[gpt-4]]
- [[claude-3]]
- [[llama-2]]
- [[llama-3]]
- [[qwen-max]]
- [[ernie-3.5-turbo]]
- [[jailbreak-hyökkäykset]]
- [[hyökkäyksen-onnistumisprosentti]]
- [[musta-laatikko-hyökkäys]]
- [[kognitiivinen-ylikuormitus]]
- [[normalisoitu-kompressioetäisyys]]
- [[jailbreakbench]]
- [[pair]]
- [[autodan]]
- [[gcg]]
- [[renellm]]
- [[textfooler]]
- [[pwws]]
- [[bert-attack]]
- [[smoothllm]]
- [[erase-and-check]]
- [[tap]]
- [[rlhf]]
- [[llm-turvallisuus]]
- [[deep-document-model]]
- [[adv-ner]]
- [[askg]]
- [[paper2lkg]]
- [[pass]]
- [[perplexity-filter]]
- [[semempsO]]
- [[rl-jack]]
- [[rocket]]
- [[deepwordbug]]
- [[jbb-behaviors]]
- [[unaligned-llm]]
- [[helper-llm]]
- [[target-llm]]
- [[frontier-models]]
- [[adaptive-attacks]]
- [[adversarial-suffix]]
- [[bit-flip-attack]]
- [[cautionary-warning-defense]]
- [[competing-objectives-attack]]
- [[composition-attack]]
- [[decomposition-attacks]]
- [[few-shot-jailbreaking]]
- [[in-context-defense]]
- [[in-context-learning]]
- [[context-window]]