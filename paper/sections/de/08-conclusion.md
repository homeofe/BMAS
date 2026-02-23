# 🎯 8. Fazit

Dieser Beitrag stellte **Blind Multi-Agent Synthesis (BMAS)** vor, eine Methodik zur Erhebung, zum Vergleich und zur Synthese von Antworten mehrerer großer Sprachmodelle in strikter Isolation, und präsentierte empirische Ergebnisse aus einem 540-Läufe-Experiment über fünf Frontier-LLMs und drei Domänenstrata.

## 📋 8.1 Zusammenfassung der Beiträge

Wir haben demonstriert:

1. **Konvergenz ist domänenabhängig und messbar.** Über 45 Prompts zeigten die Modelle A und B (technische und regulatorische Domänen) konsistent höhere modellübergreifende semantische Ähnlichkeit als Domäne C (strategische und mehrdeutige Prompts). [Genaue Werte in Abschnitt 4.]

2. **Divergenz signalisiert Fehler in faktischen Domänen.** Als semantische Ausreißer durch DBSCAN-Clustering identifizierte Modelle wiesen niedrigere faktische Genauigkeit gegen vorregistrierte Korrektantworten auf als Nicht-Ausreißermodelle, was Hypothese H2 stützt. Dies liefert eine empirische Grundlage für die Verwendung von Divergenz als praktisches Qualitätstor in KI-gestützten Entscheidungssystemen.

3. **Synthesequalität variiert nach Strategie und Domäne.** LLM-as-Judge (S3)-Synthese erzielte die höchste faktische Genauigkeit in den Domänen A und B, während Mehrheitsvotum (S1) die umfassendste Abdeckung lieferte. Semantischer Zentroid (S2) schnitt als prägnante repräsentative Zusammenfassung am besten ab. Keine einzelne Strategie dominierte über alle Prompttypen.

4. **Modellausführlichkeit ist kein Qualitäts-Proxy.** Wir beobachteten erhebliche Variation in der Antwort-Token-Anzahl über Modelle bei identischen Prompts (bis zu 6,5-faches Verhältnis bei einigen Prompts), ohne konsistente Korrelation zwischen Antwortlänge und faktischer Genauigkeit. Gemini 2.5-pro war konsistent das ausführlichste Modell; Sonar das prägnanteste. Diese stilistischen Unterschiede sagen keine Konvergenz voraus.

## 8.2 Praktische Erkenntnisse

Für Praktiker, die LLMs in regulierten oder hochrisikobehafteten Umgebungen einsetzen, schlägt BMAS eine praktische Architektur vor: Prompts gegen mehrere unabhängige Modellanbieter ausführen, semantische Konvergenz messen und Antworten mit geringer Konfidenz (hoher Divergenz) zur menschlichen Prüfung weiterleiten. Der Overhead ist durch den Zuverlässigkeitsgewinn gerechtfertigt, insbesondere für Compliance-kritische Fragen, bei denen eine einzelne falsche Antwort rechtliche oder sicherheitsrelevante Konsequenzen hat.

Das in dieser Studie verwendete Vorregistrierungsprotokoll - Korrektantworten vor jeglichen Modellläufen zu sperren - ist auf jede Multi-Modell-Evaluationsanstrengung übertragbar und verhindert den Bestätigungsfehler, der entstehen kann, wenn Evaluatoren die Antworten kennen, bevor sie die Metriken entwerfen.

## 8.3 Beziehung zu AAHP und failprompt

BMAS wurde im Kontext von AAHP (AI-to-AI Handoff Protocol), einem strukturierten Multi-Agenten-Orchestrierungsframework für Produktions-KI-Pipelines, und failprompt, einem CLI-Tool zur Validierung von KI-Antworten in CI/CD-Umgebungen, entwickelt. Zusammen bilden diese drei Projekte ein integriertes Toolkit für verantwortungsvolles Multi-Modell-KI-Deployment: AAHP liefert die Orchestrierungsschicht, failprompt das CI-Tor, und BMAS die empirische Grundlage für das Verständnis, wann und warum Multi-Modell-Konsens zuverlässiger ist als eine einzelne Modellausgabe.

Alle Code-, Prompt-, vorregistrierten Korrektantwort- und Experimentergebnisse werden als offene Datensätze veröffentlicht, um die Replikation und Erweiterung dieser Arbeit zu unterstützen.

---

*Der BMAS-Datensatz, Runner, die Metrik-Pipeline und der Synthesecode sind verfügbar unter: https://github.com/homeofe/BMAS*
