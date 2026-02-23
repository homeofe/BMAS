# 5. Analisi della divergenza

## 📊 5.1 Risultati del rilevamento delle anomalie

Su tutti i 45 prompt, 12 (44 %) hanno prodotto almeno un modello semanticamente anomalo identificato da DBSCAN (eps=0,15, min_samples=2). La frequenza delle anomalie era più alta nel dominio C (strategico), coerente con l'aspettativa che le domande ambigue producano embedding di risposta più diversificati.

**Tabella 3: Frequenza delle anomalie per dominio**

| Dominio | Prompt con anomalie | Totale prompt | Tasso |
|---|---|---|---|
| Tecnico (A) | 5 | 10 | 50 % |
| Normativo (B) | 4 | 10 | 40 % |
| Strategico (C) | 3 | 7 | 43 % |

**Tabella 4: Tasso di anomalie per modello (tutti i prompt)**

| Modello | Numero anomalie | Tasso di anomalie |
|---|---|---|
| M1 (Sonnet) | 4 | 0,15 (15 %) |
| M2 (Opus) | 4 | 0,15 (15 %) |
| M3 (GPT-5.3) | 3 | 0,11 (11 %) |
| M4 (Gemini-2.5) | 8 | 0,30 (30 %) |
| M5 (Sonar) | 2 | 0,07 (7 %) |

Sonar Deep Research (M6) aveva il tasso di anomalie più alto a 0,11, mentre Sonar (M5) aveva il più basso a 0,07. Un alto tasso di anomalie per un modello specifico non indica necessariamente qualità inferiore - può riflettere uno stile di risposta più distintivo o una tendenza a una copertura più completa che allontana il suo embedding dal centroide.

## 5.2 Correlazione divergenza-allucinazione (Ipotesi H2)

Per testare H2, abbiamo confrontato i punteggi di accuratezza fattuale tra le risposte di modelli anomali e non anomali per i prompt dei domini A e B. L'accuratezza fattuale è stata valutata confrontando ogni risposta con la checklist di riferimento pre-registrata per ciascun prompt.

> Nota: I risultati dettagliati di H2 inclusi i punteggi di accuratezza fattuale richiedono l'annotazione manuale della ground truth, parzialmente completata prima delle esecuzioni dei modelli (vedi sezione 3.3.3). I risultati completi di annotazione sono disponibili nel dataset supplementare.

Un caso notevole dai dati pilota (A01, punteggio CVSS): M1 ha attribuito 9,8 (matematicamente corretto dato il vettore), mentre i modelli convergenti accettavano il 9,6 dichiarato dal fornitore. L'anomalia (M1) era fattualmente superiore al consenso. Ciò dimostra che H2 deve essere interpretata con cautela: **lo stato di anomalia è un segnale per la revisione umana, non un verdetto di incorrettezza.**

## 5.3 Schemi di divergenza per dominio

Il dominio strategico (C) ha mostrato la maggiore divergenza non solo nei punteggi di similarità semantica ma anche nelle caratteristiche strutturali. Le risposte ai prompt del dominio C variavano nelle raccomandazioni fondamentali: modelli diversi prediligevano architetture diverse (microservizi vs. monolite), diverse priorità di migrazione (TLS-first vs. firma del codice-first) e diverse strategie di investimento (certificazione vs. controlli tecnici).

Questa diversità è legittima. A differenza dei prompt fattuali dove una risposta è corretta, i prompt strategici non hanno una ground truth autorevole. Il framework BMAS tratta questo come segnale informativo: quando i sistemi esperti sono in disaccordo, il disaccordo stesso argomenta a favore della deliberazione umana piuttosto che del processo decisionale automatico.
