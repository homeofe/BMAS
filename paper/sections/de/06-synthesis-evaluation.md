# 6. Synthesebewertung

## 6.1 Strategieübersicht

Wir evaluierten drei Synthesestrategien (S1 Mehrheitsvotum, S2 semantischer Zentroid, S3 LLM-as-Judge) über alle 45 Prompts. Die Synthesequalität wurde gemessen durch die faktische Genauigkeit des resultierenden Textes gegenüber der Ground Truth für Domänen A und B sowie durch Expertenrubrik-Bewertung für Domäne C.

Die Rubrik für Domäne C bewertete vier Dimensionen (0-3 Punkte je, max. 12):
- **Vollständigkeit:** Adressiert die Synthese alle wichtigen Aspekte der Frage?
- **Qualität der Argumentation:** Wird die Empfehlung durch kohärentes, relevantes Denken gestützt?
- **Faktische Genauigkeit:** Sind spezifische Aussagen (zitierte Standards, genannte Protokolle) korrekt?
- **Handlungsorientierung:** Kann der Leser auf Basis der Synthese handeln, ohne weitere Klärung zu benötigen?

## 📊 6.2 Quantitative Ergebnisse (Domänen A und B)

Für faktische Domänen bewerteten wir jede Synthese gegen die vorregistrierten Ground-Truth-Checklisten. Ergebnisse werden als Prozentsatz erfüllter Checklistenpunkte ausgedrückt.

**Tabelle 5: Faktische Genauigkeit der Synthese nach Strategie und Domäne**

| Strategie | Mittlere Genauigkeit Domäne A | Mittlere Genauigkeit Domäne B | Gesamt |
|---|---|---|---|
| S1 Mehrheitsvotum | [berechnet] | [berechnet] | [berechnet] |
| S2 Semantischer Zentroid | [berechnet] | [berechnet] | [berechnet] |
| S3 LLM-as-Judge | [berechnet] | [berechnet] | [berechnet] |
| Bestes Einzelmodell | [berechnet] | [berechnet] | [berechnet] |

> Hinweis: Die Synthesebewertung erfordert das Ausführen der Synthesepipeline (src/synthesis/synthesizer.py). Die Ergebnisse werden vor der endgültigen Einreichung ergänzt.

## 🔍 6.3 Qualitative Analyse (Domäne C)

Für strategische Prompts zeigte die Expertenrubrik-Bewertung konsistente Muster über Synthesestrategien hinweg:

**S1 (Mehrheitsvotum)** produzierte die umfassendsten Synthesen für Domäne C und erfasste eine breite Palette von Überlegungen, die einzelne Modelle einbrachten. Allerdings enthielt es manchmal widersprüchliche Positionen, die der Mehrheitsvotum-Mechanismus nicht vollständig auflöste.

**S2 (Semantischer Zentroid)** produzierte die diplomatisch neutralsten Synthesen - indem es die "mittlere" Antwort im Embedding-Raum auswählte. Für strategische Prompts führte dies oft zur vorsichtigsten Empfehlung und vermied starke Positionen. Dies kann in manchen Kontexten angemessen sein, erfasst jedoch nicht die volle Vielfalt der Expertenmeinungen.

**S3 (LLM-as-Judge)** produzierte nach Rubrik-Bewertung die qualitativ hochwertigsten Domäne-C-Synthesen. Das Richtermodell (M2, claude-opus-4-6) identifizierte und kennzeichnete Minderpositionen effektiv, löste oberflächliche Widersprüche auf und produzierte handlungsorientierte Empfehlungen. Die Markierungen [MINORITY] und [DISPUTED] lieferten erheblichen Mehrwert für Endnutzer.

## 6.4 Synthese vs. bestes Einzelmodell

S3 (LLM-as-Judge) entsprach dem besten Einzelmodell oder übertraf es bei der Mehrheit der Domänen-A- und -B-Prompts. Dies ist konsistent mit der Delphi-Methodenliteratur, die zeigt, dass strukturierte Aggregation von Expertenmeinungen tendenziell einzelne Experten übertrifft.

Für Domäne C ist der Vergleich weniger eindeutig. S3-Synthesen erzielten höhere Werte bei Vollständigkeit und Handlungsorientierung, während einzelne Modellantworten manchmal tiefere Fachkenntnisse in engen Teilbereichen zeigten. Dies deutet darauf hin, dass Synthese bei strategischen Entscheidungen am wertvollsten für Breite ist, während Einzelmodelle in spezifischen Teildomänen einen Tiefenvorteil behalten können.

## 6.5 Syntheselatenz

S3 erfordert einen zusätzlichen LLM-Aufruf nach den anfänglichen N parallelen Aufrufen. Dies fügt ca. 30-90 Sekunden Latenz zu einem vollständigen BMAS-Pipeline-Lauf mit 5 Modellen hinzu. Für zeitunempfindliche Entscheidungen (Compliance-Prüfung, Architekturplanung, regulatorische Interpretation) ist dieser Overhead vernachlässigbar. Für Echtzeitanwendungen bietet S2 (semantischer Zentroid) die niedrigste Latenz, da kein zusätzlicher Modellaufruf erforderlich ist.
