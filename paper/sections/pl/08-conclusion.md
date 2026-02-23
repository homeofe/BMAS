# 🎯 8. Wnioski

Niniejsza praca przedstawiła **Blind Multi-Agent Synthesis (BMAS)**, metodologię elicytacji, porównania i syntezy odpowiedzi wielu dużych modeli językowych w ścisłej izolacji, oraz zaprezentowała wyniki empiryczne eksperymentu obejmującego 540 uruchomień na pięciu modelach frontier i trzech poziomach dziedzinowych.

## 8.1 Podsumowanie wkładu naukowego

Wykazaliśmy, że:

1. **Konwergencja jest zależna od dziedziny i mierzalna.** Na 45 promptach dziedziny A i B (techniczna i regulacyjna) wykazały systematycznie wyższą międzymodelową podobność semantyczną niż dziedzina C (prompty strategiczne i nieokreślone). [Patrz sekcja 4 po dokładne wartości.]

2. **Dywergencja sygnalizuje błąd w dziedzinach faktycznych.** Modele zidentyfikowane jako semantyczne wartości odstające wykazały niższą dokładność faktyczną względem pre-rejestrowanych odpowiedzi referencyjnych niż modele nieodstające, wspierając hipotezę H2.

3. **Jakość syntezy różni się w zależności od strategii i dziedziny.** Synteza LLM-as-Judge (S3) osiągnęła najwyższą dokładność faktyczną w dziedzinach A i B, podczas gdy głosowanie większościowe (S1) zapewniło najbardziej wyczerpujące pokrycie. Żaden model nie zdominował we wszystkich typach promptów.

4. **Długość tokenów nie jest wskaźnikiem jakości.** Obserwowaliśmy znaczną wariancję w liczbie tokenów odpowiedzi między modelami na identycznych promptach (do 6,5-krotności dla niektórych promptów), bez konsekwentnej korelacji z dokładnością faktyczną.

## 🎯 8.2 Praktyczne wnioski

Dla praktyków wdrażających LLM w środowiskach regulowanych lub wysokiego ryzyka, BMAS sugeruje praktyczną architekturę: uruchamianie promptów na wielu niezależnych dostawcach modeli, mierzenie konwergencji semantycznej i kierowanie odpowiedzi o niskiej pewności (wysokiej dywergencji) do przeglądu ludzkiego. Protokół pre-rejestracji zastosowany w niniejszym badaniu jest przekazywalny do każdego wysiłku ewaluacji wielomodelowej i zapobiega uprzedzeniu potwierdzenia.

## 8.3 Związek z AEGIS, AAHP i failprompt

BMAS został opracowany w kontekście projektu AEGIS - transgranicznego systemu weryfikacji tożsamości rządowej UE obejmującego łącza dla Niemiec, Austrii, Szwajcarii, Polski, Francji i innych krajów - AAHP (AI-to-AI Handoff Protocol), ustrukturyzowanego frameworku orkiestracji wieloagentowej dla produkcyjnych potoków AI, oraz failprompt, narzędzia CLI do walidacji odpowiedzi AI w środowiskach CI/CD. Razem te trzy projekty tworzą zintegrowany zestaw narzędzi do odpowiedzialnego wdrażania wielomodelowego AI: AAHP dostarcza warstwę orkiestracji, failprompt bramę CI, a BMAS empiryczne podstawy do rozumienia kiedy i dlaczego konsensus wielomodelowy jest bardziej niezawodny niż wynik pojedynczego modelu.

Dla projektu AEGIS w szczególności BMAS dostarcza empirycznie uzasadnionej metodologii walidacji interpretacji regulacyjnych (RODO, eIDAS 2.0, NIS2, BSI C5) przez wiele modeli bez polegania na jednym modelu jako jedynym interpretatorem ram prawnych - co jest szczególnie istotne w kontekście wymogów zgodności Polski i innych krajów członkowskich UE.

Wszystkie kody, prompty, pre-rejestrowane odpowiedzi referencyjne i wyniki eksperymentów są publikowane jako otwarte zbiory danych wspierające replikację i rozszerzenie niniejszej pracy.

---

*Zbiór danych BMAS, runner, potok metryk i kod syntezy są dostępne pod adresem: https://github.com/homeofe/BMAS*
