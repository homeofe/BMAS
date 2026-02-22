# 2. Lavori correlati

BMAS si basa su metodi di consenso esperto strutturato, tecniche LLM multi-campione e multi-modello, metriche di valutazione automatizzata e clustering basato sulla densita. Questa sezione esamina ciascuna area e chiarisce il posizionamento di BMAS rispetto ai lavori precedenti.

## 2.1 Il metodo Delphi

Dalkey e Helmer (1963) introdussero il metodo Delphi alla RAND Corporation come approccio strutturato alla previsione degli esperti. Nel protocollo originale, un panel di esperti forniva stime indipendenti senza conoscere le risposte degli altri, e un facilitatore aggregava i risultati in piu round iterativi. La forza centrale del metodo era che l'isolamento preveniva l'ancoraggio e il pensiero di gruppo, consentendo ai genuini disaccordi di emergere prima che venisse ricercato il consenso. BMAS prende in prestito questo principio di isolamento direttamente: ogni LLM risponde ai prompt senza osservare gli output di nessun altro modello, garantendo che la convergenza, quando si verifica, rifletta un ragionamento indipendente piuttosto che imitazione.

## 2.2 Self-Consistency

Wang et al. (2022) proposero la self-consistency come strategia di decodifica che campiona piu catene di ragionamento da un unico modello linguistico e seleziona la risposta finale per voto di maggioranza. Il metodo dimostro miglioramenti significativi su benchmark di ragionamento aritmetico e di senso comune. Tuttavia, poiche tutte le catene di ragionamento provengono dallo stesso modello, la self-consistency cattura solo la varianza di decodifica intra-modello, non le differenze piu profonde nei dati di addestramento, nell'architettura e nell'allineamento che distinguono provider separati. BMAS estende l'intuizione di convergenza-come-segnale-di-qualita al contesto multi-provider.

## 2.3 Mixture of Agents

Wang et al. (2024) introdussero il framework Mixture-of-Agents (MoA), in cui piu LLM partecipano a round di aggregazione iterativi dove ogni modello puo osservare e raffinare gli output degli altri. MoA dimostro che il raffinamento collaborativo migliorava le prestazioni su benchmark come AlpacaEval e MT-Bench. La differenza critica con BMAS e che MoA non e cieco: i modelli nei round successivi sono esposti agli output precedenti, introducendo il rischio di propagazione degli errori. BMAS evita deliberatamente cio imponendo un rigoroso isolamento durante la fase di risposta e differendo qualsiasi interazione tra modelli a una fase di sintesi separata.

## 2.4 LLM-as-Judge

Zheng et al. (2023) studiarono l'uso di grandi modelli linguistici come valutatori degli output di altri modelli, introducendo i benchmark MT-Bench e Chatbot Arena. Il loro lavoro mostro che gli LLM potenti potevano fungere da proxy scalabili per la valutazione umana. In BMAS, il ruolo di giudice e limitato a una delle tre strategie di sintesi (S3): un sesto modello sintetizza le cinque risposte cieche in un unico output, ma la correttezza e misurata rispetto alle risposte di riferimento pre-registrate, non rispetto alle preferenze del giudice.

## 2.5 BERTScore

Zhang et al. (2020) proposero BERTScore, una metrica di valutazione automatica che calcola la similarita a livello di token tra testi candidato e di riferimento usando embedding contestuali di modelli transformer pre-addestrati. A differenza delle metriche di sovrapposizione di n-grammi come BLEU o ROUGE, BERTScore cattura l'equivalenza semantica attraverso diverse forme superficiali ed e robusta alla parafrasi. BMAS adotta BERTScore F1 come metrica primaria di similarita per coppie per misurare la convergenza inter-modello.

## 2.6 Constitutional AI

Bai et al. (2022) introdussero Constitutional AI (CAI) ad Anthropic, una metodologia di addestramento in cui un modello critica e rivede i propri output secondo un insieme di principi. BMAS puo essere visto come l'estensione dell'intuizione critica-e-revisione da un ciclo a singolo modello a un contesto multi-modello e multi-provider: invece di un modello che giudica se stesso, piu modelli addestrati indipendentemente fungono da critici impliciti l'uno dell'altro attraverso il segnale di divergenza.

## 2.7 DBSCAN

Ester et al. (1996) proposero DBSCAN (Density-Based Spatial Clustering of Applications with Noise), un algoritmo di clustering che raggruppa i punti dati in base alla connettivita di densita e identifica i punti in regioni a bassa densita come rumore o valori anomali. A differenza del k-means, DBSCAN non richiede di specificare a priori il numero di cluster. BMAS impiega DBSCAN sullo spazio degli embedding delle risposte dei modelli per rilevare output anomali.

## 2.8 Posizionamento

BMAS e, a nostra conoscenza, il primo framework a combinare quattro proprieta assenti da qualsiasi approccio precedente singolo. In primo luogo, impone l'isolamento cieco tra provider. In secondo luogo, introduce l'analisi stratificata per dominio. In terzo luogo, tratta la divergenza come segnale di anomalia piuttosto che come fallimento di coordinamento. In quarto luogo, fornisce un confronto controllato delle strategie di sintesi valutate rispetto a risposte di riferimento pre-registrate, offrendo una guida empirica su come aggregare al meglio gli output dei modelli indipendenti nella pratica.
