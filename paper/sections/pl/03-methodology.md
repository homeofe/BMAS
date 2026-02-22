# 3. Metodologia

## 3.1 Przeglad protokolu BMAS

Blind Multi-Agent Synthesis (BMAS) to czterofazowy protokol elicytacji, porownania i syntezy odpowiedzi wielu LLM na identyczne zapytania:

1. **Slepa elicytacja** - Kazdy model otrzymuje ten sam prompt bez wiedzy o badaniu, innych modelach ani innych odpowiedziach.
2. **Obliczanie metryk** - Parowe podobienstwo semantyczne, dokladnosc faktyczna i wykrywanie wartosci odstajacych sa obliczane dla wszystkich odpowiedzi.
3. **Synteza** - Trzy strategie syntezy agreguja poszczegolne odpowiedzi w jeden wynik.
4. **Ocena** - Wyniki syntezy sa oceniane wzgledem pre-rejestrowanych odpowiedzi referencyjnych (dziedziny A i B) lub oceny eksperckiej (dziedzina C).

Protokol wymusza scisla **zasade braku kontaminacji**: zadna odpowiedz modelu nie jest udostepniana zadnemu innemu modelowi w zadnej fazie poprzedzajacej synteze.

## 3.2 Modele

Oceniamy piec najbardziej zaawansowanych LLM od czterech roznych dostawcow:

| ID | Model | Dostawca | Okno kontekstu |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M tokenow |
| M2 | claude-opus-4-6 | Anthropic | 1M tokenow |
| M3 | gpt-5.3-codex | OpenAI | 272k tokenow |
| M4 | gemini-2.5-pro | Google | 1M tokenow |
| M5 | sonar-pro | Perplexity | 127k tokenow |

Roznorodnosc wielodostawcza jest celowa. Modele tego samego dostawcy dziela rodowod architektoniczny i potoki danych treningowych, co moze redukowac dywergencje nawet w warunkach slepych.

**Implementacja izolacji:** Kazdy model dziala w oddzielnej, izolowanej sesji bez wspolnego kontekstu. Systemowy prompt jest identyczny we wszystkich modelach:

> *"Jestes kompetentnym asystentem eksperckim. Odpowiedz na nastepujace pytanie mozliwie najdokladniej i najwyczerpujacym sposob. Badz precyzyjny, oparty na faktach i ustrukturyzowany. Jesli nie jestes pewny konkretnego szczegolu, wyraz to wprost."*

Temperatura nie jest modyfikowana. Celowo zachowujemy domyslne zachowanie probkowania kazdego modelu, aby uchwycic naturalna wariancje odpowiedzi.

## 3.3 Projektowanie promptow

### 3.3.1 Struktura dziedzin

Konstruujemy 30 promptow w trzech warstwach dziedzinowych:

**Dziedzina A - Techniczne wysokiej precyzji (A01-A10):** Pytania z obiektywnie prawidlowymi odpowiedziami weryfikowalnymi wzgledem autorytatywnych zrodel pierwotnych (standardy NIST FIPS, NVD, RFC IETF, specyfikacje OpenID Foundation). Przyklady: uzasadnienie punktacji CVSS, rozmiary kluczy algorytmow PQC, wyliczenie zestawow szyfrow TLS 1.3.

**Dziedzina B - Regulacyjna/Zgodnosc (B01-B10):** Pytania oparte na tekstach prawnych i regulacyjnych z autorytatywnymi zrodlami (RODO, eIDAS 2.0, NIS2, ISO 27001, BSI C5). Centralne odpowiedzi sa zdefiniowane w tekście formalnym. Przyklady: wyjatki od usuwania danych z Artykulu 17(3) RODO, klasyfikacje sektorowe NIS2, roznice poziomow oceny TISAX.

**Dziedzina C - Strategiczna/Nieokreslona (C01-C10):** Pytania bez jednej prawidlowej odpowiedzi, wymagajace eksperckiego osadu i rozumowania architektonicznego. Istnieje wiele mozliwych do obronienia stanowisk. Przyklady: decyzje architektoniczne zero-trust, priorytyzacja migracji PQC, kompromisy inwestycyjne w zgodnosci.

### 3.3.2 Wymagania wobec promptow

Wszystkie prompty spelniaja cztery kryteria:
1. **Samodzielne** - mozliwe do odpowiedzi bez zewnetrznego kontekstu ani pobierania dokumentow
2. **Ustrukturyzowana odpowiedz** - kazdy prompt okresla wymagany format wyjscia
3. **Ograniczona dlugosc** - oczekiwana odpowiedz 300-600 tokenow dla dziedzin A-B; 400-800 dla dziedziny C
4. **Weryfikowalne** - dla dziedzin A i B istnieje weryfikowalna odpowiedz

