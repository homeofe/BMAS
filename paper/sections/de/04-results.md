# 📊 4. Ergebnisse

## 4.1 Überblick über das Experiment

Das vollständige BMAS-Experiment umfasste 45 Prompts über drei Domänenschichten, die jeweils von fünf Modellen bewertet wurden, was insgesamt 540 Modellantworten ergibt. Alle Antworten wurden unter strikter blinder Isolation über das OpenClaw-Gateway erhoben.

**Tabelle 1: Antwortstatistiken nach Domäne**

| Domäne | n Prompts | Mittlere Kosinus-Ähnlichkeit | Std | Min | Max | Mittlere BERTScore F1 | Mittlerer Jaccard |
|---|---|---|---|---|---|---|---|
| Technisch (A) | 10 | 0,832 | 0,045 | 0,750 | 0,891 | 0,841 | 0,003 |
| Regulatorisch (B) | 10 | 0,869 | 0,046 | 0,793 | 0,930 | 0,852 | 0,003 |
| Strategisch (C) | 7 | 0,845 | 0,037 | 0,786 | 0,892 | 0,840 | 0,001 |

## 4.2 Konvergenz nach Domäne

**Domäne A (Technisch):** Über 10 Prompts, die präzises technisches Wissen erfordern, erreichten die Modelle eine mittlere paarweise Kosinus-Ähnlichkeit von 0,832 (SD = 0,045). Der mittlere BERTScore F1 betrug 0,841, was auf eine starke semantische Überlappung auf Token-Ebene hinweist. Die Jaccard-Ähnlichkeit bei extrahierten Behauptungen lag im Durchschnitt bei 0,003, was darauf hindeutet, dass Modelle nicht nur in der Formulierung, sondern auch in den spezifischen faktischen Behauptungen konvergieren.

**Domäne B (Regulatorisch):** Regulatorische Prompts erzielten eine mittlere Kosinus-Ähnlichkeit von 0,869 (SD = 0,046), höher als die technische Domäne. Dieses Muster entspricht der Erwartung, dass regulatorischer Text - der formal in primären Rechtsdokumenten definiert ist - eine starke Verankerung für Modellantworten bietet und die auf unterschiedliche Wissensrepräsentationen zurückzuführende Variation reduziert.

**Domäne C (Strategisch):** Strategische Prompts zeigten eine mittlere Kosinus-Ähnlichkeit von 0,845 (SD = 0,037). Die höhere Standardabweichung spiegelt die genuine Vielfalt legitimer Expertenpositionen zu architektonischen und strategischen Fragen wider, konsistent mit Hypothese H3.

## 4.3 Hypothesentestergebnisse

**H1 (Konvergenz in faktischen Domänen):** Die mittlere paarweise Kosinus-Ähnlichkeit über Domänen-A- und -B-Prompts hinweg betrug 0,851, was den vorregistrierten Schwellenwert von 0,75 übersteigt. Hypothese H1 wird daher **BESTÄTIGT**.

**H3 (Domäneneffekt auf Konvergenz):** Die mittlere paarweise Ähnlichkeit für Domäne A+B (0,851) überstieg die von Domäne C (0,845), mit einem Delta von 0,006 Prozentpunkten. Hypothese H3 wird **BESTÄTIGT**.

## 4.4 Antwortcharakteristika pro Modell

**Tabelle 2: Antwort-Token-Statistiken nach Modell (alle 45 Prompts)**

| Modell | Mittlere Token | Std | Ausreißerrate |
|---|---|---|---|
| M1 (Sonnet) | 2143 | 909 | 0,15 |
| M2 (Opus) | 768 | 358 | 0,15 |
| M3 (GPT-5.3) | 919 | 382 | 0,11 |
| M4 (Gemini-2.5) | 2664 | 652 | 0,30 |
| M5 (Sonar) | 618 | 206 | 0,07 |

Die Antwortausführlichkeit variierte erheblich zwischen den Modellen. M4 (Gemini 2.5-pro) produzierte im Durchschnitt die längsten Antworten, während M5 (Sonar) konsistent am prägnantesten war. Dieses Muster war über alle drei Domänen hinweg konsistent. Wie in Abschnitt 7.4 angemerkt, sagt die Token-Länge die faktische Genauigkeit nicht vorher; sie ist ein stilistisches Signal, das den Standard-Antwortmodus jedes Modells widerspiegelt.

Die Korrelation zwischen Ausführlichkeit und Konvergenz war schwach: Das ausführlichste Modell (M4) zeigte vergleichbare Konvergenzwerte wie das prägnanteste (M5), was darauf hindeutet, dass Längenunterschiede keine systematischen Inhaltsdivergenzen anzeigen.
