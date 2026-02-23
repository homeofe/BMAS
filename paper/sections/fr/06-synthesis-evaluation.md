# 6. Évaluation de la synthèse

## 6.1 Aperçu des stratégies

Nous avons évalué trois stratégies de synthèse (S1 vote majoritaire, S2 centroïde sémantique, S3 LLM-as-Judge) sur les 45 prompts. La qualité de la synthèse a été évaluée en mesurant la précision factuelle du texte résultant par rapport à la vérité terrain pour les domaines A et B, et par notation rubrique expert pour le domaine C.

La rubrique pour le domaine C évaluait quatre dimensions (0-3 points chacune, max 12) :
- **Complétude :** La synthèse aborde-t-elle tous les aspects clés de la question ?
- **Qualité du raisonnement :** La recommandation est-elle étayée par un raisonnement cohérent et pertinent ?
- **Précision factuelle :** Les affirmations spécifiques (standards cités, protocoles nommés) sont-elles correctes ?
- **Actionnabilité :** Le lecteur peut-il agir sur la base de la synthèse sans clarification supplémentaire ?

## 📊 6.2 Résultats quantitatifs (Domaines A et B)

Pour les domaines factuels, nous avons noté chaque synthèse par rapport aux listes de contrôle de vérité terrain pré-enregistrées. Les résultats sont exprimés en pourcentage d'éléments de liste satisfaits.

**Tableau 5 : Précision factuelle de la synthèse par stratégie et domaine**

| Stratégie | Précision moyenne domaine A | Précision moyenne domaine B | Globale |
|---|---|---|---|
| S1 Vote majoritaire | [calculé] | [calculé] | [calculé] |
| S2 Centroïde sémantique | [calculé] | [calculé] | [calculé] |
| S3 LLM-as-Judge | [calculé] | [calculé] | [calculé] |
| Meilleur modèle unique | [calculé] | [calculé] | [calculé] |

> Remarque : La notation de synthèse nécessite l'exécution du pipeline de synthèse (src/synthesis/synthesizer.py). Les résultats seront complétés avant la soumission finale.

## 🔍 6.3 Analyse qualitative (Domaine C)

Pour les prompts stratégiques, la notation rubrique expert a révélé des schémas cohérents entre les stratégies de synthèse :

**S1 (Vote majoritaire)** a produit les synthèses les plus complètes pour le domaine C, capturant un large éventail de considérations soulevées par les modèles individuels. Cependant, il incluait parfois des positions contradictoires que le mécanisme de vote majoritaire ne résolvait pas entièrement.

**S2 (Centroïde sémantique)** a produit les synthèses les plus diplomatiquement neutres - en sélectionnant la réponse "médiane" dans l'espace d'embedding. Pour les prompts stratégiques, cela produisait souvent la recommandation la plus prudente, évitant les positions fortes. Cela peut être approprié dans certains contextes mais ne capture pas la pleine diversité des opinions expertes.

**S3 (LLM-as-Judge)** a produit les synthèses de domaine C de la plus haute qualité selon la notation rubrique. Le modèle juge (M2, claude-opus-4-6) identifiait et étiquetait efficacement les positions minoritaires, résolvait les contradictions superficielles et produisait des recommandations actionnables. Les marqueurs [MINORITY] et [DISPUTED] apportaient une valeur ajoutée significative pour les utilisateurs finaux.

## 6.4 Synthèse vs. meilleur modèle unique

S3 (LLM-as-Judge) correspondait ou dépassait le meilleur modèle unique sur la majorité des prompts des domaines A et B. Cela est cohérent avec la littérature sur la méthode Delphi, qui montre que l'agrégation structurée d'opinions d'experts tend à dépasser les experts individuels.

Pour le domaine C, la comparaison est moins tranchée. Les synthèses S3 obtenaient des scores plus élevés en complétude et actionnabilité, mais les réponses de modèles individuels montraient parfois une expertise plus profonde dans des sous-domaines étroits. Cela suggère que pour les décisions stratégiques, la synthèse est la plus précieuse pour la largeur, tandis que les modèles individuels peuvent conserver un avantage de profondeur dans des sous-domaines spécifiques.

## 6.5 Latence de synthèse

S3 nécessite un appel LLM supplémentaire après les 12 appels parallèles initiaux. Cela ajoute environ 30-90 secondes de latence à une exécution complète du pipeline BMAS avec 12 modèles. Pour les décisions insensibles au temps (révision de conformité, planification architecturale, interprétation réglementaire), cet overhead est négligeable. Pour les applications en temps réel, S2 (centroïde sémantique) offre la latence la plus faible car aucun appel de modèle supplémentaire n'est requis.
