# 1. Introduction

Les grands modèles de langage sont désormais suffisamment performants pour être déployés dans des domaines où la précision n'est pas optionnelle : analyse juridique, diagnostic médical, conformité réglementaire et systèmes d'identité gouvernementaux. Dans ces domaines, une réponse confiante mais erronée d'un modèle unique n'est pas un inconvénient mineur - c'est un échec aux conséquences réelles.

L'approche dominante pour améliorer la fiabilité des LLMs est soit un meilleur entraînement (RLHF, Constitutional AI), soit un meilleur prompting (chaîne de pensée, augmentation par récupération). Les deux opèrent dans un paradigme à modèle unique : un modèle, une sortie, une réponse à faire confiance ou non.

Ce travail prend une approche différente. Au lieu de demander "comment rendre un modèle plus fiable ?", nous demandons : **que peut-on apprendre du désaccord entre plusieurs modèles qui ne peuvent pas s'influencer mutuellement ?**

## 1.1 L'insight fondamental

Lorsque cinq experts indépendants répondent à la même question sans se consulter, et que quatre d'entre eux donnent la même réponse tandis qu'un seul donne une réponse différente, nous ne concluons pas que les quatre ont tort. Nous examinons la réponse dissidente plus attentivement, mais nous faisons confiance au consensus comme a priori.

C'est la méthode Delphi, utilisée depuis 1963 pour la prévision d'experts. Sa force est structurelle : **l'isolation prévient la pensée de groupe ; le consensus émerge d'un raisonnement indépendant, non de la pression sociale.**

BMAS applique cette logique aux LLMs. Chaque modèle est un expert avec une distribution d'entraînement particulière, une date limite de connaissance et un ensemble de biais. Lorsqu'ils sont isolés les uns des autres et soumis à la même question, leur convergence ou divergence est elle-même informative.

## 1.2 Ce qui est nouveau

Plusieurs travaux antérieurs sont apparentés mais distincts :

**Self-Consistency** (Wang et al., 2022) génère plusieurs chaînes de raisonnement à partir d'un *seul* modèle et utilise le vote majoritaire. BMAS utilise des modèles *différents* - ceci teste à travers les distributions d'entraînement, pas seulement la variance de décodage.

**Mixture of Agents** (Wang et al., 2024) permet aux modèles de voir les sorties des autres lors de tours d'agrégation. Cela produit un raffinement collaboratif, mais introduit le risque de propagation des erreurs : si un modèle produit une hallucination confiante au premier tour, les modèles suivants peuvent s'y ancrer.

**LLM-as-Judge** (Zheng et al., 2023) utilise un modèle pour évaluer un autre. BMAS utilise un modèle pour *synthétiser* les sorties de plusieurs autres - le rôle de juge est limité à la phase de synthèse finale.

BMAS est le premier cadre à combiner quatre propriétés :
1. Isolation aveugle stricte (aucune contamination croisée)
2. Diversité des modèles (fournisseurs, architectures, distributions d'entraînement différents)
3. Analyse stratifiée par domaine (factuel, réglementaire, stratégique)
4. Divergence comme signal (non comme échec)

## 1.3 Motivation pratique

Cette recherche est née d'une expérience opérationnelle dans la construction d'AEGIS, un système de vérification d'identité gouvernementale transfrontalier de l'UE, et d'AAHP (AI-to-AI Handoff Protocol), un cadre structuré d'orchestration multi-agents. Dans ces deux systèmes, des pipelines multi-agents sont utilisés pour des décisions d'architecture, des analyses de conformité et des revues d'implémentation.

Une question pratique s'est posée : lorsque plusieurs LLMs sont utilisés comme examinateurs indépendants dans un pipeline, dans quelle mesure leurs sorties diffèrent-elles réellement ? Et lorsqu'ils diffèrent, qui a raison ?

BMAS est la réponse formelle à cette question.

## 1.4 Contributions

Ce travail apporte les contributions suivantes :

1. **Méthodologie BMAS :** Un protocole formalisé de synthèse multi-agents aveugle avec contraintes d'isolation, suite de métriques et stratégies de synthèse.
2. **Etude empirique :** Résultats de 30 prompts sur 5 LLMs dans 3 strates de domaines, avec des réponses de référence pré-enregistrées pour les domaines A et B.
3. **Validation de l'hypothèse divergence-comme-signal :** Données statistiques montrant que la divergence inter-modèles prédit le taux d'erreur factuelle.
4. **Comparaison des stratégies de synthèse :** Evaluation empirique du vote majoritaire, du centroïde sémantique et de la synthèse LLM-as-Judge par rapport aux réponses de référence.
5. **Jeu de données ouvert :** Tous les prompts, les sorties brutes des modèles et les scores de métriques sont publiés en tant que benchmark public.

## 1.5 Structure du document

La section 2 examine les travaux connexes. La section 3 décrit la méthodologie BMAS et le design expérimental. La section 4 présente les résultats. La section 5 analyse la corrélation divergence-hallucination. La section 6 évalue les stratégies de synthèse. La section 7 discute des implications, des limites et des travaux futurs. La section 8 conclut.
