# 1. Wprowadzenie

Duże modele językowe osiągnęły poziom możliwości wystarczający do wdrażania w domenach, gdzie dokładność nie jest opcjonalna: analiza prawna, diagnostyka medyczna, zgodność regulacyjna oraz rządowe systemy identyfikacji. W tych obszarach pewna, lecz błędna odpowiedź pojedynczego modelu nie jest drobną niedogodnością - jest niepowodzeniem o realnych konsekwencjach.

Dominujące podejście do poprawy niezawodności LLM to albo lepsze szkolenie (RLHF, Constitutional AI), albo lepsze promptowanie (łańcuch myślenia, rozszerzanie przez pobieranie). Oba działają w paradygmacie jednego modelu: jeden model, jedna odpowiedź, jeden wynik, któremu można lub nie można ufać.

Niniejsza praca przyjmuje inne podejście. Zamiast pytać "jak sprawić, by jeden model był bardziej niezawodny", pytamy: **czego możemy się nauczyć z niezgodności między wieloma modelami, które nie mogą wzajemnie na siebie wpływać?**

## 1.1 Centralna intuicja

Gdy pięć niezależnych ekspertów odpowiada na to samo pytanie bez konsultowania się ze sobą, a czterech z nich daje tę samą odpowiedź, podczas gdy jeden daje odmienną, nie wyciągamy wniosku, że ci czterej się mylą. Dokładniej badamy odpowiedź odmiennego eksperta, ale ufamy konsensusowi jako punktowi wyjścia.

To jest metoda Delphi, stosowana od 1963 roku w prognozowaniu eksperckim. Jej siła ma charakter strukturalny: **izolacja zapobiega myśleniu grupowemu; konsensus wynika z niezależnego rozumowania, nie z presji społecznej.**

BMAS stosuje tę logikę do LLM. Każdy model jest ekspertem z określonym rozkładem danych treningowych, horyzontem wiedzy i zestawem uprzedzeń. Gdy zostaną od siebie odizolowane i otrzymają to samo pytanie, ich konwergencja lub dywergencja jest sama w sobie informacyjna.

## 1.2 Co jest nowego

Kilka wcześniejszych prac jest pokrewnych, ale zasadniczo różnych:

**Self-Consistency** (Wang et al., 2022) generuje wiele łańcuchów rozumowania z *jednego* modelu i stosuje głosowanie większościowe. BMAS używa *różnych* modeli - testuje to różnice w rozkładach treningowych, a nie tylko wariancję dekodowania.

**Mixture of Agents** (Wang et al., 2024) pozwala modelom widzieć wyniki innych w rundach agregacji. Daje to współpracujące doskonalenie, lecz wprowadza ryzyko propagacji błędów: jeśli model w pierwszej rundzie wytworzy pewną halucynację, kolejne modele mogą się na niej zakotwicyć.

**LLM-as-Judge** (Zheng et al., 2023) używa jednego modelu do oceny innego. BMAS używa jednego modelu do *syntezy* wyników kilku innych - rola sędziego jest ograniczona do końcowej fazy syntezy.

BMAS jest pierwszym frameworkiem łączącym cztery właściwości:
1. Ścisła ślepa izolacja (brak wzajemnej kontaminacji)
2. Różnorodność modeli (różni dostawcy, architektury, rozkłady treningowe)
3. Analiza uwarstwiona według dziedzin (faktyczna, regulacyjna, strategiczna)
4. Dywergencja jako sygnał (nie jako niepowodzenie)

## 1.3 Praktyczna motywacja

Badanie wynikło z doświadczeń operacyjnych zdobytych podczas budowy systemu AEGIS - transgranicznego systemu weryfikacji tożsamości rządowej UE (obejmującego m.in. łącze dla Polski) - oraz AAHP (AI-to-AI Handoff Protocol), ustrukturyzowanego frameworku orkiestracji wieloagentowej. W obu systemach potoki wieloagentowe są używane do podejmowania decyzji architektonicznych, analizy zgodności i przeglądów implementacji.

Pojawiło się praktyczne pytanie: gdy wiele LLM jest używanych jako niezależni recenzenci w potoku, jak bardzo różnią się ich wyniki? A gdy się różnią, kto ma rację?

BMAS jest formalnym odpowiedzeniem na to pytanie.

## 1.4 Wkład naukowy

Niniejsza praca wnosi następujący wkład:

1. **Metodologia BMAS:** Sformalizowany protokół ślepej syntezy wieloagentowej z ograniczeniami izolacji, zestawem metryk i strategiami syntezy.
2. **Badanie empiryczne:** Wyniki 45 promptów dla 12 LLM w 3 warstwach dziedzinowych, z pre-rejestrowanymi odpowiedziami referencyjnymi dla dziedzin A i B.
3. **Walidacja hipotezy dywergencji-jako-sygnału:** Dowody statystyczne, że dywergencja między modelami przewiduje wskaźnik błędów faktycznych.
4. **Porównanie strategii syntezy:** Empiryczna ocena głosowania większościowego, centroidu semantycznego i syntezy LLM-as-Judge w odniesieniu do odpowiedzi referencyjnych.
5. **Otwarty zbiór danych:** Wszystkie prompty, surowe wyniki modeli i wskaźniki metryk opublikowane jako publiczny benchmark.

## 1.5 Struktura artykułu

Sekcja 2 omawia prace pokrewne. Sekcja 3 opisuje metodologię BMAS i projekt eksperymentu. Sekcja 4 przedstawia wyniki. Sekcja 5 analizuje korelacje dywergencja-halucynacja. Sekcja 6 ocenia strategie syntezy. Sekcja 7 omawia implikacje, ograniczenia i przyszłe prace. Sekcja 8 zawiera wnioski.
