# 3. Metodologia

## 3.1 Panoramica del protocollo BMAS

Blind Multi-Agent Synthesis (BMAS) e un protocollo in quattro fasi per elicitare, confrontare e sintetizzare le risposte di piu LLM su prompt identici:

1. **Elicitazione cieca** - Ogni modello riceve lo stesso prompt senza conoscenza dello studio, di altri modelli o di altre risposte.
2. **Calcolo delle metriche** - Similarita semantica per coppie, accuratezza fattuale e rilevamento di valori anomali vengono calcolati su tutte le risposte.
3. **Sintesi** - Tre strategie di sintesi aggregano le risposte individuali in un unico output.
4. **Valutazione** - Gli output di sintesi vengono valutati rispetto alle risposte di riferimento pre-registrate (domini A e B) o alla valutazione di esperti (dominio C).

Il protocollo impone una rigorosa **regola di non contaminazione**: nessuna risposta di un modello viene resa disponibile a nessun altro modello in nessuna fase precedente alla sintesi.

## 3.2 Modelli

Valutiamo cinque LLM all'avanguardia di quattro provider distinti:

| ID | Modello | Provider | Finestra di contesto |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M token |
| M2 | claude-opus-4-6 | Anthropic | 1M token |
| M3 | gpt-5.3-codex | OpenAI | 272k token |
| M4 | gemini-2.5-pro | Google | 1M token |
| M5 | sonar-pro | Perplexity | 127k token |

La diversita multi-provider e deliberata. I modelli dello stesso provider condividono lignaggio architetturale e pipeline di dati di addestramento, il che puo ridurre la divergenza anche in condizioni cieche.

**Implementazione dell'isolamento:** Ogni modello viene eseguito in una sessione isolata separata senza contesto condiviso. Il system prompt e identico per tutti i modelli:

> *"Sei un assistente esperto competente. Rispondi alla seguente domanda nel modo piu accurato e completo possibile. Sii preciso, fattuale e strutturato. Se non sei certo di qualche dettaglio specifico, indicalo esplicitamente."*

La temperatura non viene modificata. Preserviamo deliberatamente il comportamento di campionamento predefinito di ciascun modello per catturare la varianza naturale delle risposte.

## 3.3 Progettazione dei prompt

### 3.3.1 Struttura dei domini

Costruiamo 30 prompt su tre strati di dominio:

**Dominio A - Tecnico ad alta precisione (A01-A10):** Domande con risposte oggettivamente corrette verificabili rispetto a fonti primarie autorevoli (standard NIST FIPS, NVD, RFC IETF, specifiche OpenID Foundation). Esempi: giustificazione del punteggio CVSS, dimensioni delle chiavi degli algoritmi PQC, enumerazione delle suite di cifratura TLS 1.3.

**Dominio B - Normativo/Conformita (B01-B10):** Domande basate su testo legale e normativo con fonti autorevoli (GDPR, eIDAS 2.0, NIS2, ISO 27001, BSI C5). Le risposte centrali sono definite in testo formale. Esempi: eccezioni di cancellazione dell'Articolo 17(3) del GDPR, classificazioni settoriali NIS2, differenze di livello di valutazione TISAX.

**Dominio C - Strategico/Ambiguo (C01-C10):** Domande senza una risposta unica corretta che richiedono giudizio esperto e ragionamento architetturale. Esistono molteplici posizioni difendibili. Esempi: decisioni di architettura zero-trust, priorizzazione della migrazione PQC, compromessi di investimento nella conformita.

### 3.3.2 Requisiti dei prompt

Tutti i prompt soddisfano quattro criteri:
1. **Autonomi** - rispondibili senza contesto esterno o recupero di documenti
2. **Risposta strutturata** - ogni prompt specifica il formato di output richiesto
3. **Lunghezza limitata** - risposta attesa di 300-600 token per i domini A-B; 400-800 per il dominio C
4. **Verificabili** - per i domini A e B esiste una risposta verificabile

