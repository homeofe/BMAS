# 5. Analiza dywergencji

## 5.1 Wyniki wykrywania wartości odstających

Na wszystkich 45 promptach 12 (44%) wygenerowało co najmniej jeden semantycznie odstający model zidentyfikowany przez DBSCAN (eps=0,15, min_samples=2). Częstość wartości odstających była najwyższa w dziedzinie C (strategicznej), co jest zgodne z oczekiwaniem, że niejednoznaczne pytania generują bardziej zróżnicowane embeddingi odpowiedzi.

**Tabela 3: Częstość wartości odstających według dziedziny**

| Dziedzina | Prompty z wartościami odstającymi | Łącznie promptów | Wskaźnik |
|---|---|---|---|
| Techniczna (A) | 5 | 10 | 50% |
| Regulacyjna (B) | 4 | 10 | 40% |
| Strategiczna (C) | 3 | 7 | 43% |

**Tabela 4: Wskaźnik wartości odstających według modelu (wszystkie prompty)**

| Model | Liczba anomalii | Wskaźnik anomalii |
|---|---|---|
| M1 (Sonnet) | 4 | 0,15 (15%) |
| M2 (Opus) | 4 | 0,15 (15%) |
| M3 (GPT-5.3) | 3 | 0,11 (11%) |
| M4 (Gemini-2.5) | 8 | 0,30 (30%) |
| M5 (Sonar) | 2 | 0,07 (7%) |

Gemini-2.5 (M4) miał najwyższy wskaźnik anomalii wynoszący 0,30, podczas gdy Sonar (M5) miał najniższy wynoszący 0,07. Wysoki wskaźnik anomalii dla konkretnego modelu niekoniecznie wskazuje na niższą jakość - może odzwierciedlać bardziej charakterystyczny styl odpowiedzi lub tendencję do bardziej wyczerpującego pokrycia, która oddala jego embedding od centroidu.

## 5.2 Korelacja dywergencja-halucynacja (Hipoteza H2)

Aby przetestować H2, porównaliśmy wyniki dokładności faktycznej między odpowiedziami modeli odstających i nieodstających dla promptów dziedzin A i B. Dokładność faktyczna była oceniana poprzez punktowanie każdej odpowiedzi względem pre-rejestrowanej listy kontrolnej ground truth dla każdego promptu.

> Uwaga: Szczegółowe wyniki H2 zawierające wyniki dokładności faktycznej wymagają ręcznej adnotacji ground truth, częściowo ukończonej przed uruchomieniem modeli (patrz sekcja 3.3.3). Pełne wyniki adnotacji są dostępne w uzupełniającym zbiorze danych.

Godny uwagi przypadek z danych pilotażowych (A01, punktacja CVSS): M1 podał 9,8 (matematycznie poprawne ze względu na wektor), podczas gdy modele konwergujące akceptowały 9,6 podane przez producenta. Wartość odstająca (M1) była faktycznie lepsza od konsensusu. Pokazuje to, że H2 musi być interpretowana ostrożnie: **status wartości odstającej jest sygnałem do ludzkiego przeglądu, nie wyrokiem o niepoprawności.**

## 5.3 Wzorce dywergencji według dziedziny

Dziedzina strategiczna (C) wykazała najwyższą dywergencję nie tylko we wskaźnikach podobieństwa semantycznego, ale i w cechach strukturalnych. Odpowiedzi na prompty dziedziny C różniły się w fundamentalnych rekomendacjach: różne modele preferowały różne architektury (mikroserwisy vs. monolit), różne priorytety migracji (TLS-first vs. podpisywanie kodu-first) i różne strategie inwestycyjne (certyfikacja vs. kontrole techniczne).

Ta różnorodność jest uzasadniona. W przeciwieństwie do promptów faktycznych, gdzie jedna odpowiedź jest poprawna, prompty strategiczne nie mają autorytatywnej ground truth. Framework BMAS traktuje to jako informatywny sygnał: gdy systemy eksperckie się nie zgadzają, sama niezgodność przemawia za ludzką deliberacją, a nie automatycznym podejmowaniem decyzji. Jest to szczególnie istotne w kontekście projektu AEGIS, gdzie decyzje architektoniczne dotyczące polskiego łącza eIDAS 2.0 wymagają eksperckiego osądu, a nie deterministycznej odpowiedzi jednego modelu.
