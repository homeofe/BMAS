# 1. Introduzione

I grandi modelli linguistici hanno raggiunto un livello di capacità tale da essere impiegati in domini dove la precisione non è opzionale: analisi giuridica, diagnostica medica, conformità normativa e sistemi di identità governativi. In questi domini, una risposta sicura ma errata di un singolo modello non è un inconveniente minore - è un fallimento con conseguenze reali.

L'approccio dominante per migliorare l'affidabilità degli LLM è o un miglior addestramento (RLHF, Constitutional AI) o un miglior prompting (catena di ragionamento, aumento tramite recupero). Entrambi operano all'interno di un paradigma a modello singolo: un modello, un output, una risposta di cui fidarsi o meno.

Questo lavoro adotta un approccio diverso. Invece di chiederci "come rendiamo un modello più affidabile", chiediamo: **cosa possiamo imparare dal disaccordo tra più modelli che non possono influenzarsi a vicenda?**

## 1.1 L'intuizione centrale

Quando cinque esperti indipendenti rispondono alla stessa domanda senza consultarsi, e quattro di loro danno la stessa risposta mentre uno ne dà una diversa, non concludiamo che i quattro abbiano torto. Esaminiamo la risposta dissidente con maggiore attenzione, ma ci fidiamo del consenso come punto di partenza.

Questo è il metodo Delphi, applicato dal 1963 alla previsione degli esperti. La sua forza è strutturale: **l'isolamento previene il pensiero di gruppo; il consenso emerge dal ragionamento indipendente, non dalla pressione sociale.**

BMAS applica questa logica agli LLM. Ogni modello è un esperto con una particolare distribuzione di addestramento, una soglia di conoscenza e un insieme di distorsioni. Quando vengono isolati l'uno dall'altro e viene loro posta la stessa domanda, la loro convergenza o divergenza è di per sé informativa.

## 1.2 Cosa c'è di nuovo

Diversi lavori precedenti sono correlati ma distinti:

**Self-Consistency** (Wang et al., 2022) genera più catene di ragionamento da un *singolo* modello e usa il voto di maggioranza. BMAS usa modelli *diversi* - questo testa attraverso le distribuzioni di addestramento, non solo la varianza di decodifica.

**Mixture of Agents** (Wang et al., 2024) permette ai modelli di vedere gli output degli altri in round di aggregazione. Ciò produce un raffinamento collaborativo, ma introduce il rischio di propagazione degli errori: se un modello produce un'allucinazione sicura nel primo round, i modelli successivi potrebbero ancorarsi ad essa.

**LLM-as-Judge** (Zheng et al., 2023) usa un modello per valutare un altro. BMAS usa un modello per *sintetizzare* gli output di più altri - il ruolo di giudice è limitato alla fase finale di sintesi.

BMAS è il primo framework a combinare quattro proprietà:
1. Rigoroso isolamento cieco (nessuna contaminazione incrociata)
2. Diversità dei modelli (provider, architetture, distribuzioni di addestramento diversi)
3. Analisi stratificata per dominio (fattuale, normativo, strategico)
4. Divergenza come segnale (non come fallimento)

## 1.3 Motivazione pratica

Questa ricerca è nata dall'esperienza operativa nella costruzione di AEGIS, un sistema di verifica dell'identità governativa transfrontaliera dell'UE, e di AAHP (AI-to-AI Handoff Protocol), un framework strutturato di orchestrazione multi-agente. In entrambi i sistemi, i pipeline multi-agente vengono utilizzati per decisioni architetturali, analisi di conformità e revisioni di implementazione.

È emersa una domanda pratica: quando si utilizzano più LLM come revisori indipendenti in un pipeline, quanto differiscono realmente i loro output? E quando differiscono, chi ha ragione?

BMAS è la risposta formale a quella domanda.

## 1.4 Contributi

Questo lavoro apporta:

1. **Metodologia BMAS:** Un protocollo formalizzato di sintesi cieca multi-agente con vincoli di isolamento, insieme di metriche e strategie di sintesi.
2. **Studio empirico:** Risultati di 45 prompt per 12 LLM in 3 strati di dominio, con risposte di riferimento pre-registrate per i domini A e B.
3. **Validazione dell'ipotesi divergenza-come-segnale:** Evidenza statistica che la divergenza tra modelli predice il tasso di errori fattuali.
4. **Confronto di strategie di sintesi:** Valutazione empirica del voto di maggioranza, del centroide semantico e della sintesi LLM-as-Judge rispetto alle risposte di riferimento.
5. **Dataset aperto:** Tutti i prompt, le risposte grezze dei modelli e gli indicatori di metriche pubblicati come benchmark pubblico.

## 1.5 Struttura dell'articolo

La sezione 2 esamina i lavori correlati. La sezione 3 descrive la metodologia BMAS e il disegno sperimentale. La sezione 4 presenta i risultati. La sezione 5 analizza le correlazioni divergenza-allucinazione. La sezione 6 valuta le strategie di sintesi. La sezione 7 discute implicazioni, limitazioni e lavori futuri. La sezione 8 conclude.
