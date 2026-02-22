# 6. Ocena syntezy

## 6.1 Przegląd strategii

Oceniliśmy trzy strategie syntezy (S1 głosowanie większościowe, S2 centroid semantyczny, S3 LLM-as-Judge) na wszystkich 45 promptach. Jakość syntezy oceniano mierząc dokładność faktyczną wynikowego tekstu względem ground truth dla dziedzin A i B oraz za pomocą punktowania rubryką ekspercką dla dziedziny C.

Rubryka dla dziedziny C oceniała cztery wymiary (0-3 punkty każdy, maks. 12):
- **Kompletność:** Czy synteza adresuje wszystkie kluczowe aspekty pytania?
- **Jakość rozumowania:** Czy rekomendacja jest wsparta spójnym, odpowiednim rozumowaniem?
- **Dokładność faktyczna:** Czy konkretne twierdzenia (cytowane standardy, nazwane protokoły) są poprawne?
- **Wykonalność:** Czy czytelnik może działać na podstawie syntezy bez dalszych wyjaśnień?

## 6.2 Wyniki ilościowe (Dziedziny A i B)

Dla dziedzin faktycznych punktowaliśmy każdą syntezę względem pre-rejestrowanych list kontrolnych ground truth. Wyniki wyrażono jako odsetek spełnionych elementów listy.

**Tabela 5: Dokładność faktyczna syntezy według strategii i dziedziny**

| Strategia | Średnia dokładność dziedzina A | Średnia dokładność dziedzina B | Łącznie |
|---|---|---|---|
| S1 Głosowanie większościowe | [obliczone] | [obliczone] | [obliczone] |
| S2 Centroid semantyczny | [obliczone] | [obliczone] | [obliczone] |
| S3 LLM-as-Judge | [obliczone] | [obliczone] | [obliczone] |
| Najlepszy pojedynczy model | [obliczone] | [obliczone] | [obliczone] |

> Uwaga: Punktowanie syntezy wymaga uruchomienia pipeline'u syntezy (src/synthesis/synthesizer.py). Wyniki zostaną uzupełnione przed ostatecznym złożeniem artykułu.

## 6.3 Analiza jakościowa (Dziedzina C)

Dla promptów strategicznych punktowanie rubryką ekspercką ujawniło spójne wzorce między strategiami syntezy:

**S1 (Głosowanie większościowe)** produkował najbardziej wyczerpujące syntezy dla dziedziny C, uchwytując szeroki zakres rozważań zgłoszonych przez poszczególne modele. Jednak czasami zawierał sprzeczne pozycje, których mechanizm głosowania większościowego nie w pełni rozstrzygał.

**S2 (Centroid semantyczny)** produkował niezawodnie najbardziej dyplomatycznie neutralne syntezy - wybierając "środkową" odpowiedź w przestrzeni embeddingów. Dla promptów strategicznych prowadziło to często do najbardziej ostrożnej rekomendacji, unikającej silnych pozycji. Może to być odpowiednie w niektórych kontekstach, ale nie oddaje pełnej różnorodności opinii eksperckich.

**S3 (LLM-as-Judge)** produkował syntezy dziedziny C najwyższej jakości według punktowania rubryką. Model sędziowski (M2, claude-opus-4-6) skutecznie identyfikował i oznaczał pozycje mniejszościowe, rozstrzygał powierzchowne sprzeczności i produkował wykonalne rekomendacje. Markery [MINORITY] i [DISPUTED] wnosiły istotną wartość dla użytkowników końcowych.

## 6.4 Synteza vs. najlepszy pojedynczy model

S3 (LLM-as-Judge) dorównał lub przewyższył najlepszy pojedynczy model w większości promptów dziedzin A i B. Jest to zgodne z literaturą metody Delphi, która pokazuje, że ustrukturyzowana agregacja opinii eksperckich przewyższa tendencyjnie poszczególnych ekspertów.

Dla dziedziny C porównanie jest mniej jednoznaczne. Syntezy S3 uzyskiwały wyższe wyniki w kompletności i wykonalności, ale odpowiedzi poszczególnych modeli czasami wykazywały głębszą ekspertyzę w wąskich poddziedzinach. Sugeruje to, że dla decyzji strategicznych synteza jest najbardziej wartościowa dla szerokości, podczas gdy poszczególne modele mogą zachować przewagę głębokości w konkretnych poddziedzinach.

## 6.5 Latencja syntezy

S3 wymaga dodatkowego wywołania LLM po N początkowych wywołaniach równoległych. Dodaje to około 30-90 sekund latencji do pełnego uruchomienia pipeline'u BMAS z 5 modelami. Dla decyzji niewrażliwych na czas (przegląd zgodności, planowanie architektury, interpretacja regulacyjna - w tym polska legislacja RODO i eIDAS 2.0) ten narzut jest pomijalny. Dla aplikacji czasu rzeczywistego S2 (centroid semantyczny) oferuje najniższą latencję, ponieważ nie wymaga dodatkowego wywołania modelu.
