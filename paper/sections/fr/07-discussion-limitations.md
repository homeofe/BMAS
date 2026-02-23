# 💡 7. Discussion

## 7.1 Interprétation de la convergence et de la divergence

L'affirmation centrale de BMAS est que la convergence inter-modèles est informative - non seulement comme propriété statistique de l'expérience, mais comme signal pratique pour les applications en aval. Nos résultats [voir section 4] soutiennent cette affirmation pour les domaines factuels tout en révélant des nuances importantes.

Une forte convergence dans les domaines A et B valide l'intuition selon laquelle des modèles bien calibrés, entraînés sur les mêmes sources faisant autorité, tendent vers les mêmes réponses correctes lorsque les questions sont sans ambiguité. Ce n'est pas un résultat trivial : il suggère que pour la vérification de conformité, l'interprétation réglementaire et la citation des normes techniques, un consensus de plusieurs modèles indépendants peut substituer - ou au moins augmenter - la revue par un seul expert dans des contextes critiques en temps.

Une faible convergence dans le domaine C (prompts stratégiques et ambigus) est également informative. Plutôt que de représenter un échec des modèles, elle reflète la difficulté épistémique réelle des questions. Lorsque douze systèmes experts indépendants ne s'accordent pas sur des décisions d'architecture optimales ou des arbitrages d'investissements de sécurité, le désaccord lui-même est significatif - il signale que la question n'a pas de réponse correcte dominante et mérite une délibération humaine. BMAS sert ainsi d'**oracle de complexité** en plus d'un signal de qualité.

## 7.2 Le lien divergence-hallucination

Notre analyse des valeurs aberrantes [voir section 5] fournit des preuves préliminaires pour l'hypothèse divergence-comme-signal. Les modèles identifiés comme valeurs aberrantes dans l'espace d'embedding tendent à avoir des scores de précision factuelle plus faibles, suggérant que l'isolation sémantique par rapport au cluster de consensus corrèle avec la déviation factuelle par rapport à la vérité de référence.

Ce résultat a des implications pratiques pour le déploiement de l'IA dans les industries réglementées. Un système de production implémentant une surveillance de type BMAS pourrait signaler les réponses qui s'écartent significativement du cluster de consensus pour une revue humaine, réduisant la dépendance à la vérification manuelle de chaque sortie de modèle tout en maintenant des garanties de précision.

Nous avertissons cependant que la corrélation n'est pas la causalité. Une réponse aberrante peut être correcte tandis que le consensus est erroné - particulièrement pour des informations publiées récemment ou des connaissances spécifiques à un domaine peu représentées dans les données d'entraînement de la plupart des modèles. La réponse de M1 à A01 (scoring CVSS de CVE-2024-21762) l'a démontré : le score aberrant était mathématiquement correct tandis que les modèles consensuels acceptaient le score indiqué par le vendeur, qui diffère en raison d'une convention d'arrondi. Toute implémentation de production d'un filtrage basé sur la divergence doit conserver une capacité de dérogation humaine.

## 7.3 Comparaison des stratégies de synthèse

Les trois stratégies de synthèse évaluées - vote majoritaire (S1), centroïde sémantique (S2) et LLM-as-Judge (S3) - présentent chacune des compromis distincts [voir section 6].

S1 (vote majoritaire) produit une couverture complète mais peut être verbeux et inclure occasionnellement des affirmations minoritaires à faible confiance malgré le seuil de 60 %. Il est le plus approprié lorsque la complétude est prioritaire sur la concision.

S2 (centroïde sémantique) produit de manière fiable la réponse la plus "moyenne" - informative comme benchmark mais pouvant masquer des insights minoritaires importants. Il fonctionne mieux lorsqu'une réponse représentative unique est nécessaire et que la question est bien contrainte.

