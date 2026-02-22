# 7. Dyskusja

## 7.1 Interpretacja konwergencji i dywergencji

Centralna teza BMAS glosi, ze konwergencja miedzymodelowa jest informacyjna: nie tylko jako wlasciwosc statystyczna eksperymentu, ale jako praktyczny sygnal dla zastosowan w dalszym etapie lancucha. Nasze wyniki [patrz sekcja 4] wspieraja te teze dla dziedzin faktycznych, ujawniajac jednoczesnie wazne niuanse.

Wysoka konwergencja w dziedzinach A i B potwierdza intuicje, ze dobrze skalibrowane modele wytrenowane na tych samych autorytatywnych zrodlach zmierzaja ku tym samym prawidlowym odpowiedziom, gdy pytania sa jednoznaczne. Niska konwergencja w dziedzinie C odzwierciedla rzeczywista trudnosc epistemiczna pytan. Gdy piec niezaleznych systemow eksperckich nie zgadza sie co do optymalnych decyzji architektonicznych, sama niezgodnosc jest znaczaca: sygnalizuje, ze pytanie nie ma dominujacej prawidlowej odpowiedzi i wymaga ludzkiej deliberacji. BMAS pełni zatem role **wyroczni zlozonosci** obok sygnalu jakosci.

## 7.2 Zwiazek dywergencji z halucynacja

Nasza analiza wartosci odstajacych dostarcza wstepnych dowodow, ze modele zidentyfikowane jako odstajace w przestrzeni embeddingowej maja tendencje do nizszych wynikow dokladnosci faktycznej. System produkcyjny implementujacy monitorowanie w stylu BMAS moze oznaczac odpowiedzi znaczaco odbiegajace od klastra konsensusu do przegladu ludzkiego.

Zastrzegamy jednak, ze korelacja nie jest przyczynowoscia. Odpowiedz odstajaca moze byc prawidlowa, podczas gdy konsensus jest bledny. Odpowiedz M1 na pytanie A01 (punktacja CVSS dla CVE-2024-21762) to potwierdzila: wynik odstajacy byl matematycznie poprawny, podczas gdy modele konsensusu akceptowaly wynik deklarowany przez producenta. Kazda produkcyjna implementacja filtrowania opartego na dywergencji musi zachowac mozliwosc ludzkiej nadrzednosci decyzji.

## 7.3 Porownanie strategii syntezy

S1 (glosowanie wiekszosciowe) produkuje wyczerpujace pokrycie, lecz moze byc gadatliwa. Jest najbardziej odpowiednia, gdy kompletnosc ma pierwszenstwo przed zwiezloscia.

S2 (centroid semantyczny) niezawodnie produkuje najbardziej "przecietna" odpowiedz. Sprawdza sie najlepiej, gdy potrzebna jest reprezentatywna pojedyncza odpowiedz, a pytanie jest dobrze zdefiniowane.

S3 (LLM-as-Judge) produkuje najwyzsza dokladnosc faktyczna w dziedzinach A i B, lecz wprowadza nowa zaleznosc: wlasne uprzedzenia modelu sedziego. Uzycie zarezerwowanego modelu jako sedziego lagodzi to ryzyko.

## 7.4 Ograniczenia

**Wielkosc probki.** Przy 30 promptach w trzech dziedzinach badanie to ustanawia poczatkowe dowody, lecz nie pozwala na szeroka generalizacje statystyczna. Badanie uzupelniajace ze 100+ promptami na dziedzine znaczaco wzmocniloby twierdzenia.

**Dobor modeli.** Piec modeli stanowi probe wygodna. Sklad modeli wplywa na rozklad konsensusu. Przyszle prace powinny systematycznie zmieniac sklad modeli.

**Jakosc odpowiedzi referencyjnych.** Trzy elementy zostaly oznaczone jako wymagajace recznej weryfikacji (rozbiez nosc CVSS w A01, zrodlo BSI w A10, numer wytycznej EDPB w B09).

**Waznosc czasowa.** Daty granicze wiedzy LLM i wersje modeli ulegaja zmianom. Badania replikacyjne powinny precyzyjnie dokumentowac wersje modeli.

**Temperatura i probkowanie.** Temperatura nie byla kontrolowana miedzy modelami. Replikacja z kontrolowana temperatura izolowałaby te zmienna.

**Dlugosc tokenow nie jest gestoscia informacji.** M4 (Gemini 2.5-pro) byl systematycznie najbardziej gadatliwy bez wyzszej dokladnosci faktycznej.

## 7.5 Implikacje dla wdrazania AI

1. **Konsensus jako brama jakosci.** W systemach AI wysokiego ryzyka warstwa w stylu BMAS moze uruchamiac wiele modeli na tym samym zapytaniu i wstrzymywac odpowiedz do czasu, az konsensus osiagnie zdefiniowany prog. Niezgodnosc wyzwala przeglad ludzki zamiast automatycznych dzialan.
2. **Routing wedlug dziedziny.** Dla zapytan faktycznych z autorytatywnymi zrodlami pojedynczy wysokowydajny model moze byc wystarczajacy. Naklad wielomodelowy jest najbardziej uzasadniony dla zapytan strategicznych.
3. **Wymogi roznorodnosci.** Wydajnosc BMAS zalezy od roznorodnosci modeli. Dwa bardzo podobne modele tego samego dostawcy wnosza mniej informacji niz dwa z roznych rodzin architektonicznych.

## 7.6 Przyszle prace

- Badanie dryftu czasowego: uruchamianie tych samych promptow co 6 miesiecy
- Rozszerzenie dziedzin: diagnostyka medyczna, analiza finansowa, rozumowanie prawnicze
- Analiza kalibracji: czy pewnosc modelu koreluje z zgodnoscia konsensusu
- Adaptacyjna synteza: dynamiczny wybor S1, S2 lub S3 na podstawie mierzonej konwergencji
- Ocena ludzka: porownanie jakosci syntezy BMAS z odpowiedziami ludzkich ekspertow

## 7.7 Uwaga dotyczaca projektu AEGIS

Wyniki BMAS maja bezposrednie zastosowanie w projekcie AEGIS - transgranicznym systemie weryfikacji tozsamosci rzadowej UE obejmujacym lacza dla Niemiec, Austrii, Szwajcarii, Polski i Francji. W kontekscie AEGIS wielomodelowa walidacja odpowiedzi jest kluczowa dla zapewnienia zgodnosci z roznymi krajowymi wymaganiami regulacyjnymi (RODO, eIDAS 2.0, BSI C5, TISAX) bez polegania na pojedynczym modelu jako jedynym interpretatorem ram prawnych.
