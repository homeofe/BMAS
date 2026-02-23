# 📋 Zusammenfassung

Wir stellen **Blind Multi-Agent Synthesis (BMAS)** vor, eine Methodik zur Messung von Konvergenz und Divergenz mehrerer großer Sprachmodelle (LLMs), die auf identische Prompts unter strikter gegenseitiger Isolation antworten. Inspiriert von der Delphi-Methode aus der Expertenprognose erzwingt BMAS eine vollständige Antwortisolation pro Modell: Kein Modell kennt die Ausgabe eines anderen Modells, bevor die Synthesephase beginnt.

Wir evaluieren zwölf modernste LLMs über drei Domänenebenen: (A) hochpräzise technische Fragen mit verifizierbaren Korrektantworten, (B) regulatorische und Compliance-Fragen mit autoritativen Rechtsquellen sowie (C) strategische und architekturelle Fragen mit legitimen Expertenmeinungsverschiedenheiten. Mithilfe semantischer Ähnlichkeitsmetriken (BERTScore, Kosinus-Embedding-Distanz), faktischer Genauigkeit gegen vorregistrierte Korrektantworten und Ausreißererkennung via DBSCAN-Clustering quantifizieren wir die modellübergreifende Abweichung sowie deren Zusammenhang mit Domänentyp und Halluzinationsrate.

Unsere zentrale Hypothese lautet: In gut definierten, faktischen Domänen konvergieren LLM-Antworten so stark, dass **Konsens als Qualitätssignal** dient. Hohe modellübergreifende Übereinstimmung ist ein Prädiktor für faktische Korrektheit, während signifikante Divergenz auf Modellhalluzinationen oder unzureichend spezifizierte Fragen hinweist. Zusätzlich evaluieren wir drei Synthesestrategien - Mehrheitsvotum auf Behauptungsebene, semantische Zentroidselektion und LLM-as-Judge-Synthese - anhand vorregistrierter Korrektantworten.

BMAS hat direkte praktische Implikationen für KI-Einsätze in Hochrisikobereichen wie Behörden, Gesundheitswesen und Rechtssystemen, in denen keiner einzelnen Modellausgabe bedingungslos vertraut werden kann. Indem BMAS **Divergenz als Anomaliesignal** statt als Koordinationsversagen behandelt, bietet es eine praktische Qualitätssicherungsschicht für LLM-Systeme im Produktivbetrieb.

**Schlagwörter:** Große Sprachmodelle, Multi-Agenten-Systeme, Konsens, Halluzinationserkennung, Delphi-Methode, semantische Ähnlichkeit, KI-Qualitätssicherung
