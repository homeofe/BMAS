# 7. Dyskusja

## 7.1 Interpretacja konwergencji i dywergencji

Centralna teza BMAS głosi, że konwergencja międzymodelowa jest informacyjna: nie tylko jako właściwość statystyczna eksperymentu, ale jako praktyczny sygnał dla zastosowań w dalszym etapie łańcucha. Nasze wyniki [patrz sekcja 4] wspierają tę tezę dla dziedzin faktycznych, ujawniając jednocześnie ważne niuanse.

Wysoka konwergencja w dziedzinach A i B potwierdza intuicję, że dobrze skalibrowane modele wytrenowane na tych samych autorytatywnych źródłach zmierzają ku tym samym prawidłowym odpowiedziom, gdy pytania są jednoznaczne. Niska konwergencja w dziedzinie C odzwierciedla rzeczywistą trudność epistemiczną pytań. Gdy dwanaście niezależnych systemów eksperckich nie zgadza się co do optymalnych decyzji architektonicznych, sama niezgodność jest znacząca: sygnalizuje, że pytanie nie ma dominującej prawidłowej odpowiedzi i wymaga ludzkiej deliberacji. BMAS pełni zatem rolę **wyroczni złożoności** obok sygnału jakości.

## 7.2 Związek dywergencji z halucynacją

Nasza analiza wartości odstających dostarcza wstępnych dowodów, że modele zidentyfikowane jako odstające w przestrzeni embeddingowej mają tendencję do niższych wyników dokładności faktycznej. System produkcyjny implementujący monitorowanie w stylu BMAS może oznaczać odpowiedzi znacząco odbiegające od klastra konsensusu do przeglądu ludzkiego.

Zastrzegamy jednak, że korelacja nie jest przyczynowością. Odpowiedź odstająca może być prawidłowa, podczas gdy konsensus jest błędny. Odpowiedź M1 na pytanie A01 (punktacja CVSS dla CVE-2024-21762) to potwierdziła: wynik odstający był matematycznie poprawny, podczas gdy modele konsensusu akceptowały wynik deklarowany przez producenta. Każda produkcyjna implementacja filtrowania opartego na dywergencji musi zachować możliwość ludzkiej nadrzędności decyzji.

## 7.3 Porównanie strategii syntezy

S1 (głosowanie większościowe) produkuje wyczerpujące pokrycie, lecz może być gadatliwa. Jest najbardziej odpowiednia, gdy kompletność ma pierwszeństwo przed zwięzłością.

S2 (centroid semantyczny) niezawodnie produkuje najbardziej "przeciętną" odpowiedź. Sprawdza się najlepiej, gdy potrzebna jest reprezentatywna pojedyncza odpowiedź, a pytanie jest dobrze zdefiniowane.

S3 (LLM-as-Judge) produkuje najwyższą dokładność faktyczną w dziedzinach A i B, lecz wprowadza nową zależność: własne uprzedzenia modelu sędziego. Użycie zarezerwowanego modelu jako sędziego łagodzi to ryzyko.

## 7.4 Ograniczenia

**Wielkość próbki.** Przy 45 promptach w trzech dziedzinach badanie to ustanawia początkowe dowody, lecz nie pozwala na szeroką generalizację statystyczną. Badanie uzupełniające ze 100+ promptami na dziedzinę znacząco wzmocniłoby twierdzenia.

**Dobór modeli.** Dwanaście modeli stanowi próbę wygodną. Skład modeli wpływa na rozkład konsensusu. Przyszłe prace powinny systematycznie zmieniać skład modeli.

**Jakość odpowiedzi referencyjnych.** Trzy elementy zostały oznaczone jako wymagające ręcznej weryfikacji (rozbieżność CVSS w A01, źródło BSI w A10, numer wytycznej EDPB w B09).

**Ważność czasowa.** Daty graniczne wiedzy LLM i wersje modeli ulegają zmianom. Badania replikacyjne powinny precyzyjnie dokumentować wersje modeli.

**Temperatura i próbkowanie.** Temperatura nie była kontrolowana między modelami. Replikacja z kontrolowaną temperaturą izolowałaby tę zmienną.

**Długość tokenów nie jest gęstością informacji.** M4 (Gemini 2.5-pro) był systematycznie najbardziej gadatliwy bez wyższej dokładności faktycznej.

## 7.5 Implikacje dla wdrażania AI

1. **Konsensus jako brama jakości.** W systemach AI wysokiego ryzyka warstwa w stylu BMAS może uruchamiać wiele modeli na tym samym zapytaniu i wstrzymywać odpowiedź do czasu, aż konsensus osiągnie zdefiniowany próg. Niezgodność wyzwala przegląd ludzki zamiast automatycznych działań.
2. **Routing według dziedziny.** Dla zapytań faktycznych z autorytatywnymi źródłami pojedynczy wysokowydajny model może być wystarczający. Nakład wielomodelowy jest najbardziej uzasadniony dla zapytań strategicznych.
3. **Wymogi różnorodności.** Wydajność BMAS zależy od różnorodności modeli. Dwa bardzo podobne modele tego samego dostawcy wnoszą mniej informacji niż dwa z różnych rodzin architektonicznych.

## 7.6 Przyszłe prace

- Badanie dryftu czasowego: uruchamianie tych samych promptów co 6 miesięcy
- Rozszerzenie dziedzin: diagnostyka medyczna, analiza finansowa, rozumowanie prawnicze
- Analiza kalibracji: czy pewność modelu koreluje z zgodnością konsensusu
- Adaptacyjna synteza: dynamiczny wybór S1, S2 lub S3 na podstawie mierzonej konwergencji
- Ocena ludzka: porównanie jakości syntezy BMAS z odpowiedziami ludzkich ekspertów

## 7.7 Uwaga dotycząca projektu AEGIS

Wyniki BMAS mają bezpośrednie zastosowanie w projekcie AEGIS - transgranicznym systemie weryfikacji tożsamości rządowej UE obejmującym łącza dla Niemiec, Austrii, Szwajcarii, Polski i Francji. W kontekście AEGIS wielomodelowa walidacja odpowiedzi jest kluczowa dla zapewnienia zgodności z różnymi krajowymi wymaganiami regulacyjnymi (RODO, eIDAS 2.0, BSI C5, TISAX) bez polegania na pojedynczym modelu jako jedynym interpretatorem ram prawnych.
