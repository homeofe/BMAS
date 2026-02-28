# 🎯 8. Conclusione

Questo lavoro ha presentato **Blind Multi-Agent Synthesis (BMAS)**, una metodologia per elicitare, confrontare e sintetizzare le risposte di più grandi modelli linguistici in rigoroso isolamento, e ha presentato risultati empirici di un esperimento con 540 esecuzioni su dodici LLM frontier e tre strati di dominio.

## 8.1 Riepilogo dei contributi

Abbiamo dimostrato che:

1. **La convergenza è dipendente dal dominio e misurabile.** Su 45 prompt, i domini A e B (tecnico e normativo) hanno mostrato sistematicamente una maggiore similarità semantica inter-modello rispetto al dominio C. [Vedi sezione 4 per i valori esatti.]

2. **La divergenza segnala l'errore nei domini fattuali.** I modelli identificati come valori anomali semantici hanno mostrato una minore accuratezza fattuale rispetto alle risposte di riferimento pre-registrate rispetto ai modelli non anomali, supportando l'ipotesi H2.

3. **La qualità della sintesi varia per strategia e dominio.** La sintesi LLM-as-Judge (S3) ha prodotto la maggiore accuratezza fattuale nei domini A e B, mentre il voto di maggioranza (S1) ha fornito la copertura più esaustiva. Nessuna strategia singola ha dominato su tutti i tipi di prompt.

4. **La lunghezza dei token non è un indicatore di qualità.** Abbiamo osservato una variazione significativa nel numero di token di risposta tra i modelli su prompt identici (fino a 6,5 volte per alcuni prompt), senza correlazione consistente con l'accuratezza fattuale.

## 8.2 Insegnamenti pratici

Per i professionisti che dispiegano LLM in ambienti regolamentati o ad alto rischio, BMAS suggerisce un'architettura pratica: eseguire i prompt su più provider di modelli indipendenti, misurare la convergenza semantica e instradare le risposte a bassa fiducia verso una revisione umana. Il protocollo di pre-registrazione è trasferibile a qualsiasi sforzo di valutazione multi-modello e previene i bias di conferma.

## 8.3 Relazione con AEGIS, AAHP e failprompt

BMAS è stato sviluppato nel contesto di AEGIS, un sistema di verifica dell'identità governativa transfrontaliera dell'UE che comprende connettori per diversi paesi europei, di AAHP (AI-to-AI Handoff Protocol), un framework strutturato di orchestrazione multi-agente per i pipeline di IA in produzione, e di failprompt, uno strumento CLI per la validazione delle risposte AI in ambienti CI/CD. Insieme, questi tre progetti formano un kit di strumenti integrato per il dispiegamento responsabile dell'IA multi-modello: AAHP fornisce lo strato di orchestrazione, failprompt il portale CI, e BMAS la base empirica per comprendere quando e perché il consenso multi-modello è più affidabile dell'output di un singolo modello.

Tutti i codici, i prompt, le risposte di riferimento pre-registrate e i risultati sperimentali sono pubblicati come dataset aperti che supportano la replica e l'estensione di questo lavoro.

---

*Il dataset BMAS, il runner, il pipeline di metriche e il codice di sintesi sono disponibili all'indirizzo: https://github.com/homeofe/BMAS*
