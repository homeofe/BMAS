# 1. Wprowadzenie

Duze modele jezykowe osiagnely poziom mozliwosci wystarczajacy do wdrazania w domenach, gdzie dokladnosc nie jest opcjonalna: analiza prawna, diagnostyka medyczna, zgodnosc regulacyjna oraz rzadowe systemy identyfikacji. W tych obszarach pewna, lecz bledna odpowiedz pojedynczego modelu nie jest drobna niedogodnoscia - jest niepowodzeniem o realnych konsekwencjach.

Dominujace podejscie do poprawy niezawodnosci LLM to albo lepsze szkolenie (RLHF, Constitutional AI), albo lepsze promptowanie (lancuch myslenia, rozszerzanie przez pobieranie). Oba dzialaja w paradygmacie jednego modelu: jeden model, jedna odpowiedz, jeden wynik, ktoremu mozna lub nie mozna ufac.

Niniejsza praca przyjmuje inne podejscie. Zamiast pytac "jak sprawic, by jeden model byl bardziej niezawodny", pytamy: **czego mozemy sie nauczyc z niezgodnosci miedzy wieloma modelami, ktore nie moga wzajemnie na siebie wplywac?**

## 1.1 Centralna intuicja

Gdy piec niezaleznych ekspertow odpowiada na to samo pytanie bez konsultowania sie ze soba, a czterech z nich daje te sama odpowiedz, podczas gdy jeden daje odmienna, nie wyciagamy wniosku, ze ci czterej sie myla. Dokladniej badamy odpowiedz odmiennego eksperta, ale ufamy konsensusowi jako punktowi wyjscia.

To jest metoda Delphi, stosowana od 1963 roku w prognozowaniu eksperckim. Jej sila ma charakter strukturalny: **izolacja zapobiega mysleniu grupowemu; konsensus wynika z niezaleznego rozumowania, nie z presji spolecznej.**

BMAS stosuje te logike do LLM. Kazdy model jest ekspertem z okreslonym rozkladem danych treningowych, horyzontem wiedzy i zestawem uprzedzen. Gdy zostana od siebie odizolowane i otrzymaja to samo pytanie, ich konwergencja lub dywergencja jest sama w sobie informacyjna.

## 1.2 Co jest nowego

Kilka wczesniejszych prac jest pokrewnych, ale zasadniczo roznych:

**Self-Consistency** (Wang et al., 2022) generuje wiele lancuchow rozumowania z *jednego* modelu i stosuje glosowanie wiekszosciowe. BMAS uzywa *roznych* modeli - testuje to roznice w rozkladach treningowych, a nie tylko wariancje dekodowania.

**Mixture of Agents** (Wang et al., 2024) pozwala modelom widziec wyniki innych w rundach agregacji. Daje to wspolpracujace doskonalenie, lecz wprowadza ryzyko propagacji bledow: jesli model w pierwszej rundzie wytworzy pewna halucynacje, kolejne modele moga sie na niej zakotwiczyc.

**LLM-as-Judge** (Zheng et al., 2023) uzywa jednego modelu do oceny innego. BMAS uzywa jednego modelu do *syntezy* wynikow kilku innych - rola sedzia jest ograniczona do koncowej fazy syntezy.

BMAS jest pierwszym frameworkiem laczacym cztery wlasciwosci:
1. Scisla slepa izolacja (brak wzajemnej kontaminacji)
2. Roznorodnosc modeli (rozni dostawcy, architektury, rozklady treningowe)
3. Analiza uwarstwiona wedlug dziedzin (faktyczna, regulacyjna, strategiczna)
4. Dywergencja jako sygnal (nie jako niepowodzenie)

## 1.3 Praktyczna motywacja

Badanie wyniklo z doswiadczen operacyjnych zdobytych podczas budowy systemu AEGIS - transgranicznego systemu weryfikacji tozsamosci rzadowej UE (obejmujacego m.in. zlacze dla Polski) - oraz AAHP (AI-to-AI Handoff Protocol), ustrukturyzowanego frameworku orkiestracji wieloagentowej. W obu systemach potoki wieloagentowe sa uzywane do podejmowania decyzji architektonicznych, analizy zgodnosci i przegladow implementacji.

Pojawilo sie praktyczne pytanie: gdy wiele LLM jest uzywanych jako niezalezni recenzenci w potoku, jak bardzo roznia sie ich wyniki? A gdy sie roznia, kto ma racje?

BMAS jest formalnym odpowiedzeniem na to pytanie.

## 1.4 Wklad naukowy

Niniejsza praca wnosi nastepujacy wklad:

1. **Metodologia BMAS:** Sformalizowany protokol sleepej syntezy wieloagentowej z ograniczeniami izolacji, zestawem metryk i strategiami syntezy.
2. **Badanie empiryczne:** Wyniki 30 promptow dla 5 LLM w 3 warstwach dziedzinowych, z pre-rejestrowanymi odpowiedziami referencyjnymi dla dziedzin A i B.
3. **Walidacja hipotezy dywergencji-jako-sygnalu:** Dowody statystyczne, ze dywergencja miedzy modelami przewiduje wskaznik bledow faktycznych.
4. **Porownanie strategii syntezy:** Empiryczna ocena glosowania wiekszosciowego, centroidu semantycznego i syntezy LLM-as-Judge w odniesieniu do odpowiedzi referencyjnych.
5. **Otwarty zbior danych:** Wszystkie prompty, surowe wyniki modeli i wskazniki metryk opublikowane jako publiczny benchmark.

## 1.5 Struktura artykulu

Sekcja 2 omawia prace pokrewne. Sekcja 3 opisuje metodologie BMAS i projekt eksperymentu. Sekcja 4 przedstawia wyniki. Sekcja 5 analizuje korelacje dywergencja-halucynacja. Sekcja 6 ocenia strategie syntezy. Sekcja 7 omawia implikacje, ograniczenia i przyszle prace. Sekcja 8 zawiera wnioski.
