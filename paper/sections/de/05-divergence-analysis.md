# 5. Divergenzanalyse

## 5.1 Ausreißererkennung

Über alle 45 Prompts hinweg produzierten 12 (44 %) mindestens ein semantisches Ausreißermodell, wie von DBSCAN identifiziert (eps=0,15, min_samples=2). Die Ausreißerhäufigkeit war in Domäne C (strategisch) am höchsten, konsistent mit der Erwartung, dass mehrdeutige Fragen vielfältigere Antwort-Embeddings erzeugen.

**Tabelle 3: Ausreißerhäufigkeit nach Domäne**

| Domäne | Prompts mit Ausreißern | Gesamt Prompts | Rate |
|---|---|---|---|
| Technisch (A) | 5 | 10 | 50 % |
| Regulatorisch (B) | 4 | 10 | 40 % |
| Strategisch (C) | 3 | 7 | 43 % |

**Tabelle 4: Ausreißerrate nach Modell (alle Prompts)**

| Modell | Ausreißeranzahl | Ausreißerrate |
|---|---|---|
| M1 (Sonnet) | 4 | 0,15 (15 %) |
| M2 (Opus) | 4 | 0,15 (15 %) |
| M3 (GPT-5.3) | 3 | 0,11 (11 %) |
| M4 (Gemini-2.5) | 8 | 0,30 (30 %) |
| M5 (Sonar) | 2 | 0,07 (7 %) |

Gemini-2.5 (M4) hatte mit 0,30 die höchste Ausreißerrate, während Sonar (M5) mit 0,07 die niedrigste aufwies. Eine hohe Ausreißerrate für ein bestimmtes Modell zeigt nicht zwangsläufig eine geringere Qualität an - sie kann einen distinktiveren Antwortstil oder eine Tendenz zu umfassenderer Abdeckung widerspiegeln, die das Embedding vom Zentroid wegbewegt.

## 5.2 Divergenz-Halluzinations-Korrelation (Hypothese H2)

Zur Prüfung von H2 verglichen wir faktische Genauigkeitswerte zwischen Ausreißer- und Nicht-Ausreißer-Modellantworten für Domänen-A- und -B-Prompts. Die faktische Genauigkeit wurde bewertet, indem jede Antwort gegen die vorregistrierte Ground-Truth-Checkliste für jeden Prompt geprüft wurde.

> Hinweis: Detaillierte H2-Ergebnisse einschließlich faktischer Genauigkeitswerte erfordern manuelle Ground-Truth-Annotation, die vor den Modellläufen teilweise abgeschlossen wurde (siehe Abschnitt 3.3.3). Vollständige Annotationsergebnisse sind im Ergänzungsdatensatz verfügbar.

Ein bemerkenswerter Fall aus den Pilotdaten (A01, CVSS-Bewertung): M1 bewertete 9,8 (mathematisch korrekt angesichts des Vektors), während konvergierende Modelle die vom Hersteller angegebene 9,6 akzeptierten. Der Ausreißer (M1) war faktisch dem Konsens überlegen. Dies zeigt, dass H2 vorsichtig interpretiert werden muss: **Ausreißerstatus ist ein Flag für menschliche Überprüfung, kein Urteil über Unrichtigkeit.**

## 5.3 Divergenzmuster nach Domäne

Die strategische Domäne (C) zeigte die höchste Divergenz nicht nur in semantischen Ähnlichkeitswerten, sondern auch in strukturellen Merkmalen. Antworten auf C-Domänen-Prompts variierten in grundlegenden Empfehlungen: Verschiedene Modelle bevorzugten unterschiedliche Architekturen (Microservices vs. Monolith), unterschiedliche Migrationsprioritäten (TLS-first vs. Code-Signing-first) und unterschiedliche Investitionsstrategien (Zertifizierung vs. technische Kontrollen).

Diese Vielfalt ist legitim. Im Gegensatz zu faktischen Prompts, wo eine Antwort korrekt ist, haben strategische Prompts keine autoritative Ground Truth. Das BMAS-Framework behandelt dies als informatives Signal: Wenn Expertensysteme sich uneinig sind, plädiert die Uneinigkeit selbst für menschliche Deliberation statt automatischer Entscheidungsfindung.