S3 (LLM-as-Judge) produit la précision factuelle la plus élevée pour les domaines A et B [voir section 6] mais introduit une nouvelle dépendance : les biais propres du modèle juge. Lorsque le modèle juge est lui-même une valeur aberrante sur un prompt donné, sa synthèse peut systématiquement sous-représenter le point de vue majoritaire. L'utilisation d'un modèle réservé (un qui n'a pas participé au run aveugle) comme juge atténue ce risque.

## ⚠️ 7.4 Limites

**Taille de l'échantillon.** Avec 45 prompts sur trois domaines, cette étude établit des preuves initiales pour la méthodologie BMAS mais ne permet pas une généralisation statistique large. Une étude de suivi avec 100+ prompts par domaine renforcerait substantiellement les affirmations.

**Sélection des modèles.** Les douze modèles utilisés représentent un échantillon de commodité de modèles frontier accessibles au moment de l'étude. La composition des modèles affecte la distribution du consensus : une étude utilisant douze modèles Anthropic montrerait des caractéristiques de variance différentes d'une étude inter-fournisseurs. Les travaux futurs devraient faire varier systématiquement la composition des modèles.

**Qualité des réponses de référence.** Les réponses de référence pour les domaines A et B ont été compilées par recherche sur le web par rapport à des sources primaires. Trois items ont été signalés comme nécessitant une vérification manuelle (discordance CVSS de A01, accès à la source BSI de A10, référence aux directives EDPB de B09). Ces items sont notés dans le jeu de données mais peuvent introduire de légères inexactitudes de scoring.

**Validité temporelle.** Les dates limites de connaissance et les versions de modèles des LLMs évoluent. Les résultats rapportés ici reflètent des versions de modèles spécifiques à un moment précis. Les études de réplication devraient documenter précisément la version du modèle et la date limite de connaissance.

**Température et échantillonnage.** Nous n'avons pas contrôlé la température entre les modèles. Le comportement d'échantillonnage par défaut a été préservé pour capturer la variance naturelle des modèles. Cela signifie qu'une partie de la variance observée peut être attribuable à la stochasticité de décodage plutôt qu'à de vraies différences de connaissances. Une réplication à température contrôlée isolerait cette variable.

**La longueur des tokens n'est pas une densité d'information.** Notre observation selon laquelle M4 (Gemini 2.5-pro) produit systématiquement plus de tokens n'implique pas une plus grande précision ou complétude. Le nombre de tokens est un signal stylistique, pas un signal de qualité. Toutes les affirmations de précision factuelle sont basées sur le scoring par rapport aux réponses de référence, pas sur la longueur des réponses.

## 7.5 Implications pour le déploiement de l'IA

BMAS a trois implications directes pour le déploiement :

**1. Le consensus comme portail de qualité.** Dans les systèmes d'IA à enjeux élevés (juridique, médical, gouvernemental), une couche de type BMAS peut exécuter plusieurs modèles sur la même requête et retenir la réponse jusqu'à ce que le consensus atteigne un seuil défini. Le désaccord déclenche une revue humaine plutôt qu'une action automatisée.

**2. Routage par domaine.** Les résultats de BMAS suggèrent que pour les requêtes factuelles avec des sources faisant autorité, un seul modèle performant peut être suffisant. La charge multi-modèles est la plus justifiée pour les requêtes stratégiques, ambigues ou nouvelles où le domaine manque d'une réponse de référence faisant autorité unique.

**3. Exigences de diversité.** La performance de BMAS dépend de la diversité des modèles. Deux modèles très similaires du même fournisseur ajoutent moins d'information que deux modèles de familles architecturales différentes. Les décisions d'acquisition pour les systèmes d'IA dans les industries réglementées devraient prendre en compte la diversité des fournisseurs en plus des capacités individuelles des modèles.

## 7.6 Travaux futurs

Plusieurs extensions du cadre BMAS méritent d'être étudiées :

- **Etude de dérive temporelle :** exécuter les mêmes prompts sur les mêmes modèles à intervalles de 6 mois pour mesurer si la convergence change lors des mises à jour des modèles
- **Extension des domaines :** étendre au diagnostic médical, à l'analyse financière et au raisonnement juridique
- **Analyse de calibration :** mesurer si la confiance du modèle (lorsqu'elle est exprimée) corrèle avec l'accord de consensus
- **Synthèse adaptative :** développer une stratégie de synthèse qui sélectionne S1, S2 ou S3 dynamiquement en fonction de la convergence mesurée
- **Evaluation humaine :** comparer la qualité de la synthèse BMAS aux réponses d'experts humains en utilisant une évaluation aveugle
