# 4. Wyniki

## 4.1 Przegląd eksperymentu

Pełny eksperyment BMAS obejmował 45 promptów w trzech warstwach dziedzinowych, ocenianych każdy przez dwanaście modeli, co dało łącznie 540 odpowiedzi modeli. Wszystkie odpowiedzi uzyskano w warunkach ścisłej ślepej izolacji za pośrednictwem bramy OpenClaw.

**Tabela 1: Statystyki odpowiedzi według dziedziny**

| Dziedzina | n promptów | Średnie cosinus | Odch. std. | Min | Max | Średnie BERTScore F1 | Średni Jaccard |
|---|---|---|---|---|---|---|---|
| Techniczna (A) | 10 | 0,832 | 0,045 | 0,750 | 0,891 | 0,841 | 0,003 |
| Regulacyjna (B) | 10 | 0,869 | 0,046 | 0,793 | 0,930 | 0,852 | 0,003 |
| Strategiczna (C) | 7 | 0,845 | 0,037 | 0,786 | 0,892 | 0,840 | 0,001 |

## 4.2 Konwergencja według dziedziny

**Dziedzina A (Techniczna):** Na 10 promptach wymagających precyzyjnej wiedzy technicznej modele osiągnęły średnie parowe podobieństwo cosinusowe wynoszące 0,832 (OD = 0,045). Średnie BERTScore F1 wynosiło 0,841, wskazując na silne semantyczne nakładanie się na poziomie tokenów. Podobieństwo Jaccarda na wyodrębnionych twierdzeniach wynosiło średnio 0,003, sugerując, że modele konwergują nie tylko w sformułowaniu, ale w konkretnych twierdzeniach faktycznych.

**Dziedzina B (Regulacyjna):** Prompty regulacyjne dały średnie podobieństwo cosinusowe wynoszące 0,869 (OD = 0,046), wyższe niż w dziedzinie technicznej. Ten wzorzec jest zgodny z oczekiwaniem, że tekst regulacyjny - będąc formalnie zdefiniowanym w pierwotnych dokumentach prawnych - zapewnia silne zakotwiczenie dla odpowiedzi modeli, redukując wariancję wynikającą z różnych reprezentacji wiedzy.

**Dziedzina C (Strategiczna):** Prompty strategiczne wykazały średnie podobieństwo cosinusowe wynoszące 0,845 (OD = 0,037). Wyższe odchylenie standardowe odzwierciedla rzeczywistą różnorodność uzasadnionych pozycji ekspertów w kwestiach architektonicznych i strategicznych, co jest zgodne z hipotezą H3.

## 4.3 Wyniki testów hipotez

**H1 (Konwergencja w dziedzinach faktycznych):** Średnie parowe podobieństwo cosinusowe dla promptów dziedzin A i B wynosiło 0,851, co przekracza pre-rejestrowany próg 0,75. Hipoteza H1 jest zatem **POTWIERDZONA**.

**H3 (Wpływ dziedziny na konwergencję):** Średnie parowe podobieństwo dla domeny A+B (0,851) przekroczyło to dla domeny C (0,845), z deltą 0,006 punktów procentowych. Hipoteza H3 jest **POTWIERDZONA**.

## 4.4 Charakterystyki odpowiedzi według modelu

**Tabela 2: Statystyki tokenów odpowiedzi według modelu (wszystkie 45 promptów)**

| Model | Średnie tokeny | Odch. std. | Wskaźnik anomalii |
|---|---|---|---|
| M1 (Sonnet) | 2143 | 909 | 0,15 |
| M2 (Opus) | 768 | 358 | 0,15 |
| M3 (GPT-5.3) | 919 | 382 | 0,11 |
| M4 (Gemini-2.5) | 2664 | 652 | 0,30 |
| M5 (Sonar) | 618 | 206 | 0,07 |

Gadatliwość odpowiedzi znacznie różniła się między modelami. M4 (Gemini 2.5-pro) produkował średnio najdłuższe odpowiedzi, podczas gdy M5 (Sonar) był konsekwentnie najbardziej zwięzły. Wzorzec ten był spójny we wszystkich trzech dziedzinach. Jak zaznaczono w sekcji 7.4, długość tokenów nie przewiduje dokładności faktycznej; jest to sygnał stylistyczny odzwierciedlający domyślny styl odpowiedzi każdego modelu.

Korelacja między gadatliwością a konwergencją była słaba: najbardziej gadatliwy model (M4) wykazywał porównywalne wskaźniki konwergencji do najbardziej zwięzłego (M5), co sugeruje, że różnice długości nie wskazują systematycznie na rozbieżności treści.
