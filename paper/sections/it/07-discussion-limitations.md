# 7. Discussione

## 7.1 Interpretazione della convergenza e della divergenza

L'affermazione centrale di BMAS è che la convergenza inter-modello è informativa: non solo come proprietà statistica dell'esperimento, ma come segnale pratico per le applicazioni a valle. I nostri risultati [vedi sezione 4] supportano questa affermazione per i domini fattuali, rivelando importanti sfumature.

L'alta convergenza nei domini A e B valida l'intuizione che i modelli ben calibrati, addestrati sulle stesse fonti autorevoli, tendano verso le stesse risposte corrette quando le domande sono non ambigue. La bassa convergenza nel dominio C riflette la genuina difficoltà epistemica delle domande. Quando dodici sistemi esperti indipendenti non concordano su decisioni di architettura ottimali, il disaccordo stesso è significativo: segnala che la domanda non ha una risposta corretta dominante e merita deliberazione umana. BMAS funge così da **oracolo di complessità** oltre che da segnale di qualità.

## 7.2 La connessione divergenza-allucinazione

La nostra analisi dei valori anomali fornisce prove preliminari che i modelli identificati come anomali nello spazio degli embedding tendono ad avere punteggi di accuratezza fattuale più bassi. Un sistema di produzione che implementa un monitoraggio di tipo BMAS potrebbe segnalare le risposte che si discostano significativamente dal cluster di consenso per una revisione umana.

Avvertiamo tuttavia che la correlazione non implica causalità. Una risposta anomala può essere corretta mentre il consenso è errato. La risposta di M1 alla domanda A01 (punteggio CVSS di CVE-2024-21762) lo ha dimostrato: il punteggio anomalo era matematicamente corretto mentre i modelli di consenso accettavano il punteggio dichiarato dal fornitore. Qualsiasi implementazione in produzione di filtri basati sulla divergenza deve mantenere la capacità di deroga umana.

## 7.3 Confronto delle strategie di sintesi

S1 (voto di maggioranza) produce una copertura esaustiva ma può essere prolisso. È più appropriato quando la completezza ha la priorità sulla concisione.

S2 (centroide semantico) produce in modo affidabile la risposta più "media". Funziona meglio quando è necessaria una risposta rappresentativa e la domanda è ben vincolata.

S3 (LLM-as-Judge) produce la maggiore accuratezza fattuale nei domini A e B ma introduce una nuova dipendenza: i bias del modello giudice. L'utilizzo di un modello riservato come giudice mitiga questo rischio.

## 7.4 Limitazioni

**Dimensione del campione.** Con 45 prompt su tre domini, questo studio stabilisce prove iniziali ma non consente un'ampia generalizzazione statistica. Uno studio di follow-up con 100+ prompt per dominio rafforzerebbe sostanzialmente le affermazioni.

**Selezione dei modelli.** I dodici modelli rappresentano un campione di convenienza. La composizione dei modelli influisce sulla distribuzione del consenso. I lavori futuri dovrebbero variare sistematicamente la composizione dei modelli.

**Qualità delle risposte di riferimento.** Tre elementi sono stati segnalati come necessitanti di verifica manuale (discrepanza CVSS di A01, fonte BSI di A10, riferimento EDPB di B09).

**Validità temporale.** Le date limite di conoscenza degli LLM e le versioni dei modelli cambiano. Gli studi di replica devono documentare la versione del modello con precisione.

**Temperatura e campionamento.** La temperatura non è stata controllata tra i modelli. La replica con temperatura controllata isolerebbe questa variabile.

**La lunghezza dei token non è densità di informazione.** M4 (Gemini 2.5-pro) è stato sistematicamente il più prolisso senza una maggiore accuratezza fattuale.

## 7.5 Implicazioni per il dispiegamento dell'IA

1. **Consenso come portale di qualità.** Nei sistemi di IA ad alto rischio, uno strato di tipo BMAS può eseguire più modelli sulla stessa query e trattenere la risposta finché il consenso non raggiunge una soglia definita. La discordanza attiva la revisione umana invece di azioni automatiche.
2. **Instradamento per dominio.** Per le query fattuali con fonti autorevoli, un singolo modello ad alte prestazioni può essere sufficiente. L'overhead multi-modello è più giustificato per le query strategiche.
3. **Requisiti di diversità.** Le prestazioni di BMAS dipendono dalla diversità dei modelli. Due modelli simili dello stesso provider aggiungono meno informazioni rispetto a due di famiglie architetturali diverse.

## 7.6 Lavori futuri

- Studio di deriva temporale: eseguire gli stessi prompt ogni 6 mesi
- Espansione dei domini: diagnostica medica, analisi finanziaria, ragionamento giuridico
- Analisi di calibrazione: se la fiducia del modello correla con l'accordo di consenso
- Sintesi adattiva: selezione dinamica di S1, S2 o S3 in base alla convergenza misurata
- Valutazione umana: confrontare la qualità della sintesi BMAS con le risposte di esperti umani
