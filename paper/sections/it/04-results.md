# 4. Risultati

## 4.1 Panoramica dell'esperimento

L'esperimento BMAS completo comprendeva 45 prompt su tre strati di dominio, ognuno valutato da dodici modelli, producendo in totale 540 risposte di modelli. Tutte le risposte sono state ottenute sotto rigoroso isolamento cieco tramite il gateway OpenClaw.

**Tabella 1: Statistiche di risposta per dominio**

| Dominio | n prompt | Coseno medio | Dev. std. | Min | Max | BERTScore F1 medio | Jaccard medio |
|---|---|---|---|---|---|---|---|
| Tecnico (A) | 10 | 0,832 | 0,045 | 0,750 | 0,891 | 0,841 | 0,003 |
| Normativo (B) | 10 | 0,869 | 0,046 | 0,793 | 0,930 | 0,852 | 0,003 |
| Strategico (C) | 7 | 0,845 | 0,037 | 0,786 | 0,892 | 0,840 | 0,001 |

## 4.2 Convergenza per dominio

**Dominio A (Tecnico):** Su 10 prompt che richiedono conoscenze tecniche precise, i modelli hanno raggiunto una similarità coseno per coppie media di 0,832 (DS = 0,045). Il BERTScore F1 medio era 0,841, indicando una forte sovrapposizione semantica a livello di token. La similarità Jaccard sulle affermazioni estratte era in media 0,003, suggerendo che i modelli convergono non solo nella formulazione ma nelle specifiche affermazioni fattuali che fanno.

**Dominio B (Normativo):** I prompt normativi hanno prodotto una similarità coseno media di 0,869 (DS = 0,046), superiore al dominio tecnico. Questo schema è coerente con l'aspettativa che il testo normativo - essendo formalmente definito nei documenti giuridici primari - fornisca un forte ancoraggio per le risposte dei modelli, riducendo la variazione attribuibile a diverse rappresentazioni della conoscenza.

**Dominio C (Strategico):** I prompt strategici hanno mostrato una similarità coseno media di 0,845 (DS = 0,037). La deviazione standard più elevata riflette la genuina diversità delle posizioni legittime degli esperti su questioni architetturali e strategiche, coerente con l'ipotesi H3.

## 4.3 Risultati dei test delle ipotesi

**H1 (Convergenza nei domini fattuali):** La similarità coseno per coppie media sui prompt dei domini A e B era 0,851, che supera la soglia pre-registrata di 0,75. L'ipotesi H1 è quindi **CONFERMATA**.

**H3 (Effetto del dominio sulla convergenza):** La similarità per coppie media per il dominio A+B (0,851) superava quella del dominio C (0,845), con un delta di 0,006 punti percentuali. L'ipotesi H3 è **CONFERMATA**.

## 4.4 Caratteristiche di risposta per modello

**Tabella 2: Statistiche di token di risposta per modello (tutti i 45 prompt)**

| Modello | Token medi | Dev. std. | Tasso di anomalia |
|---|---|---|---|
| M1 (Sonnet) | 2143 | 909 | 0,15 |
| M2 (Opus) | 768 | 358 | 0,15 |
| M3 (GPT-5.3) | 919 | 382 | 0,11 |
| M4 (Gemini-2.5) | 2664 | 652 | 0,30 |
| M5 (Sonar) | 618 | 206 | 0,07 |

La verbosità delle risposte variava sostanzialmente tra i modelli. M4 (Gemini 2.5-pro) produceva le risposte più lunghe in media, mentre M5 (Sonar) era sistematicamente il più conciso. Questo schema era coerente nei tre domini. Come indicato nella sezione 7.4, la lunghezza in token non predice l'accuratezza fattuale; è un segnale stilistico che riflette lo stile di risposta predefinito di ciascun modello.

La correlazione tra verbosità e convergenza era debole: il modello più verboso (M4) mostrava punteggi di convergenza comparabili al più conciso (M5), suggerendo che le differenze di lunghezza non indicano sistematicamente divergenze di contenuto.
