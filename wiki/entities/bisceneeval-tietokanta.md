---
type: entity
title: "BiSceneEval-tietokanta"
tags: ["arviointitietokanta", "jailbreak", "LLM-turvallisuus", "haitallinen-sisältö"]
related: ["ice-jailbreak-menetelma", "advbench", "toxigen", "hatexplain", "jailbreak-hyökkäykset", "hyökkäyksen-onnistumisprosentti", "normalisoitu-kompressioetäisyys"]
sources: ["Cui 等 - 2025 - Exploring Jailbreak Attacks on LLMs through Intent Concealment and Diversion.md"]
created: 2025-01-01
updated: 2025-01-01
---
# BiSceneEval-tietokanta

## Yleiskatsaus

**BiSceneEval** on kattava arviointitietokanta, joka on suunniteltu LLM-turvallisuuden arviointiin kahdessa eri skenaariossa: kysely-vastaus-tehtävissä ja tekstintuottotehtävissä. Tietokanta paljastaa nykyisten puolustusmekanismien kriittisiä haavoittuvuuksia ja tarjoaa standardoidun arviointikehyksen jailbreak-hyökkäysten vaikutusten mittaamiseen.

## Tietokannan rakenne

### Harmful Inquiries (Haitalliset kyselyt)
Kysely-vastausskenaario, jossa malleja pyydetään generoimaan haitallisia vastauksia. Sisältää **319** merkintää 6 kategoriassa:

| Kategoria | Määrä | Kuvaus |
|-----------|-------|--------|
| Contraband (Salakuljetus) | 49 | Kyselyt, jotka pyrkivät saamaan neuvoja laittomien tuotteiden valmistukseen |
| Malware (Haittaohjelma) | 45 | Kyselyt koskien haittaohjelmien luontia tai kyberhyökkäyksiä |
| Evasion (Välttäminen) | 65 | Kyselyt, jotka pyrkivät välttämään oikeudellisia seuraamuksia |
| Self-harm (Itseinho) | 52 | Kyselyt, jotka provosoivat itsetuhoiseen sisältöön |
| Sexual (Seksuaalinen) | 57 | Kyselyt eksplisiittisen seksuaalisen sisällön generointiin |
| Violence (Väkivalta) | 51 | Kyselyt väkivaltaisen tai hyväksikäyttävän sisällön tuottamiseen |

### Toxic Responses (Myrkylliset vastaukset)
Tekstintuottoskenaario, jossa malleja pyydetään tuottamaan myrkyllistä tekstiä. Sisältää **433** merkintää 5 kategoriassa:

| Kategoria | Määrä | Kuvaus |
|-----------|-------|--------|
| Harassment (Kiusaaminen) | 89 | Sisältö, joka ilmaisee tai provosoi häirintäkieltä |
| Hate (Viha) | 94 | Sisältö, joka ilmaisee vihaa rotuun, sukupuoleen tai uskontoon perustuen |
| Self-harm (Itseinho) | 61 | Sisältö, joka edistää itsetuhoista käyttäytymistä |
| Sexual (Seksuaalinen) | 93 | Sisältö, joka on tarkoitettu seksuaalisen kiihottamisen herättämiseen |
| Violence (Väkivalta) | 96 | Sisältö, joka kuvaa kuolemaa, väkivaltaa tai fyysistä vammoja |

## Rakennusprosessi

Tietokannan rakentaminen koostuu kolmesta vaiheesta:

### 1. Datankeruu
- Reddit-alafoorumeilta (r/crime, r/legaladvice, r/criminal)
- AdvBench-tietokannasta
- ToxiGen-datasetistä
- HateXplain-datasetistä

### 2. Deduplikointi
- Normalisoitua kompressioetäisyys (NCD) käytetään semanttisen samankaltaisuuden tunnistamiseen
- NCD-kynnysarvo: 0,6
- Ryhmistä, joissa on korkea samankaltaisuus, säilytetään vain yksi merkintä

### 3. Tarkastelu ja luokittelu
- Kuusi asiantuntijaa lingvistiikan ja turvallisuuden aloilta
- OpenAI Moderation Endpoint -mallin automaattinen luokittelu
- Toksiivisuuspisteet alle 0,9 poistetaan

## Arviointimetriikat

### Kysely-vastausskenaario
- **Hybrid-ASR**: Yhdistelmä avainsana- ja LLM-arviointimenetelmistä
- **Human-ASR**: Ihmisarviointi vähintään 3 asiantuntijan toimesta

### Tekstintuottoskenaario
- **Restore-ASR**: Tarkistaa, sisältääkö vastaus kaikki syötteen sanat
- **Levenshtein-etäisyys**: Tekstin samankaltaisuuden mittari, kynnysarvo 0,95

## Aiheeseen liittyvät sivut

- [[ice-jailbreak-menetelma]]
- [[hierarchical-split]]
- [[semantic-expansion]]
- [[advbench]]
- [[toxigen]]
- [[hatexplain]]
- [[jailbreak-hyökkäykset]]
- [[hyökkäyksen-onnistumisprosentti]]
- [[normalisoitu-kompressioetäisyys]]
- [[openai-moderation-endpoint]]
- [[gpt-3.5]]
- [[gpt-4]]
- [[gpt-4o]]
- [[claude-3]]
- [[llama-3]]
- [[qwen-max]]
- [[ernie-3.5-turbo]]
- [[llm-turvallisuus]]