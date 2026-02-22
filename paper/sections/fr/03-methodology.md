# 3. Méthodologie

## 3.1 Vue d'ensemble du protocole BMAS

Blind Multi-Agent Synthesis (BMAS) est un protocole en quatre phases pour éliciter, comparer et synthétiser les réponses de plusieurs LLMs sur des prompts identiques. Les quatre phases sont :

1. **Elicitation aveugle** - Chaque modèle reçoit le même prompt sans connaissance de l'étude, des autres modèles ou des autres réponses.
2. **Calcul des métriques** - La similarité sémantique par paires, la précision factuelle et la détection des valeurs aberrantes sont calculées pour toutes les réponses des modèles.
3. **Synthèse** - Trois stratégies de synthèse agrègent les réponses individuelles en une seule sortie.
4. **Evaluation** - Les sorties de synthèse sont évaluées par rapport aux réponses de référence pré-enregistrées (domaines A et B) ou par l'évaluation d'experts (domaine C).

Le protocole impose une stricte **règle de non-contamination** : aucune réponse de modèle n'est rendue disponible à aucun autre modèle à aucune phase avant la synthèse. Cela reflète l'exigence d'isolation de la méthode Delphi et distingue BMAS des approches multi-agents coopératives telles que MoA (Wang et al., 2024).

## 3.2 Modèles

Nous évaluons cinq LLMs de pointe de quatre fournisseurs distincts :

| ID | Modèle | Fournisseur | Fenêtre de contexte |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M tokens |
| M2 | claude-opus-4-6 | Anthropic | 1M tokens |
| M3 | gpt-5.3-codex | OpenAI | 272k tokens |
| M4 | gemini-2.5-pro | Google | 1M tokens |
| M5 | sonar-pro | Perplexity | 127k tokens |

La diversité multi-fournisseurs est délibérée. Les modèles du même fournisseur partagent une lignée architecturale et des pipelines de données d'entraînement, ce qui peut réduire la divergence même dans des conditions aveugles. L'inclusion de modèles de quatre fournisseurs séparés maximise l'indépendance des réponses.

**Implémentation de l'isolation :** Chaque modèle fonctionne dans une session isolée séparée sans contexte partagé. Le prompt système est identique pour tous les modèles :

> *"Vous êtes un assistant expert compétent. Répondez à la question suivante de manière aussi précise et complète que possible. Soyez précis, factuel et structuré. Si vous n'êtes pas certain d'un détail spécifique, indiquez-le explicitement."*

La température n'est pas modifiée. Nous préservons délibérément le comportement d'échantillonnage par défaut de chaque modèle pour capturer la variance naturelle des réponses, non pour la normaliser.

## 3.3 Conception des prompts

### 3.3.1 Structure des domaines

Nous avons construit 30 prompts sur trois strates de domaines :

**Domaine A - Questions techniques de haute précision (A01-A10) :** Questions avec des réponses objectivement correctes vérifiables par rapport à des sources primaires faisant autorité (normes NIST FIPS, NVD, RFCs IETF, spécifications OpenID Foundation). Exemples : justification du scoring CVSS, tailles de clés des algorithmes PQC, énumération des suites de chiffrement TLS 1.3.

**Domaine B - Réglementaire/Conformité (B01-B10) :** Questions fondées sur des textes juridiques et réglementaires avec des sources faisant autorité (RGPD, eIDAS 2.0, NIS2, ISO 27001, BSI C5). Un certain jugement interprétatif est requis aux marges, mais les réponses centrales sont définies dans des textes formels. Exemples : exceptions d'effacement de l'Article 17(3) du RGPD, classifications sectorielles NIS2, différences de niveaux d'évaluation TISAX.

**Domaine C - Stratégique/Ambigu (C01-C10) :** Questions sans réponse unique correcte, nécessitant un jugement d'expert et un raisonnement architectural. Plusieurs positions défendables existent. Exemples : décisions d'architecture zero-trust, priorisation de la migration PQC, arbitrages d'investissements de conformité.

### 3.3.2 Exigences des prompts

Tous les prompts ont été conçus pour satisfaire quatre critères :

1. **Autonome** - répondable sans contexte externe ni récupération de documents
2. **Réponse structurée** - chaque prompt spécifie un format de sortie requis (liste, comparaison, décision avec justification)
3. **Longueur bornée** - réponse attendue de 300-600 tokens pour les domaines A-B ; 400-800 pour le domaine C
4. **Testable** - pour les domaines A et B, une réponse vérifiable existe ; pour le domaine C, l'évaluation par expert est pratiquement réalisable

### 3.3.3 Pré-enregistrement

Suivant les bonnes pratiques de la science ouverte, les réponses de référence pour les domaines A et B ont été documentées et verrouillées avant tout lancement de modèle. Cela prévient les biais de confirmation inconscients dans le scoring. Les documents de réponses de référence sont publiés avec le jeu de données.

