# 3. Metodologia

## 3.1 Przegląd protokołu BMAS

Blind Multi-Agent Synthesis (BMAS) to czterofazowy protokół elicytacji, porównania i syntezy odpowiedzi wielu LLM na identyczne zapytania:

1. **Ślepa elicytacja** - Każdy model otrzymuje ten sam prompt bez wiedzy o badaniu, innych modelach ani innych odpowiedziach.
2. **Obliczanie metryk** - Parowe podobieństwo semantyczne, dokładność faktyczna i wykrywanie wartości odstających są obliczane dla wszystkich odpowiedzi.
3. **Synteza** - Trzy strategie syntezy agregują poszczególne odpowiedzi w jeden wynik.
4. **Ocena** - Wyniki syntezy są oceniane względem pre-rejestrowanych odpowiedzi referencyjnych (dziedziny A i B) lub oceny eksperckiej (dziedzina C).

Protokół wymusza ścisłą **zasadę braku kontaminacji**: żadna odpowiedź modelu nie jest udostępniana żadnemu innemu modelowi w żadnej fazie poprzedzającej syntezę.

## 3.2 Modele

Oceniamy dwanaście najbardziej zaawansowanych LLM od czterech różnych dostawców:

| ID | Model | Dostawca | Okno kontekstu |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M tokenów |
| M2 | claude-opus-4-6 | Anthropic | 1M tokenów |
| M3 | gpt-5.3-codex | OpenAI | 272k tokenów |
| M4 | gemini-2.5-pro | Google | 1M tokenów |
| M5 | sonar-pro | Perplexity | 127k tokenów |

Różnorodność wielodostawcza jest celowa. Modele tego samego dostawcy dzielą rodowód architektoniczny i potoki danych treningowych, co może redukować dywergencję nawet w warunkach ślepych.

**Implementacja izolacji:** Każdy model działa w oddzielnej, izolowanej sesji bez wspólnego kontekstu. Systemowy prompt jest identyczny we wszystkich modelach:

> *"Jesteś kompetentnym asystentem eksperckim. Odpowiedz na następujące pytanie możliwie najdokładniej i najwyczerpującym sposobem. Bądź precyzyjny, oparty na faktach i ustrukturyzowany. Jeśli nie jesteś pewien konkretnego szczegółu, wyraź to wprost."*

Temperatura nie jest modyfikowana. Celowo zachowujemy domyślne zachowanie próbkowania każdego modelu, aby uchwycić naturalną wariancję odpowiedzi.

## 3.3 Projektowanie promptów

### 3.3.1 Struktura dziedzin

Konstruujemy 45 promptów w trzech warstwach dziedzinowych:

**Dziedzina A - Techniczne wysokiej precyzji (A01-A10):** Pytania z obiektywnie prawidłowymi odpowiedziami weryfikowalnymi względem autorytatywnych źródeł pierwotnych (standardy NIST FIPS, NVD, RFC IETF, specyfikacje OpenID Foundation). Przykłady: uzasadnienie punktacji CVSS, rozmiary kluczy algorytmów PQC, wyliczenie zestawów szyfrów TLS 1.3.

**Dziedzina B - Regulacyjna/Zgodność (B01-B10):** Pytania oparte na tekstach prawnych i regulacyjnych z autorytatywnymi źródłami (RODO, eIDAS 2.0, NIS2, ISO 27001, BSI C5). Centralne odpowiedzi są zdefiniowane w tekście formalnym. Przykłady: wyjątki od usuwania danych z Artykułu 17(3) RODO, klasyfikacje sektorowe NIS2, różnice poziomów oceny TISAX.

**Dziedzina C - Strategiczna/Nieokreślona (C01-C10):** Pytania bez jednej prawidłowej odpowiedzi, wymagające eksperckiego osądu i rozumowania architektonicznego. Istnieje wiele możliwych do obronienia stanowisk. Przykłady: decyzje architektoniczne zero-trust, priorytyzacja migracji PQC, kompromisy inwestycyjne w zgodności.

### 3.3.2 Wymagania wobec promptów

Wszystkie prompty spełniają cztery kryteria:
1. **Samodzielne** - możliwe do odpowiedzi bez zewnętrznego kontekstu ani pobierania dokumentów
2. **Ustrukturyzowana odpowiedź** - każdy prompt określa wymagany format wyjścia
3. **Ograniczona długość** - oczekiwana odpowiedź 300-600 tokenów dla dziedzin A-B; 400-800 dla dziedziny C
4. **Weryfikowalne** - dla dziedzin A i B istnieje weryfikowalna odpowiedź

