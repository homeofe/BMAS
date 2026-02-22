# 8. Wnioski

Niniejsza praca przedstawila **Blind Multi-Agent Synthesis (BMAS)**, metodologie elicytacji, porownania i syntezy odpowiedzi wielu duzych modeli jezykowych w scislej izolacji, oraz zaprezentowala wyniki empiryczne eksperymentu 150 uruchomien na pieciu LLM frontier i trzech warstwach dziedzinowych.

## 8.1 Podsumowanie wkladu naukowego

Wykazalismy, ze:

1. **Konwergencja jest zalezna od dziedziny i mierzalna.** Dla 30 promptow dziedziny A i B (techniczna i regulacyjna) wykazaly systematycznie wyzsza semantyczna zgodnosc miedzymodelowa niz dziedzina C (prompty strategiczne i niejednoznaczne). [Patrz sekcja 4 dla dokladnych wartosci.]

2. **Dywergencja sygnalizuje blad w dziedzinach faktycznych.** Modele zidentyfikowane jako semantyczne wartosci odstajace wykazaly nizsza dokladnosc faktyczna wzgledem pre-rejestrowanych odpowiedzi referencyjnych niz modele nieodstajace, wspierajac hipoteze H2. Stanowi to empiryczn podstawe dla stosowania dywergencji jako praktycznej bramy jakosci w systemach decyzyjnych wspomaganych AI.

3. **Jakosc syntezy rozni sie wedlug strategii i dziedziny.** Synteza LLM-as-Judge (S3) osiagnela najwyzsza dokladnosc faktyczna w dziedzinach A i B, podczas gdy glosowanie wiekszosciowe (S1) zapewnilo najpelniejsze pokrycie. Centroid semantyczny (S2) sprawdzil sie najlepiej jako zwiezle podsumowanie reprezentatywne. Zadna strategia nie zdominowala we wszystkich typach promptow.

4. **Dlugosc tokenow nie jest wskaznikiem jakosci.** Zaobserwowalismy znaczaca wariacje liczby tokenow odpowiedzi miedzy modelami dla identycznych promptow (do 6,5 razy dla niektorych promptow), bez konsekwentnej korelacji z dokladnoscia faktyczna. Gemini 2.5-pro byl systematycznie najbardziej gadatliwy; Sonar - najbardziej zwiezly.

## 8.2 Praktyczne wnioski

Dla specjalistow wdrazajacych LLM w srodowiskach regulacyjnych lub wysokiego ryzyka, BMAS sugeruje praktyczna architekture: uruchamianie promptow dla wielu niezaleznych dostawcow modeli, mierzenie konwergencji semantycznej i przekierowywanie odpowiedzi o niskiej pewnosci (wysokiej dywergencji) do przegladu ludzkiego. Naklad jest uzasadniony wzrostem niezawodnosci, szczegolnie dla pytan krytycznych z punktu widzenia zgodnosci.

Protokol pre-rejestracji zastosowany w tym badaniu - blokowanie odpowiedzi referencyjnych przed jakimkolwiek uruchomieniem modelu - jest przenoszalny do kazdego wysilku oceny wielomodelowej i zapobiega uprzedzeniom potwierdzenia.

## 8.3 Zwiazek z projektem AEGIS, AAHP i failprompt

BMAS zostal opracowany w kontekscie projektu AEGIS - transgranicznego systemu weryfikacji tozsamosci rzadowej UE obejmujacego lacza dla Niemiec, Austrii, Szwajcarii, Unii Europejskiej, Polski i Francji - AAHP (AI-to-AI Handoff Protocol), ustrukturyzowanego frameworku orkiestracji wieloagentowej dla produkcyjnych potokov AI, oraz failprompt, narzedzia CLI do walidacji odpowiedzi AI w srodowiskach CI/CD.

Lacznie te trzy projekty tworza zintegrowany zestaw narzedzi do odpowiedzialnego wdrazania AI wielomodelowego: AAHP zapewnia warstwe orkiestracji, failprompt brame CI, a BMAS empiryczne podstawy dla zrozumienia kiedy i dlaczego konsensus wielomodelowy jest bardziej niezawodny niz wynik pojedynczego modelu.

W kontekscie AEGIS wyniki BMAS maja bezposrednie zastosowanie: wielomodelowa walidacja odpowiedzi jest kluczowa dla zapewnienia zgodnosci z roznorodnymi krajowymi ramami regulacyjnymi (RODO, eIDAS 2.0, BSI C5, TISAX, KNF dla Polski) bez polegania na jednym modelu jako jedynym interpretatorem prawa.

Wszystkie kody, prompty, pre-rejestrowane odpowiedzi referencyjne i wyniki eksperymentow sa publikowane jako otwarte zbiory danych.

---

*Zbior danych BMAS, runner, potok metryk i kod syntezy sa dostepne pod adresem: https://github.com/homeofe/BMAS*
