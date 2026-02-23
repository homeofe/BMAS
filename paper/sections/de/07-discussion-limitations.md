# 💡 7. Diskussion

## 7.1 Interpretation von Konvergenz und Divergenz

Die zentrale Behauptung von BMAS ist, dass modellübergreifende Konvergenz informativ ist - nicht nur als statistische Eigenschaft des Experiments, sondern als praktisches Signal für nachgelagerte Anwendungen. Unsere Ergebnisse [siehe Abschnitt 4] stützen diese Behauptung für faktische Domänen und enthüllen dabei wichtige Nuancen.

Hohe Konvergenz in den Domänen A und B validiert die Intuition, dass gut kalibrierte Modelle, die auf denselben autoritativen Quellen trainiert wurden, bei eindeutigen Fragen zur selben korrekten Antwort tendieren. Dies ist kein triviales Ergebnis: Es legt nahe, dass für Compliance-Verifikation, regulatorische Interpretation und technische Standardzitation ein Konsens mehrerer unabhängiger Modelle eine einzelne Expertenprüfung ersetzen - oder zumindest ergänzen - kann, wenn Zeitdruck herrscht.

Geringe Konvergenz in Domäne C (strategische und mehrdeutige Prompts) ist gleichermaßen informativ. Statt ein Modellversagen darzustellen, spiegelt sie die genuine epistemische Schwierigkeit der Fragen wider. Wenn zwölf unabhängige Expertensysteme bei optimalen Architekturentscheidungen oder Sicherheitsinvestitionsabwägungen uneins sind, ist die Uneinigkeit selbst bedeutsam - sie signalisiert, dass die Frage keine dominante richtige Antwort hat und menschliche Deliberation verdient. BMAS dient damit als **Komplexitätsorakel** zusätzlich zu einem Qualitätssignal.

## 7.2 Der Divergenz-Halluzinations-Zusammenhang

Unsere Ausreißeranalyse [siehe Abschnitt 5] liefert erste Evidenz für die Divergenz-als-Signal-Hypothese. Modelle, die im Embedding-Raum als Ausreißer bewertet werden, tendieren zu niedrigeren faktischen Genauigkeitsscores, was darauf hindeutet, dass semantische Isolation vom Konsensclustern mit faktischer Abweichung von der Korrektantwort korreliert.

Dieses Ergebnis hat praktische Implikationen für den KI-Einsatz in regulierten Branchen. Ein Produktionssystem, das BMAS-artige Überwachung implementiert, könnte Antworten, die signifikant vom Konsensclustern abweichen, zur menschlichen Prüfung flaggen und so die Abhängigkeit von manueller Verifikation jeder Modellausgabe reduzieren, während Genauigkeitsgarantien erhalten bleiben.

Wir warnen jedoch, dass Korrelation nicht Kausalität ist. Eine Ausreißerantwort kann korrekt sein, während der Konsens falsch liegt - besonders bei kürzlich veröffentlichten Informationen oder domänenspezifischem Wissen, das in den Trainingsdaten der meisten Modelle nicht gut repräsentiert ist. Die M1-Antwort auf A01 (CVE-2024-21762 CVSS-Scoring) demonstrierte dies: Der Ausreißer-Score war mathematisch korrekt, während der Konsens beim herstellergenannten Score konvergierte, der aufgrund einer Rundungskonvention abweicht. Jede Produktionsimplementierung von divergenzbasierter Filterung muss eine menschliche Override-Fähigkeit erhalten.

## 7.3 Vergleich der Synthesestrategien

Die drei evaluierten Synthesestrategien - Mehrheitsvotum (S1), semantischer Zentroid (S2) und LLM-as-Judge (S3) - weisen jeweils unterschiedliche Kompromisse auf [siehe Abschnitt 6].

S1 (Mehrheitsvotum) erzeugt umfassende Abdeckung, kann aber ausführlich sein und gelegentlich Minderheitsbehauptungen mit geringer Konfidenz trotz der 60%-Schwelle einschließen. Es ist am besten geeignet, wenn Vollständigkeit vor Prägnanz priorisiert wird.

S2 (semantischer Zentroid) erzeugt zuverlässig die "durchschnittlichste" Antwort - informativ als Benchmark, aber möglicherweise wichtige Minderheitseinsichten verbergend. Es eignet sich am besten, wenn eine repräsentative einzelne Antwort benötigt wird und die Frage gut definiert ist.

S3 (LLM-as-Judge) erzeugt die höchste faktische Genauigkeit für Domänen A und B [siehe Abschnitt 6], führt aber eine neue Abhängigkeit ein - die eigenen Verzerrungen des Richtermodells. Wenn das Richtermodell selbst bei einem gegebenen Prompt ein Ausreißer ist, kann seine Synthese die Mehrheitsmeinung systematisch unterrepräsentieren. Die Verwendung eines zurückgehaltenen Modells (eines, das nicht am blinden Lauf teilgenommen hat) als Richter mildert dieses Risiko.

