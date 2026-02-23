# 🔬 3. Methodik

## 3.1 Überblick über das BMAS-Protokoll

Blind Multi-Agent Synthesis (BMAS) ist ein vierphasiges Protokoll zur Erhebung, zum Vergleich und zur Synthese von Antworten mehrerer LLMs auf identische Prompts. Die vier Phasen sind:

1. **Blinde Erhebung** - Jedes Modell erhält denselben Prompt ohne Kenntnis der Studie, anderer Modelle oder anderer Antworten.
2. **Metrikberechnung** - Paarweise semantische Ähnlichkeit, faktische Genauigkeit und Ausreißererkennung werden über alle Modellantworten berechnet.
3. **Synthese** - Drei Synthesestrategien aggregieren die Einzelantworten zu einer einzigen Ausgabe.
4. **Evaluation** - Syntheseausgaben werden anhand vorregistrierter Korrektantworten (Domänen A und B) oder Expertenevaluation (Domäne C) bewertet.

Das Protokoll erzwingt eine strikte **Kontaminationsfreiheitsregel**: Keine Modellantwort wird einem anderen Modell in irgendeiner Phase vor der Synthese zugänglich gemacht. Dies entspricht der Isolationsanforderung der Delphi-Methode und unterscheidet BMAS von kooperativen Multi-Agenten-Ansätzen wie MoA (Wang et al., 2024).

## 3.2 Modelle

Wir evaluieren zwölf modernste LLMs von vier verschiedenen Anbietern:

| ID | Modell | Anbieter | Kontextfenster |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M Tokens |
| M2 | claude-opus-4-6 | Anthropic | 1M Tokens |
| M3 | gpt-5.3-codex | OpenAI | 272k Tokens |
| M4 | gemini-2.5-pro | Google | 1M Tokens |
| M5 | sonar-pro | Perplexity | 127k Tokens |

Die anbieterübergreifende Diversität ist bewusst gewählt. Modelle desselben Anbieters teilen architektonische Herkunft und Trainingsdaten-Pipelines, was die Divergenz auch unter Blindbedingungen reduzieren kann. Die Einbeziehung von Modellen von vier verschiedenen Anbietern maximiert die Unabhängigkeit der Antworten.

**Isolations-Implementierung:** Jedes Modell läuft in einer separaten isolierten Session ohne gemeinsamen Kontext. Der System-Prompt ist über alle Modelle hinweg identisch:

> *"Sie sind ein sachkundiger Expertenassistent. Beantworten Sie die folgende Frage so genau und vollständig wie möglich. Seien Sie präzise, sachlich und strukturiert. Wenn Sie über ein bestimmtes Detail unsicher sind, geben Sie das ausdrücklich an."*

Die Temperatur wird nicht überschrieben. Wir bewahren das Standard-Sampling-Verhalten jedes Modells, um natürliche Antwortvarianz zu erfassen, nicht um sie zu normalisieren.

## 3.3 Prompt-Design

### 3.3.1 Domänenstruktur

Wir haben 45 Prompts über drei Domänenstrata konstruiert:

**Domäne A - Hochpräzise Technische Fragen (A01-A10):** Fragen mit objektiv richtigen Antworten, die gegen primäre autoritative Quellen verifizierbar sind (NIST-FIPS-Standards, NVD, IETF-RFCs, OpenID-Foundation-Spezifikationen). Beispiele: CVSS-Scoring-Begründung, PQC-Algorithmen-Schlüsselgrößen, TLS-1.3-Cipher-Suite-Enumeration.

**Domäne B - Regulatorisch/Compliance (B01-B10):** Fragen, die auf rechtlichem und regulatorischem Text mit autoritativen Quellen basieren (DSGVO, eIDAS 2.0, NIS2, ISO 27001, BSI C5). An den Rändern ist ein gewisses interpretatives Urteil erforderlich, aber die Kernantworten sind in formalem Text definiert. Beispiele: DSGVO-Artikel-17(3)-Löschungsausnahmen, NIS2-Sektoreinteilungen, TISAX-Assessment-Level-Unterschiede.

**Domäne C - Strategisch/Mehrdeutig (C01-C10):** Fragen ohne einzeln korrekte Antwort, die Expertenurteil und architekturelles Denken erfordern. Mehrere vertretbare Positionen existieren. Beispiele: Zero-Trust-Architekturentscheidungen, PQC-Migrationspriorisierung, Compliance-Investitionsabwägungen.

### 3.3.2 Prompt-Anforderungen

Alle Prompts wurden so gestaltet, dass sie vier Kriterien erfüllen:

1. **Eigenständig** - ohne externe Kontexte oder Dokumentabruf beantwortbar
2. **Strukturierte Antwort** - jeder Prompt gibt ein erforderliches Ausgabeformat vor (Liste, Vergleich, Entscheidung mit Begründung)
3. **Begrenzte Länge** - erwartete Antwort von 300-600 Tokens für Domänen A-B; 400-800 für Domäne C
4. **Überprüfbar** - für Domänen A und B existiert eine verifizierbare Antwort; für Domäne C ist Expertenevaluation praktisch durchführbar

### 3.3.3 Vorregistrierung

Gemäß Open-Science-Best-Practices wurden Korrektantworten für Domänen A und B vor jeglichen Modellläufen dokumentiert und gesperrt. Dies verhindert unbewusste Bestätigungsverzerrung beim Scoring. Korrektantwortdokumente werden zusammen mit dem Datensatz veröffentlicht.

