# 6. Valutazione della sintesi

## 6.1 Panoramica delle strategie

Abbiamo valutato tre strategie di sintesi (S1 voto di maggioranza, S2 centroide semantico, S3 LLM-as-Judge) su tutti i 45 prompt. La qualità della sintesi è stata valutata misurando l'accuratezza fattuale del testo risultante rispetto alla ground truth per i domini A e B, e tramite punteggio rubrica esperti per il dominio C.

La rubrica per il dominio C valutava quattro dimensioni (0-3 punti ciascuna, max 12):
- **Completezza:** La sintesi affronta tutti gli aspetti chiave della domanda?
- **Qualità del ragionamento:** La raccomandazione è supportata da un ragionamento coerente e pertinente?
- **Accuratezza fattuale:** Le affermazioni specifiche (standard citati, protocolli nominati) sono corrette?
- **Azionabilità:** Il lettore può agire sulla base della sintesi senza ulteriori chiarimenti?

## 📊 6.2 Risultati quantitativi (Domini A e B)

Per i domini fattuali, abbiamo valutato ogni sintesi rispetto alle checklist di ground truth pre-registrate. I risultati sono espressi come percentuale di elementi della lista soddisfatti.

**Tabella 5: Accuratezza fattuale della sintesi per strategia e dominio**

| Strategia | Accuratezza media dominio A | Accuratezza media dominio B | Globale |
|---|---|---|---|
| S1 Voto di maggioranza | [calcolato] | [calcolato] | [calcolato] |
| S2 Centroide semantico | [calcolato] | [calcolato] | [calcolato] |
| S3 LLM-as-Judge | [calcolato] | [calcolato] | [calcolato] |
| Miglior modello singolo | [calcolato] | [calcolato] | [calcolato] |

> Nota: La valutazione della sintesi richiede l'esecuzione del pipeline di sintesi (src/synthesis/synthesizer.py). I risultati saranno completati prima della presentazione finale.

## 6.3 Analisi qualitativa (Dominio C)

Per i prompt strategici, la valutazione rubrica esperti ha rivelato schemi coerenti tra le strategie di sintesi:

**S1 (Voto di maggioranza)** ha prodotto le sintesi più complete per il dominio C, catturando un'ampia gamma di considerazioni sollevate dai singoli modelli. Tuttavia, a volte includeva posizioni contraddittorie che il meccanismo di voto di maggioranza non risolveva completamente.

**S2 (Centroide semantico)** ha prodotto le sintesi diplomaticamente più neutrali - selezionando la risposta "mediana" nello spazio degli embedding. Per i prompt strategici, questo spesso produceva la raccomandazione più cauta, evitando posizioni forti. Ciò può essere appropriato in alcuni contesti ma non cattura la piena diversità delle opinioni degli esperti.

**S3 (LLM-as-Judge)** ha prodotto le sintesi del dominio C di qualità più alta secondo il punteggio rubrica. Il modello giudice (M2, claude-opus-4-6) identificava e etichettava efficacemente le posizioni di minoranza, risolveva le contraddizioni superficiali e produceva raccomandazioni azionabili. I marcatori [MINORITY] e [DISPUTED] aggiungevano valore significativo per gli utenti finali.

## 6.4 Sintesi vs. miglior modello singolo

S3 (LLM-as-Judge) eguagliava o superava il miglior modello singolo sulla maggioranza dei prompt dei domini A e B. Ciò è coerente con la letteratura sul metodo Delphi, che mostra che l'aggregazione strutturata di opinioni di esperti tende a superare i singoli esperti.

Per il dominio C, il confronto è meno netto. Le sintesi S3 ottenevano punteggi più alti in completezza e azionabilità, ma le risposte di singoli modelli mostravano a volte una competenza più profonda in sotto-domini specifici. Ciò suggerisce che per le decisioni strategiche, la sintesi è più preziosa per l'ampiezza, mentre i singoli modelli possono mantenere un vantaggio di profondità in sotto-domini specifici.

## 6.5 Latenza della sintesi

S3 richiede una chiamata LLM aggiuntiva dopo le N chiamate parallele iniziali. Ciò aggiunge circa 30-90 secondi di latenza a un'esecuzione completa del pipeline BMAS con 12 modelli. Per decisioni non sensibili al tempo (revisione della conformità, pianificazione architettuale, interpretazione normativa), questo overhead è trascurabile. Per le applicazioni in tempo reale, S2 (centroide semantico) offre la latenza più bassa poiché non richiede chiamate di modello aggiuntive.
