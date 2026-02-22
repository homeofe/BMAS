# 1. Einleitung

Große Sprachmodelle sind inzwischen leistungsfähig genug, dass sie in Domänen eingesetzt werden, in denen Genauigkeit keine Option, sondern eine Voraussetzung ist: Rechtsanalyse, medizinische Diagnostik, regulatorische Compliance und staatliche Identitätssysteme. In diesen Bereichen ist eine selbstsichere, aber falsche Antwort eines einzelnen Modells kein geringfügiges Ärgernis - sie ist ein Versagen mit realen Konsequenzen.

Der vorherrschende Ansatz zur Verbesserung der LLM-Zuverlässigkeit besteht entweder in besserem Training (RLHF, Constitutional AI) oder in besserem Prompting (Chain-of-Thought, Retrieval Augmentation). Beide Methoden operieren innerhalb eines Einzelmodell-Paradigmas: ein Modell, eine Ausgabe, eine Antwort - der man vertrauen kann oder nicht.

Dieser Beitrag verfolgt einen anderen Ansatz. Statt zu fragen "Wie machen wir ein Modell zuverlässiger?", fragen wir: **Was können wir aus der Uneinigkeit mehrerer Modelle lernen, die sich gegenseitig nicht beeinflussen dürfen?**

## 1.1 Die Kerneinsicht

Wenn fünf unabhängige Experten dieselbe Frage beantworten, ohne sich gegenseitig zu konsultieren, und vier von ihnen dieselbe Antwort geben, während einer eine abweichende gibt, schließen wir nicht, dass die vier falsch liegen. Wir untersuchen die abweichende Antwort genauer - vertrauen aber dem Konsens als Ausgangspunkt.

Dies ist die Delphi-Methode, die seit 1963 in der Expertenprognose eingesetzt wird. Ihre Stärke ist struktureller Natur: **Isolation verhindert Gruppendenken; Konsens entsteht aus unabhängigem Denken, nicht aus sozialem Druck.**

BMAS überträgt diese Logik auf LLMs. Jedes Modell ist ein Experte mit einer bestimmten Trainingsverteilung, einem bestimmten Wissensstand und einer Reihe von Verzerrungen. Wenn sie voneinander isoliert werden und dieselbe Frage erhalten, ist ihre Konvergenz oder Divergenz an sich informativ.

## 1.2 Was Neues ist

Mehrere frühere Arbeiten sind verwandt, aber grundlegend verschieden:

**Self-Consistency** (Wang et al., 2022) generiert mehrere Reasoning-Ketten aus einem *einzelnen* Modell und nutzt Mehrheitsvoting. BMAS verwendet *verschiedene* Modelle - dies testet über Trainingsverteilungen hinweg, nicht nur Dekodierungsvarianz.

**Mixture of Agents** (Wang et al., 2024) erlaubt Modellen, die Ausgaben der anderen in Aggregationsrunden zu sehen. Dies führt zu kollaborativer Verbesserung, birgt aber das Risiko der Fehlerfortpflanzung: Wenn ein Modell in Runde eins eine selbstsichere Halluzination produziert, können nachfolgende Modelle daran andocken.

**LLM-as-Judge** (Zheng et al., 2023) nutzt ein Modell zur Bewertung eines anderen. BMAS verwendet ein Modell zur *Synthese* der Ausgaben mehrerer anderer - die Richterrolle ist auf die finale Synthesephase beschränkt.

BMAS ist das erste Framework, das vier Eigenschaften kombiniert:
1. Strikte Blind-Isolation (keine gegenseitige Kontamination)
2. Modellvielfalt (verschiedene Anbieter, Architekturen, Trainingsverteilungen)
3. Domänenstratifizierte Analyse (faktisch, regulatorisch, strategisch)
4. Divergenz als Signal (nicht als Versagen)

## 1.3 Praktische Motivation

Diese Forschung entstand aus operativer Erfahrung beim Aufbau von AEGIS, einem grenzüberschreitenden EU-Identitätsverifizierungssystem, und AAHP (AI-to-AI Handoff Protocol), einem strukturierten Multi-Agenten-Orchestrierungsframework. In beiden Systemen werden Multi-Agenten-Pipelines für Architekturentscheidungen, Compliance-Analysen und Implementierungsreviews eingesetzt.

Eine praktische Frage stellte sich: Wenn mehrere LLMs als unabhängige Prüfer in einer Pipeline eingesetzt werden - wie stark unterscheiden sich ihre Ausgaben tatsächlich? Und wenn sie sich unterscheiden, wer hat recht?

BMAS ist die formale Antwort auf diese Frage.

## 1.4 Beiträge

Dieser Beitrag leistet folgende Beiträge:

1. **BMAS-Methodik:** Ein formalisiertes Blind-Multi-Agenten-Syntheseprotokoll mit Isolationsbedingungen, Metriksuite und Synthesestrategien.
2. **Empirische Studie:** Ergebnisse aus 30 Prompts über 5 LLMs in 3 Domänenstrata, mit vorregistrierten Korrektantworten für Domänen A und B.
3. **Validierung der Divergenz-als-Signal-Hypothese:** Statistische Evidenz, dass modellübergreifende Divergenz die faktische Fehlerrate vorhersagt.
4. **Vergleich von Synthesestrategien:** Empirische Evaluation von Mehrheitsvotum, semantischem Zentroid und LLM-as-Judge-Synthese anhand von Korrektantworten.
5. **Offener Datensatz:** Alle Prompts, rohe Modellausgaben und Metrikscores werden als öffentlicher Benchmark veröffentlicht.

## 1.5 Struktur des Beitrags

Abschnitt 2 bespricht verwandte Arbeiten. Abschnitt 3 beschreibt die BMAS-Methodik und das experimentelle Design. Abschnitt 4 präsentiert Ergebnisse. Abschnitt 5 analysiert die Divergenz-Halluzination-Korrelation. Abschnitt 6 evaluiert Synthesestrategien. Abschnitt 7 diskutiert Implikationen, Einschränkungen und zukünftige Arbeiten. Abschnitt 8 schließt ab.
