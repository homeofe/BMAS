# 8. Wnioski

Niniejsza praca przedstawila **Blind Multi-Agent Synthesis (BMAS)**, metodologie elicytacji, porownania i syntezy odpowiedzi wielu duzych modeli jezykowych w scislej izolacji, oraz zaprezentowala wyniki empiryczne eksperymentu obejmujacego 150 uruchomien na pieciu modelach frontier i trzech poziomach dziedzinowych.

## 8.1 Podsumowanie wkladu naukowego

Wykazalismy, ze:

1. **Konwergencja jest zalezna od dziedziny i mierzalna.** Na 30 promptach dziedziny A i B (techniczna i regulacyjna) wykazaly systematycznie wyzsza miedzymodelowa podobnosc semantyczna niz dziedzina C (prompty strategiczne i nieokreslone). [Patrz sekcja 4 po dokladne wartosci.]

2. **Dywergencja sygnalizuje blad w dziedzinach faktycznych.** Modele zidentyfikowane jako semantyczne wartosci odstajace wykazaly nizsza dokladnosc faktyczna wzgledem pre-rejestrowanych odpowiedzi referencyjnych niz modele nieodstajace, wspierajac hipoteze H2.

3. **Jakosc syntezy rozni sie w zaleznosci od strategii i dziedziny.** Synteza LLM-as-Judge (S3) osiagnela najwyzsza dokladnosc faktyczna w dziedzinach A i B, podczas gdy glosowanie wiekszosciowe (S1) zapewnilo najbardziej wyczerpujace pokrycie. Zaden model nie zdominowal we wszystkich typach promptow.

4. **Dlugosc tokenow nie jest wskaznikiem jakosci.** Obserwowalismy znaczna wariancje w liczbie tokenow odpowiedzi miedzy modelami na identycznych promptach (do 6,5-krotnosci dla niektorych promptow), bez konsekwentnej korelacji z dokladnoscia faktyczna.

## 8.2 Praktyczne wnioski

Dla praktycy wdrazajacych LLM w srodowiskach regulowanych lub wysokiego ryzyka, BMAS sugeruje praktyczna architekture: uruchamianie promptow na wielu niezaleznych dostawcach modeli, mierzenie konwergencji semantycznej i kierowanie odpowiedzi o niskiej pewnosci (wysokiej dywergencji) do przegladu ludzkiego. Protokol pre-rejestracji zastosowany w niniejszym badaniu jest przekazywalny do kazdego wysilku ewaluacji wielomodelowej i zapobiega uprzedzeniu potwierdzenia.

## 8.3 Zwiazek z AEGIS, AAHP i failprompt

BMAS zostal opracowany w kontekscie projektu AEGIS - transgranicznego systemu weryfikacji tozsamosci rzadowej UE obejmujacego lacza dla Niemiec, Austrii, Szwajcarii, Polski, Francji i innych krajow - AAHP (AI-to-AI Handoff Protocol), ustrukturyzowanego frameworku orkiestracji wieloagentowej dla produkcyjnych potoków AI, oraz failprompt, narzedzia CLI do walidacji odpowiedzi AI w srodowiskach CI/CD. Razem te trzy projekty tworza zintegrowany zestaw narzedzi do odpowiedzialnego wdrazania wielomodelowego AI: AAHP dostarcza warstwe orkiestracji, failprompt brame CI, a BMAS empiryczne podstawy do rozumienia kiedy i dlaczego konsensus wielomodelowy jest bardziej niezawodny niz wynik pojedynczego modelu.

Dla projektu AEGIS w szczegolnosci BMAS dostarcza empirycznie uzasadnionej metodologii walidacji interpretacji regulacyjnych (RODO, eIDAS 2.0, NIS2, BSI C5) przez wiele modeli bez polegania na jednym modelu jako jedynym interpretatorem ram prawnych - co jest szczegolnie istotne w kontekscie wymogow zgodnosci Polski i innych krajow czlonkowskich UE.

Wszystkie kody, prompty, pre-rejestrowane odpowiedzi referencyjne i wyniki eksperymentow sa publikowane jako otwarte zbiory danych wspierajace replikacje i rozszerzenie niniejszej pracy.

---

*Zbior danych BMAS, runner, potok metryk i kod syntezy sa dostepne pod adresem: https://github.com/homeofe/BMAS*