### 3.3.3 Pre-registrazione

Seguendo le migliori pratiche della scienza aperta, le risposte di riferimento per i domini A e B sono state documentate e bloccate prima di qualsiasi esecuzione dei modelli. Questo impedisce il bias di conferma inconscio nel punteggio.

## 3.4 Metriche

### 3.4.1 Similarita semantica (primaria)

Calcoliamo la similarita coseno per coppie tra embedding di risposta usando il modello sentence-transformer `all-mpnet-base-v2`. Per N modelli, questo produce una matrice di similarita N x N per prompt. Riportiamo:
- **Similarita media per coppie (MPS):** media di tutti gli N(N-1)/2 punteggi per coppie
- **Similarita minima per coppie:** la coppia piu divergente
- **Deviazione standard della similarita:** varianza all'interno del cluster di risposte del prompt

### 3.4.2 BERTScore

Calcoliamo BERTScore F1 per coppie come misura secondaria di similarita semantica a livello di token. BERTScore cattura la prossimita lessicale oltre gli embedding a livello di frase.

### 3.4.3 Jaccard sulle affermazioni chiave

Estraiamo affermazioni fattuali discrete da ciascuna risposta usando la segmentazione in frasi e calcoliamo la similarita Jaccard per coppie su insiemi di affermazioni normalizzati. Questa metrica cattura l'accordo strutturale.

### 3.4.4 Rilevamento dei valori anomali

Applichiamo DBSCAN con eps=0.15 e min_samples=2. I modelli i cui embedding cadono al di fuori di tutti i cluster di vicinato ricevono un'etichetta di valore anomalo (-1). Trattiamo lo stato di valore anomalo come segnale di potenziale allucinazione nei domini A e B.

### 3.4.5 Accuratezza fattuale (solo domini A e B)

Per ogni risposta dei domini A e B, valutiamo l'accuratezza fattuale rispetto alla lista di controllo delle risposte di riferimento pre-registrate. Il punteggio di accuratezza fattuale e la frazione di elementi della lista soddisfatti.

## 3.5 Strategie di sintesi

**S1 - Voto di maggioranza (livello di affermazione):** Le affermazioni fattuali vengono accettate se appaiono nelle risposte di almeno il 60% dei modelli. Le affermazioni di minoranza vengono aggiunte con un marcatore [MINORITY].

**S2 - Centroide semantico:** La risposta il cui embedding e piu vicino alla media di tutti gli embedding viene selezionata come base di sintesi. Non viene aggiunto nuovo contenuto.

**S3 - LLM-as-Judge:** Le cinque risposte anonimizzate vengono presentate a una sesta istanza del modello (M2, claude-opus-4-6) con l'istruzione di produrre una sintesi autorevole unica, marcando le affermazioni di minoranza ([MINORITY]) e le contraddizioni ([DISPUTED]).

## 3.6 Ipotesi

**H1 (Convergenza nei domini fattuali):** La similarita semantica media per coppie per i prompt dei domini A e B supera 0.75 (BERTScore F1).

**H2 (La divergenza segnala errore):** Tra le risposte dei domini A e B, i modelli anomali (etichetta DBSCAN -1) avranno punteggi di accuratezza fattuale significativamente piu bassi rispetto ai modelli non anomali (t-test unilaterale, alfa=0.05).

**H3 (Effetto del dominio sulla convergenza):** La similarita media per coppie per il dominio C sara significativamente inferiore a quella per i domini A e B (ANOVA a una via, Tukey HSD post-hoc, alfa=0.05).

## 3.7 Configurazione sperimentale

Tutte le esecuzioni dei modelli sono state effettuate tramite il gateway OpenClaw, che instrada indipendentemente all'API di ciascun provider. Il dataset completo di 150 esecuzioni (30 prompt x 5 modelli) e pubblicato insieme a questo lavoro.
