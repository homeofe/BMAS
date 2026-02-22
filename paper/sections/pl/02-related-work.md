# 2. Prace pokrewne

BMAS opiera sie na metodach strukturalnego konsensusu eksperckiego, technikach LLM wieloprobkowych i wielomodelowych, zautomatyzowanych metrykach oceny oraz klasteryzacji opartej na gestosci. Niniejsza sekcja omawia kazdy z tych obszarow i wyjasnia pozycjonowanie BMAS wzgledem wczesniejszych prac.

## 2.1 Metoda Delphi

Dalkey i Helmer (1963) wprowadzili metode Delphi w RAND Corporation jako ustrukturyzowane podejscie do prognozowania eksperckiego. W oryginalnym protokole panel ekspertow dostarczal niezaleznych oszacowan bez znajomosci odpowiedzi innych, a moderator agregował wyniki w wielu iteracyjnych rundach. Centralna sila metody polegala na tym, ze izolacja zapobiegala zakotwiczeniu i mysleniu grupowemu, umozliwiajac ujawnienie prawdziwych rozbieznosci zanim poszukiwano konsensusu. BMAS przejmuje te zasade izolacji bezposrednio: kazdy LLM odpowiada na prompty bez obserwowania wynikow jakiegokolwiek innego modelu, zapewniajac, ze konwergencja, gdy nastepuje, odzwierciedla niezalezne rozumowanie, a nie imitacje.

## 2.2 Self-Consistency

Wang et al. (2022) zaproponowali self-consistency jako strategie dekodowania, ktora probkuje wiele lancuchow rozumowania z jednego modelu jezykowego i wybiera koncowa odpowiedz przez glosowanie wiekszosciowe. Metoda wykazala znaczace ulepszenia na benchmarkach rozumowania arytmetycznego i rozumowania zdrowego rozsadku. Jednak poniewaz wszystkie lancuchy rozumowania pochodza z tego samego modelu, self-consistency rejestruje tylko wariancje dekodowania wewnatrzmodelowego, nie glębsze roznice w danych treningowych, architekturze i wyrownaniu, ktore rozrozniaja roznych dostawcow. BMAS rozszerza intuicje konwergencji-jako-sygnalu-jakosci na ramy miedzyoperatorskie.

## 2.3 Mixture of Agents

Wang et al. (2024) wprowadzili framework Mixture-of-Agents (MoA), w ktorym wiele LLM uczestniczy w iteracyjnych rundach agregacji, gdzie kazdy model moze obserwowac i udoskonalac wyniki innych. MoA wykazal, ze wspolpracujace doskonalenie miedzy modelami poprawia wydajnosc na benchmarkach takich jak AlpacaEval i MT-Bench. Krytyczna roznica w stosunku do BMAS polega na tym, ze MoA nie jest slepy: modele w pozniejszych rundach sa narazone na poprzednie wyniki, co wprowadza ryzyko propagacji bledow. BMAS celowo tego unika, wymuszajac scisla izolacje podczas fazy odpowiedzi i odkladajac wszelkie interakcje miedzymodelowe do oddzielnej fazy syntezy.

## 2.4 LLM-as-Judge

Zheng et al. (2023) zbadali uzycie duzych modeli jezykowych jako oceniajacych wyniki innych modeli, wprowadzajac benchmarki MT-Bench i Chatbot Arena. Ich praca wykazala, ze silne LLM moga sluzyc jako skalowalne proxy dla oceny ludzkiej. W BMAS rola sedziego jest ograniczona do jednej z trzech strategii syntezy (S3): szosty model syntezuje piec slepych odpowiedzi w jeden wynik, ale poprawnosc jest mierzona wzgledem pre-rejestrowanych odpowiedzi referencyjnych, nie preferencji sedziego.

## 2.5 BERTScore

Zhang et al. (2020) zaproponowali BERTScore, automatyczna metryke oceny obliczajaca podobienstwo na poziomie tokenow miedzy tekstami kandydackimi a referencyjnymi przy uzyciu kontekstowych embeddingow z pre-trenowanych modeli transformer. W przeciwienstwie do metryk nakladania sie n-gramow, takich jak BLEU czy ROUGE, BERTScore rejestruje rownowaznosc semantyczna w roznych formach powierzchniowych i jest odporna na parafraze. BMAS przyjmuje BERTScore F1 jako glowna metryke podobienstwa parowego do mierzenia konwergencji miedzymodelowej.

## 2.6 Constitutional AI

Bai et al. (2022) wprowadzili Constitutional AI (CAI) w Anthropic, metodologie szkolenia, w ktorej model krytykuje i poprawia wlasne wyniki zgodnie z zestawem zasad. BMAS mozna postrzegac jako rozszerzenie intuicji krytyki-i-rewizji z petli jednomodelowej na ramy wielomodelowe i wielodostawcowe: zamiast jednego modelu oceniajacego samego siebie, wiele niezaleznie przeszkolonych modeli sluzy jako niejawni krytycy dla siebie nawzajem poprzez sygnal dywergencji.

## 2.7 DBSCAN

Ester et al. (1996) zaproponowali DBSCAN (Density-Based Spatial Clustering of Applications with Noise), algorytm klasteryzacji grupujacy punkty danych na podstawie gestosci lacznosci i identyfikujacy punkty w obszarach niskiej gestosci jako szum lub wartosci odstajace. W przeciwienstwie do k-sredni, DBSCAN nie wymaga a priori okreslenia liczby klastrow. BMAS stosuje DBSCAN w przestrzeni embeddingowej odpowiedzi modeli do wykrywania wynikow odstajacych.

## 2.8 Pozycjonowanie

BMAS jest, zgodnie z nasza wiedza, pierwszym frameworkiem laczacym cztery wlasciwosci nieobecne w zadnym pojedynczym wczesniejszym podejsciu. Po pierwsze, wymusza slepa izolacje miedzyoperatorska. Po drugie, wprowadza analize uwarstwiona wedlug dziedzin. Po trzecie, traktuje dywergencje jako sygnal anomalii, a nie niepowodzenie koordynacji. Po czwarte, dostarcza kontrolowanego porownania strategii syntezy ocenianych wzgledem pre-rejestrowanych odpowiedzi referencyjnych, oferujac empiryczne wskazowki dotyczace optymalnej agregacji niezaleznych wynikow modeli w praktyce.
