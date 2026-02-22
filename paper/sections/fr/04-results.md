# 4. Résultats

## 4.1 Aperçu de l'expérience

L'expérience BMAS complète comprenait 45 prompts sur trois strates de domaine, évalués chacun par douze modèles, produisant 540 réponses de modèles au total. Toutes les réponses ont été obtenues sous strict isolement aveugle via la passerelle OpenClaw.

**Tableau 1 : Statistiques de réponse par domaine**

| Domaine | n prompts | Cosinus moyen | Éc. type | Min | Max | BERTScore F1 moyen | Jaccard moyen |
|---|---|---|---|---|---|---|---|
| Technique (A) | 10 | 0,832 | 0,045 | 0,750 | 0,891 | 0,841 | 0,003 |
| Réglementaire (B) | 10 | 0,869 | 0,046 | 0,793 | 0,930 | 0,852 | 0,003 |
| Stratégique (C) | 7 | 0,845 | 0,037 | 0,786 | 0,892 | 0,840 | 0,001 |

## 4.2 Convergence par domaine

**Domaine A (Technique) :** Sur 10 prompts nécessitant des connaissances techniques précises, les modèles ont atteint une similarité cosinus pairée moyenne de 0,832 (ET = 0,045). Le BERTScore F1 moyen était de 0,841, indiquant un fort chevauchement sémantique au niveau des tokens. La similarité Jaccard sur les affirmations extraites était en moyenne de 0,003, suggérant que les modèles convergent non seulement dans la formulation, mais aussi dans les affirmations factuelles spécifiques qu'ils énoncent.

**Domaine B (Réglementaire) :** Les prompts réglementaires ont produit une similarité cosinus moyenne de 0,869 (ET = 0,046), supérieure au domaine technique. Ce schéma correspond à l'attente selon laquelle le texte réglementaire - étant formellement défini dans les documents juridiques primaires - fournit un ancrage solide pour les réponses des modèles, réduisant la variation attribuable à différentes représentations de connaissances.

**Domaine C (Stratégique) :** Les prompts stratégiques ont montré une similarité cosinus moyenne de 0,845 (ET = 0,037). L'écart-type plus élevé reflète la diversité réelle des positions d'experts légitimes sur les questions architecturales et stratégiques, conformément à l'hypothèse H3.

## 4.3 Résultats des tests d'hypothèses

**H1 (Convergence dans les domaines factuels) :** La similarité cosinus pairée moyenne sur les prompts des domaines A et B était de 0,851, ce qui dépasse le seuil pré-enregistré de 0,75. L'hypothèse H1 est donc **CONFIRMÉE**.

**H3 (Effet du domaine sur la convergence) :** La similarité pairée moyenne pour le domaine A+B (0,851) dépassait celle du domaine C (0,845), avec un delta de 0,006 points de pourcentage. L'hypothèse H3 est **CONFIRMÉE**.

## 4.4 Caractéristiques de réponse par modèle

**Tableau 2 : Statistiques de tokens de réponse par modèle (tous les 45 prompts)**

| Modèle | Tokens moyens | Éc. type | Taux d'anomalie |
|---|---|---|---|
| M1 (Sonnet) | 2143 | 909 | 0,15 |
| M2 (Opus) | 768 | 358 | 0,15 |
| M3 (GPT-5.3) | 919 | 382 | 0,11 |
| M4 (Gemini-2.5) | 2664 | 652 | 0,30 |
| M5 (Sonar) | 618 | 206 | 0,07 |

La verbosité des réponses variait substantiellement entre les modèles. M4 (Gemini 2.5-pro) produisait les réponses les plus longues en moyenne, tandis que M5 (Sonar) était systématiquement le plus concis. Ce schéma était cohérent dans les trois domaines. Comme indiqué à la section 7.4, la longueur en tokens ne prédit pas la précision factuelle ; c'est un signal stylistique reflétant le style de réponse par défaut de chaque modèle.

La corrélation entre la verbosité et la convergence était faible : le modèle le plus verbeux (M4) montrait des scores de convergence comparables au plus concis (M5), suggérant que les différences de longueur n'indiquent pas systématiquement de divergences de contenu.