### 3.3.3 Pre-rejestracja

Zgodnie z najlepszymi praktykami otwartej nauki, odpowiedzi referencyjne dla dziedzin A i B zostaly udokumentowane i zablokowane przed uruchomieniem jakiegokolwiek modelu. Zapobiega to nieswiadomemu uprzedzeniu potwierdzenia w ocenianiu.

## 3.4 Metryki

### 3.4.1 Podobienstwo semantyczne (podstawowe)

Obliczamy parowe podobienstwo cosinusowe miedzy embeddingami odpowiedzi za pomoca modelu sentence-transformer `all-mpnet-base-v2`. Dla N modeli daje to macierz podobienstwa N x N na prompt. Raportujemy:
- **Srednie parowe podobienstwo (MPS):** srednia ze wszystkich N(N-1)/2 parowych wynikow
- **Minimalne parowe podobienstwo:** najbardziej rozbiezna para
- **Odchylenie standardowe podobienstwa:** wariancja w obrebie klastra odpowiedzi na prompt

### 3.4.2 BERTScore

Obliczamy parowe BERTScore F1 jako wtorne miary podobienstwa semantycznego na poziomie tokenow. BERTScore rejestruje bliskosc leksykalna poza embeddingami na poziomie zdan.

### 3.4.3 Jaccard na kluczowych twierdzeniach

Wyodrebniamy dyskretne twierdzenia faktyczne z kazdej odpowiedzi za pomoca segmentacji zdan i obliczamy parowe podobienstwo Jaccarda na znormalizowanych zbiorach twierdzenia. Metryka ta rejestruje zgodnosc strukturalna.

### 3.4.4 Wykrywanie wartosci odstajacych

Stosujemy DBSCAN z eps=0.15 i min_samples=2. Modele, ktorych embeddingi wypadaja poza wszystkie klastry sasiedztwa, otrzymuja etykiete wartosci odstajacej (-1). Traktujemy status wartosci odstajacej jako sygnal potencjalnej halucynacji w dziedzinach A i B.

### 3.4.5 Dokladnosc faktyczna (tylko dziedziny A i B)

Dla kazdej odpowiedzi dziedzin A i B oceniamy dokladnosc faktyczna wzgledem listy kontrolnej pre-rejestrowanych odpowiedzi referencyjnych. Wynik dokladnosci faktycznej to ulamek spelnionych elementow listy.

## 3.5 Strategie syntezy

**S1 - Glosowanie wiekszosciowe (poziom twierdzenia):** Twierdzenia faktyczne sa akceptowane, jesli pojawiaja sie w odpowiedziach co najmniej 60% modeli. Twierdzenia mniejszosciowe sa dodawane z markerem [MINORITY].

**S2 - Centroid semantyczny:** Odpowiedz, ktorej embedding jest najblizszy sredniej wszystkich embedddingow, jest wybierana jako baza syntezy. Nie dodaje sie nowych tresci.

**S3 - LLM-as-Judge:** Piec anonimizowanych odpowiedzi jest przedstawianych szostej instancji modelu (M2, claude-opus-4-6) z poleceniem produkcji jednej autorytatywnej syntezy, oznaczajac twierdzenia mniejszoscioew ([MINORITY]) i sprzecznosci ([DISPUTED]).

## 3.6 Hipotezy

**H1 (Konwergencja w dziedzinach faktycznych):** Srednie parowe podobienstwo semantyczne dla promptow dziedzin A i B przekroczy 0.75 (BERTScore F1).

**H2 (Dywergencja sygnalizuje blad):** Wsrod odpowiedzi dziedzin A i B modele odstajace (etykieta DBSCAN -1) beda mialy znaczaco nizsze wyniki dokladnosci faktycznej niz modele nieodstajace (jednostronny test t, alfa=0.05).

**H3 (Wplyw dziedziny na konwergencje):** Srednie parowe podobienstwo dla dziedziny C bedzie znaczaco nizsze niz dla dziedzin A i B (jednoczynnikowa ANOVA, Tukey HSD post-hoc, alfa=0.05).

## 3.7 Konfiguracja eksperymentalna

Wszystkie uruchomienia modeli zostaly wykonane za posrednictwem bramy OpenClaw, ktora kieruje niezaleznie do API kazdego dostawcy. Kompletny zbior danych 150 uruchomien (30 promptow x 5 modeli) jest publikowany razem z niniejsza praca.