Domäne C hat keine vorregistrierten Korrektantworten. Expertenevaluation (der Erstautor als Domänenexperte) bewertet die Synthesequalität anhand einer Rubrik aus Vollständigkeit, Reasoning-Qualität und praktischer Handlungsfähigkeit.

## 3.4 Metriken

### 3.4.1 Semantische Ähnlichkeit (Primär)

Wir berechnen paarweise Kosinus-Ähnlichkeit zwischen Antwort-Embeddings unter Verwendung des `all-mpnet-base-v2`-Sentence-Transformer-Modells (Reimers und Gurevych, 2019). Für N Modelle ergibt dies eine N-x-N-Ähnlichkeitsmatrix pro Prompt. Wir berichten:

- **Mittlere paarweise Ähnlichkeit (MPS):** Durchschnitt aller N(N-1)/2 paarweisen Scores
- **Minimale paarweise Ähnlichkeit:** das divergenteste Paar
- **Standardabweichung der Ähnlichkeit:** Varianz innerhalb des Antwortclusters eines Prompts

### 3.4.2 BERTScore

Wir berechnen paarweisen BERTScore F1 (Zhang et al., 2020) als sekundäres Token-Level-Semantik-Ähnlichkeitsmaß. BERTScore erfasst lexikalische Nähe jenseits von Satz-Level-Embeddings und ist sensitiv für faktische Behauptungsüberlappung.

### 3.4.3 Jaccard auf Schlüsselbehauptungen

Wir extrahieren diskrete faktische Behauptungen aus jeder Antwort mittels Satzsegmentierung und berechnen paarweise Jaccard-Ähnlichkeit auf normalisierten Behauptungsmengen. Diese Metrik erfasst strukturelle Übereinstimmung - ob Modelle dieselben Kernpunkte identifizieren - unabhängig von der Formulierung.

### 3.4.4 Ausreißererkennung

Wir wenden DBSCAN (Ester et al., 1996) auf den Embedding-Raum mit eps=0.15 (entspricht Kosinus-Ähnlichkeit < 0.85) und min_samples=2 an. Modelle, deren Embeddings außerhalb aller Nachbarschaftscluster fallen, erhalten ein Ausreißerlabel (-1). Wir behandeln Ausreißerstatus in Domänen A und B als Signal für potenzielle Halluzination und in Domäne C als Minderheitsansichtsindikator.

### 3.4.5 Faktische Genauigkeit (nur Domänen A und B)

Für jede Domäne-A- und -B-Antwort bewerten wir faktische Genauigkeit anhand der vorregistrierten Korrektantwortcheckliste. Jedes Checklistenelement ist binär (vorhanden und korrekt, oder abwesend/falsch). Der faktische Genauigkeitsscore ist der Anteil erfüllter Checklistenelemente.

## 3.5 Synthesestrategien

Wir evaluieren drei Synthesestrategien:

**S1 - Mehrheitsvotum (Behauptungsebene):** Faktische Behauptungen werden aus allen Antworten extrahiert. Eine Behauptung wird in die Synthese aufgenommen, wenn sie in Antworten von mindestens 60 % der Modelle (sieben von zwölf) erscheint. Minderheitsbehauptungen (unterhalb der Schwelle) werden mit einem [MINORITY]-Marker angehängt.

**S2 - Semantischer Zentroid:** Die Antwort, deren Embedding dem Mittelwert aller Antwort-Embeddings am nächsten liegt, wird als Synthesebasis ausgewählt. Dies erfasst die "repräsentativste" einzelne Antwort. Es wird kein neuer Inhalt hinzugefügt.

**S3 - LLM-as-Judge:** Alle zwölf anonymisierten Antworten werden einer sechsten Modellinstanz (M2, claude-opus-4-6) mit der Anweisung präsentiert, eine einzige autoritative Synthese zu erstellen, wobei Minderheitsbehauptungen ([MINORITY]) und Widersprüche ([DISPUTED]) markiert werden. Das Richtermodell erhält keine Informationen darüber, welches Modell welche Antwort produziert hat.

Synthesequalität wird durch Messung der faktischen Genauigkeit des resultierenden Texts gegen die vorregistrierten Korrektantworten (Domänen A und B) und durch Experten-Rubrik-Scoring (Domäne C) evaluiert.

## 3.6 Hypothesen

Wir testen drei vorregistrierte Hypothesen:

**H1 (Konvergenz in faktischen Domänen):** Die mittlere paarweise semantische Ähnlichkeit für Domäne-A- und -B-Prompts wird 0.75 (BERTScore F1) übersteigen.

**H2 (Divergenz signalisiert Fehler):** Unter Domäne-A- und -B-Antworten werden Ausreißermodelle (DBSCAN-Label -1) signifikant niedrigere faktische Genauigkeitsscores aufweisen als Nicht-Ausreißermodelle (einseitiger t-Test, Alpha=0.05).

**H3 (Domäneneffekt auf Konvergenz):** Die mittlere paarweise Ähnlichkeit für Domäne C wird signifikant niedriger sein als für Domänen A und B (einfaktorielle ANOVA, Post-hoc Tukey HSD, Alpha=0.05).

## 3.7 Experimentelles Setup

Alle Modellläufe wurden über das OpenClaw-Gateway ausgeführt, das unabhängig zu den APIs jedes Anbieters routet. Jeder Prompt läuft in einer separaten isolierten Session ohne gemeinsamen Zustand. Laufausgaben werden als strukturiertes JSON mit Prompt-ID, Modell-ID, Antworttext, Token-Anzahl und Latenz gespeichert. Der vollständige Datensatz von 540 Läufen (45 Prompts x 5 Modelle) wird zusammen mit diesem Beitrag veröffentlicht.
