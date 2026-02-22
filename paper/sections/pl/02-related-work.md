# 2. Prace pokrewne

BMAS opiera się na metodach strukturalnego konsensusu eksperckiego, technikach LLM wielopróbkowych i wielomodelowych, zautomatyzowanych metrykach oceny oraz klasteryzacji opartej na gęstości. Niniejsza sekcja omawia każdy z tych obszarów i wyjaśnia pozycjonowanie BMAS względem wcześniejszych prac.

## 2.1 Metoda Delphi

Dalkey i Helmer (1963) wprowadzili metodę Delphi w RAND Corporation jako ustrukturyzowane podejście do prognozowania eksperckiego. W oryginalnym protokole panel ekspertów dostarczał niezależnych oszacowań bez znajomości odpowiedzi innych, a moderator agregował wyniki w wielu iteracyjnych rundach. Centralna siła metody polegała na tym, że izolacja zapobiegała zakotwiczeniu i myśleniu grupowemu, umożliwiając ujawnienie prawdziwych rozbieżności zanim poszukiwano konsensusu. BMAS przejmuje tę zasadę izolacji bezpośrednio: każdy LLM odpowiada na prompty bez obserwowania wyników jakiegokolwiek innego modelu, zapewniając, że konwergencja, gdy następuje, odzwierciedla niezależne rozumowanie, a nie imitację.

## 2.2 Self-Consistency

Wang et al. (2022) zaproponowali self-consistency jako strategię dekodowania, która próbkuje wiele łańcuchów rozumowania z jednego modelu językowego i wybiera końcową odpowiedź przez głosowanie większościowe. Metoda wykazała znaczące ulepszenia na benchmarkach rozumowania arytmetycznego i rozumowania zdrowego rozsądku. Jednak ponieważ wszystkie łańcuchy rozumowania pochodzą z tego samego modelu, self-consistency rejestruje tylko wariancję dekodowania wewnątrzmodelowego, nie głębsze różnice w danych treningowych, architekturze i wyrównaniu, które rozróżniają różnych dostawców. BMAS rozszerza intuicję konwergencji-jako-sygnału-jakości na ramy międzyoperatorskie.

## 2.3 Mixture of Agents

Wang et al. (2024) wprowadzili framework Mixture-of-Agents (MoA), w którym wiele LLM uczestniczy w iteracyjnych rundach agregacji, gdzie każdy model może obserwować i udoskonalać wyniki innych. MoA wykazał, że współpracujące doskonalenie między modelami poprawia wydajność na benchmarkach takich jak AlpacaEval i MT-Bench. Krytyczna różnica w stosunku do BMAS polega na tym, że MoA nie jest ślepy: modele w późniejszych rundach są narażone na poprzednie wyniki, co wprowadza ryzyko propagacji błędów. BMAS celowo tego unika, wymuszając ścisłą izolację podczas fazy odpowiedzi i odkładając wszelkie interakcje między modelami do oddzielnej fazy syntezy.

## 2.4 LLM-as-Judge

Zheng et al. (2023) zbadali użycie dużych modeli językowych jako oceniających wyniki innych modeli, wprowadzając benchmarki MT-Bench i Chatbot Arena. Ich praca wykazała, że silne LLM mogą służyć jako skalowalne proxy dla oceny ludzkiej. W BMAS rola sędziego jest ograniczona do jednej z trzech strategii syntezy (S3): szósty model syntezuje pięć ślepych odpowiedzi w jeden wynik, ale poprawność jest mierzona względem pre-rejestrowanych odpowiedzi referencyjnych, nie preferencji sędziego.

## 2.5 BERTScore

Zhang et al. (2020) zaproponowali BERTScore, automatyczną metrykę oceny obliczającą podobieństwo na poziomie tokenów między tekstami kandydackimi a referencyjnymi przy użyciu kontekstowych embeddingów z pre-trenowanych modeli transformer. W przeciwieństwie do metryk nakładania się n-gramów, takich jak BLEU czy ROUGE, BERTScore rejestruje równoważność semantyczną w różnych formach powierzchniowych i jest odporna na parafrazę. BMAS przyjmuje BERTScore F1 jako główną metrykę podobieństwa parowego do mierzenia konwergencji między modelami.

## 2.6 Constitutional AI

Bai et al. (2022) wprowadzili Constitutional AI (CAI) w Anthropic, metodologię szkolenia, w której model krytykuje i poprawia własne wyniki zgodnie z zestawem zasad. BMAS można postrzegać jako rozszerzenie intuicji krytyki-i-rewizji z pętli jednomodelowej na ramy wielomodelowe i wielodostawcowe: zamiast jednego modelu oceniającego samego siebie, wiele niezależnie przeszkolonych modeli służy jako niejawni krytycy dla siebie nawzajem poprzez sygnał dywergencji.

## 2.7 DBSCAN

Ester et al. (1996) zaproponowali DBSCAN (Density-Based Spatial Clustering of Applications with Noise), algorytm klasteryzacji grupujący punkty danych na podstawie gęstości łączności i identyfikujący punkty w obszarach niskiej gęstości jako szum lub wartości odstające. W przeciwieństwie do k-średnich, DBSCAN nie wymaga a priori określenia liczby klastrów. BMAS stosuje DBSCAN w przestrzeni embeddingowej odpowiedzi modeli do wykrywania wyników odstających.

## 2.8 Pozycjonowanie

BMAS jest, zgodnie z naszą wiedzą, pierwszym frameworkiem łączącym cztery właściwości nieobecne w żadnym pojedynczym wcześniejszym podejściu. Po pierwsze, wymusza ślepą izolację międzyoperatorską. Po drugie, wprowadza analizę uwarstwioną według dziedzin. Po trzecie, traktuje dywergencję jako sygnał anomalii, a nie niepowodzenie koordynacji. Po czwarte, dostarcza kontrolowanego porównania strategii syntezy ocenianych względem pre-rejestrowanych odpowiedzi referencyjnych, oferując empiryczne wskazówki dotyczące optymalnej agregacji niezależnych wyników modeli w praktyce.
