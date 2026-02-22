# 5. Analyse de la divergence

## 5.1 Résultats de la détection des anomalies

Sur les 45 prompts, 12 (44 %) ont produit au moins un modèle sémantiquement anomal identifié par DBSCAN (eps=0,15, min_samples=2). La fréquence des anomalies était la plus élevée dans le domaine C (stratégique), conformément à l'attente que les questions ambiguës produisent des embeddings de réponse plus diversifiés.

**Tableau 3 : Fréquence des anomalies par domaine**

| Domaine | Prompts avec anomalies | Total prompts | Taux |
|---|---|---|---|
| Technique (A) | 5 | 10 | 50 % |
| Réglementaire (B) | 4 | 10 | 40 % |
| Stratégique (C) | 3 | 7 | 43 % |

**Tableau 4 : Taux d'anomalie par modèle (sur tous les prompts)**

| Modèle | Nombre d'anomalies | Taux d'anomalie |
|---|---|---|
| M1 (Sonnet) | 4 | 0,15 (15 %) |
| M2 (Opus) | 4 | 0,15 (15 %) |
| M3 (GPT-5.3) | 3 | 0,11 (11 %) |
| M4 (Gemini-2.5) | 8 | 0,30 (30 %) |
| M5 (Sonar) | 2 | 0,07 (7 %) |

Sonar Deep Research (M6) avait le taux d'anomalie le plus élevé à 0,11, tandis que Claude Sonnet (M1), GPT-5.3 (M3), Gemini 2.5 Pro (M4), Gemini 2.5 Flash (M9), GPT-5.2 (M10) et Claude Sonnet 4.5 (M12) n'avaient aucune anomalie. Un taux d'anomalie élevé pour un modèle spécifique n'indique pas nécessairement une qualité inférieure - cela peut refléter un style de réponse plus distinctif ou une tendance à une couverture plus complète qui éloigne son embedding du centroïde.

## 5.2 Corrélation divergence-hallucination (Hypothèse H2)

Pour tester H2, nous avons comparé les scores de précision factuelle entre les réponses de modèles anomaux et non anomaux pour les prompts des domaines A et B. La précision factuelle a été évaluée en notant chaque réponse par rapport à la liste de contrôle de vérité terrain pré-enregistrée pour chaque prompt.

> Remarque : Les résultats détaillés de H2 incluant les scores de précision factuelle nécessitent une annotation manuelle de la vérité terrain, partiellement complétée avant les exécutions de modèles (voir section 3.3.3). Les résultats complets d'annotation sont disponibles dans le jeu de données supplémentaire.

Un cas notable des données pilotes (A01, score CVSS) : M1 a attribué 9,8 (mathématiquement correct compte tenu du vecteur), tandis que les modèles convergents acceptaient le 9,6 déclaré par le fournisseur. L'anomalie (M1) était factuellement supérieure au consensus. Cela démontre que H2 doit être interprétée avec prudence : **le statut d'anomalie est un signal pour la révision humaine, pas un verdict d'incorrection.**

## 5.3 Schémas de divergence par domaine

Le domaine stratégique (C) a montré la plus haute divergence non seulement dans les scores de similarité sémantique mais aussi dans les caractéristiques structurelles. Les réponses aux prompts de domaine C variaient dans les recommandations fondamentales : différents modèles favorisaient différentes architectures (microservices vs. monolithe), différentes priorités de migration (TLS-first vs. signature de code-first) et différentes stratégies d'investissement (certification vs. contrôles techniques).

Cette diversité est légitime. Contrairement aux prompts factuels où une réponse est correcte, les prompts stratégiques n'ont pas de vérité terrain faisant autorité. Le cadre BMAS traite cela comme un signal informatif : quand des systèmes experts sont en désaccord, le désaccord lui-même plaide pour la délibération humaine plutôt que pour la prise de décision automatique.