### 3.3.3 Pre-rejestracja

Zgodnie z najlepszymi praktykami otwartej nauki, odpowiedzi referencyjne dla dziedzin A i B zostały udokumentowane i zablokowane przed uruchomieniem jakiegokolwiek modelu. Zapobiega to nieświadomemu uprzedzeniu potwierdzenia w ocenianiu.

## 3.4 Metryki

### 3.4.1 Podobieństwo semantyczne (podstawowe)

Obliczamy parowe podobieństwo cosinusowe między embeddingami odpowiedzi za pomocą modelu sentence-transformer `all-mpnet-base-v2`. Dla N modeli daje to macierz podobieństwa N x N na prompt. Raportujemy:
- **Średnie parowe podobieństwo (MPS):** średnia ze wszystkich N(N-1)/2 parowych wyników
- **Minimalne parowe podobieństwo:** najbardziej rozbieżna para
- **Odchylenie standardowe podobieństwa:** wariancja w obrębie klastra odpowiedzi na prompt

### 3.4.2 BERTScore

Obliczamy parowe BERTScore F1 jako wtórne miary podobieństwa semantycznego na poziomie tokenów. BERTScore rejestruje bliskość leksykalną poza embeddingami na poziomie zdań.

### 3.4.3 Jaccard na kluczowych twierdzeniach

Wyodrębniamy dyskretne twierdzenia faktyczne z każdej odpowiedzi za pomocą segmentacji zdań i obliczamy parowe podobieństwo Jaccarda na znormalizowanych zbiorach twierdzenia. Metryka ta rejestruje zgodność strukturalną.

### 3.4.4 Wykrywanie wartości odstających

Stosujemy DBSCAN z eps=0.15 i min_samples=2. Modele, których embeddingi wypadają poza wszystkie klastry sąsiedztwa, otrzymują etykietę wartości odstającej (-1). Traktujemy status wartości odstającej jako sygnał potencjalnej halucynacji w dziedzinach A i B.

### 3.4.5 Dokładność faktyczna (tylko dziedziny A i B)

Dla każdej odpowiedzi dziedzin A i B oceniamy dokładność faktyczną względem listy kontrolnej pre-rejestrowanych odpowiedzi referencyjnych. Wynik dokładności faktycznej to ułamek spełnionych elementów listy.

## 3.5 Strategie syntezy

**S1 - Głosowanie większościowe (poziom twierdzenia):** Twierdzenia faktyczne są akceptowane, jeśli pojawiają się w odpowiedziach co najmniej 60% modeli. Twierdzenia mniejszościowe są dodawane z markerem [MINORITY].

**S2 - Centroid semantyczny:** Odpowiedź, której embedding jest najbliższy średniej wszystkich embeddingów, jest wybierana jako baza syntezy. Nie dodaje się nowych treści.

**S3 - LLM-as-Judge:** Pięć zanonimizowanych odpowiedzi jest przedstawianych szóstej instancji modelu (M2, claude-opus-4-6) z poleceniem produkcji jednej autorytatywnej syntezy, oznaczając twierdzenia mniejszościowe ([MINORITY]) i sprzeczności ([DISPUTED]).

## 3.6 Hipotezy

**H1 (Konwergencja w dziedzinach faktycznych):** Średnie parowe podobieństwo semantyczne dla promptów dziedzin A i B przekroczy 0.75 (BERTScore F1).

**H2 (Dywergencja sygnalizuje błąd):** Wśród odpowiedzi dziedzin A i B modele odstające (etykieta DBSCAN -1) będą miały znacząco niższe wyniki dokładności faktycznej niż modele nieodstające (jednostronny test t, alfa=0.05).

**H3 (Wpływ dziedziny na konwergencję):** Średnie parowe podobieństwo dla dziedziny C będzie znacząco niższe niż dla dziedzin A i B (jednoczynnikowa ANOVA, Tukey HSD post-hoc, alfa=0.05).

## 3.7 Konfiguracja eksperymentalna

Wszystkie uruchomienia modeli zostały wykonane za pośrednictwem bramy OpenClaw, która kieruje niezależnie do API każdego dostawcy. Kompletny zbiór danych 540 uruchomień (45 promptów x 5 modeli) jest publikowany razem z niniejszą pracą.