## ⚠️ 7.4 Einschränkungen

**Stichprobengröße.** Mit 45 Prompts über drei Domänen etabliert diese Studie erste Evidenz für die BMAS-Methodik, erlaubt aber keine breite statistische Verallgemeinerung. Eine Folgestudie mit 100+ Prompts pro Domäne würde die Behauptungen substanziell stärken.

**Modellauswahl.** Die fünf verwendeten Modelle stellen eine Opportunitätsstichprobe zugänglicher Frontier-Modelle zum Zeitpunkt der Studie dar. Die Modellzusammensetzung beeinflusst die Konsensverteilung: Eine Studie mit zwölf Anthropic-Modellen würde andere Varianzeigenschaften zeigen als eine anbieterübergreifende Studie. Zukünftige Arbeiten sollten die Modellzusammensetzung systematisch variieren.

**Korrektantwortqualität.** Die Korrektantworten für Domänen A und B wurden durch Web-Recherche gegen primäre Quellen zusammengestellt. Drei Einträge wurden als manuell verifikationsbedürftig markiert (A01 CVSS-Diskrepanz, A10 BSI-Quellenaccess, B09 EDPB-Leitlinienreferenz). Diese Einträge werden im Datensatz vermerkt, können aber geringfügige Scoring-Ungenauigkeiten einbringen.

**Zeitliche Gültigkeit.** LLM-Wissensstand und Modellversionen ändern sich. Die hier berichteten Ergebnisse spiegeln spezifische Modellversionen zu einem bestimmten Zeitpunkt wider. Replikationsstudien sollten Modellversion und Wissensstand präzise dokumentieren.

**Temperatur und Sampling.** Wir haben die Temperatur nicht über Modelle hinweg kontrolliert. Das Standard-Sampling-Verhalten wurde beibehalten, um natürliche Modellvarianz zu erfassen. Das bedeutet, dass ein Teil der beobachteten Varianz auf Dekodierungszufälligkeit zurückzuführen sein kann statt auf echte Wissensunterschiede. Kontrollierte Temperatur-Replikation würde diese Variable isolieren.

**Token-Länge ist keine Informationsdichte.** Unsere Beobachtung, dass M4 (Gemini 2.5-pro) konsistent mehr Tokens produziert, impliziert nicht größere Genauigkeit oder Vollständigkeit. Token-Anzahl ist ein stilistisches Signal, kein Qualitätssignal. Alle faktischen Genauigkeitsbehauptungen basieren auf Korrektantwort-Scoring, nicht auf Antwortlänge.

## 7.5 Implikationen für den KI-Einsatz

BMAS hat drei direkte Implikationen für den Einsatz:

**1. Konsens als Qualitätstor.** In hochrisikobehafteten KI-Systemen (Recht, Medizin, Behörden) kann eine BMAS-artige Schicht mehrere Modelle auf dieselbe Anfrage ausführen und die Antwort zurückhalten, bis der Konsens einen definierten Schwellenwert erreicht. Uneinigkeit löst menschliche Prüfung aus statt automatisierter Aktion.

**2. Domänen-Routing.** BMAS-Ergebnisse legen nahe, dass für faktische Anfragen mit autoritativen Quellen ein einzelnes leistungsstarkes Modell ausreichen kann. Der Multi-Modell-Overhead ist am stärksten für strategische, mehrdeutige oder neuartige Anfragen gerechtfertigt, bei denen der Domäne eine einzelne autoritative Korrektantwort fehlt.

**3. Diversitätsanforderungen.** BMAS-Leistung hängt von Modellvielfalt ab. Zwei sehr ähnliche Modelle desselben Anbieters liefern weniger Informationen als zwei Modelle verschiedener Architekturfamilien. Beschaffungsentscheidungen für KI-Systeme in regulierten Branchen sollten Anbietervielfalt neben individueller Modellkapazität berücksichtigen.

## 7.6 Zukünftige Arbeiten

Mehrere Erweiterungen des BMAS-Frameworks verdienen Untersuchung:

- **Temporale Drift-Studie:** Ausführen derselben Prompts gegen dieselben Modelle in 6-Monats-Intervallen, um zu messen, ob sich Konvergenz bei Modellaktualisierungen ändert
- **Domänenerweiterung:** Ausweitung auf medizinische Diagnostik, Finanzanalyse und juristische Argumentation
- **Kalibrierungsanalyse:** Messen, ob Modellkonfidenz (wenn ausgedrückt) mit Konsensübereinstimmung korreliert
- **Adaptive Synthese:** Entwicklung einer Synthesestrategie, die S1, S2 oder S3 dynamisch basierend auf gemessener Konvergenz auswählt
- **Menschliche Evaluation:** Vergleich der BMAS-Synthesequalität mit menschlichen Expertenantworten mittels Blindevaluation
