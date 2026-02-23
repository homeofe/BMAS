# 📋 Streszczenie

Przedstawiamy **Blind Multi-Agent Synthesis (BMAS)**, metodologię pomiaru konwergencji i dywergencji wielu dużych modeli językowych (LLM) odpowiadających na identyczne zapytania w ścisłej izolacji. Inspirowany metodą Delphi stosowaną w prognozowaniu eksperckim, BMAS wymusza pełną izolację odpowiedzi na poziomie modelu: żaden model nie obserwuje wyników innego modelu przed fazą syntezy.

Oceniamy dwanaście najbardziej zaawansowanych LLM na trzech poziomach dziedzinowych: (A) pytania techniczne wysokiej precyzji z weryfikowalnymi odpowiedziami, (B) pytania regulacyjne i dotyczące zgodności z autorytatywnymi źródłami prawnymi oraz (C) pytania strategiczne i architektoniczne z uzasadnionymi rozbieżnościami między ekspertami. Stosując metryki podobieństwa semantycznego (BERTScore, odległość cosinusowa na embeddingach), dokładność faktyczną w porównaniu z pre-rejestrowanymi odpowiedziami referencyjnymi oraz wykrywanie wartości odstających za pomocą klasteryzacji DBSCAN, kwantyfikujemy odchylenia między modelami i ich związek z typem dziedziny oraz wskaźnikiem halucynacji.

Nasza centralna hipoteza głosi, że w dobrze zdefiniowanych dziedzinach faktycznych odpowiedzi LLM konwergują w stopniu umożliwiającym traktowanie **konsensusu jako sygnału jakości**: wysoka zgodność między modelami przewiduje poprawność faktyczną, natomiast znacząca dywergencja sygnalizuje halucynację modelu lub niewystarczająco sprecyzowane pytanie. Oceniamy ponadto trzy strategie syntezy - agregację przez głosowanie większościowe, wybór centroidu semantycznego oraz syntezę LLM-as-Judge - w odniesieniu do pre-rejestrowanych odpowiedzi referencyjnych.

BMAS ma bezpośrednie implikacje praktyczne dla wdrożeń AI wysokiego ryzyka w administracji publicznej, systemach ochrony zdrowia i systemach prawnych, gdzie żadnemu pojedynczemu modelowi nie można bezwarunkowo ufać. Traktując **dywergencję jako sygnał anomalii** zamiast niepowodzenia koordynacji, BMAS dostarcza praktyczną warstwę zapewnienia jakości dla systemów LLM w środowisku produkcyjnym.

**Słowa kluczowe:** duże modele językowe, systemy wieloagentowe, konsensus, wykrywanie halucynacji, metoda Delphi, podobieństwo semantyczne, zapewnienie jakości AI