Le domaine C n'a pas de réponses de référence pré-enregistrées. L'évaluation par expert (l'auteur principal comme expert du domaine) évalue la qualité de la synthèse selon une rubrique de complétude, de qualité du raisonnement et d'exploitabilité pratique.

## 3.4 Métriques

### 3.4.1 Similarité sémantique (primaire)

Nous calculons la similarité cosinus par paires entre les embeddings de réponses en utilisant le modèle sentence-transformer `all-mpnet-base-v2` (Reimers et Gurevych, 2019). Pour N modèles, cela produit une matrice de similarité N x N par prompt. Nous rapportons :

- **Similarité par paires moyenne (MPS) :** moyenne de tous les scores par paires N(N-1)/2
- **Similarité minimale par paires :** la paire la plus divergente
- **Ecart-type de similarité :** variance au sein du cluster de réponses du prompt

### 3.4.2 BERTScore

Nous calculons BERTScore F1 par paires (Zhang et al., 2020) comme mesure secondaire de similarité sémantique au niveau des tokens. BERTScore capture la proximité lexicale au-delà des embeddings au niveau des phrases et est sensible au chevauchement des affirmations factuelles.

### 3.4.3 Jaccard sur les affirmations clés

Nous extrayons des affirmations factuelles discrètes de chaque réponse en utilisant la segmentation en phrases et calculons la similarité Jaccard par paires sur des ensembles d'affirmations normalisées. Cette métrique capture l'accord structurel - si les modèles identifient les mêmes points clés - indépendamment de la formulation.

### 3.4.4 Détection des valeurs aberrantes

Nous appliquons DBSCAN (Ester et al., 1996) à l'espace d'embedding avec eps=0.15 (équivalent à une similarité cosinus inférieure à 0.85) et min_samples=2. Les modèles dont les embeddings tombent en dehors de tous les clusters de voisinage reçoivent une étiquette aberrante (-1). Nous traitons le statut d'aberrant comme un signal de hallucination potentielle dans les domaines A et B, et comme indicateur de point de vue minoritaire dans le domaine C.

### 3.4.5 Précision factuelle (domaines A et B uniquement)

Pour chaque réponse des domaines A et B, nous évaluons la précision factuelle par rapport à la liste de contrôle des réponses de référence pré-enregistrées. Chaque item de la liste de contrôle est binaire (présent et correct, ou absent/incorrect). Le score de précision factuelle est la fraction d'items de la liste de contrôle satisfaits.

## 3.5 Stratégies de synthèse

Nous évaluons trois stratégies de synthèse :

**S1 - Vote majoritaire (niveau des affirmations) :** Les affirmations factuelles sont extraites de toutes les réponses. Une affirmation est acceptée dans la synthèse si elle apparaît dans les réponses d'au moins 60 % des modèles (trois sur cinq). Les affirmations minoritaires (sous le seuil) sont ajoutées avec un marqueur [MINORITY].

**S2 - Centroïde sémantique :** La réponse dont l'embedding est le plus proche de la moyenne de tous les embeddings de réponses est sélectionnée comme base de synthèse. Cela capture la réponse individuelle la plus "représentative". Aucun nouveau contenu n'est ajouté.

**S3 - LLM-as-Judge :** Les cinq réponses anonymisées sont présentées à une sixième instance de modèle (M2, claude-opus-4-6) avec pour instruction de produire une synthèse faisant autorité unique, en marquant les affirmations minoritaires ([MINORITY]) et les contradictions ([DISPUTED]). Le modèle juge ne reçoit aucune information identifiant quel modèle a produit quelle réponse.

La qualité de la synthèse est évaluée en mesurant la précision factuelle du texte résultant par rapport aux réponses de référence pré-enregistrées (domaines A et B) et par scoring selon une rubrique d'expert (domaine C).

## 3.6 Hypothèses

Nous testons trois hypothèses pré-enregistrées :

**H1 (Convergence dans les domaines factuels) :** La similarité sémantique par paires moyenne pour les prompts des domaines A et B dépassera 0.75 (BERTScore F1).

**H2 (La divergence signale l'erreur) :** Parmi les réponses des domaines A et B, les modèles aberrants (label DBSCAN -1) auront des scores de précision factuelle significativement plus faibles que les modèles non-aberrants (test t unilatéral, alpha=0.05).

**H3 (Effet du domaine sur la convergence) :** La similarité par paires moyenne pour le domaine C sera significativement plus faible que pour les domaines A et B (ANOVA à sens unique, Tukey HSD post-hoc, alpha=0.05).

## 3.7 Configuration expérimentale

Tous les lancements de modèles ont été exécutés via la passerelle OpenClaw, qui route indépendamment vers l'API de chaque fournisseur. Chaque prompt s'exécute dans une session isolée séparée sans état partagé. Les sorties des lancements sont stockées en JSON structuré avec l'ID du prompt, l'ID du modèle, le texte de la réponse, le nombre de tokens et la latence. Le jeu de données complet de 150 lancements (30 prompts x 5 modèles) est publié avec ce travail.
