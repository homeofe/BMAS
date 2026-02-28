# 🎯 8. Conclusion

Ce travail a introduit **Blind Multi-Agent Synthesis (BMAS)**, une méthodologie pour éliciter, comparer et synthétiser les réponses de plusieurs grands modèles de langage dans une isolation stricte, et a présenté des résultats empiriques d'une expérience de 540 lancements sur douze LLMs frontier et trois strates de domaines.

## 📋 8.1 Résumé des contributions

Nous avons démontré que :

1. **La convergence est dépendante du domaine et mesurable.** Sur 45 prompts, les domaines A et B (technique et réglementaire) ont montré une similarité sémantique inter-modèles systématiquement plus élevée que le domaine C (prompts stratégiques et ambigus). [Voir la section 4 pour les valeurs exactes.]

2. **La divergence signale l'erreur dans les domaines factuels.** Les modèles identifiés comme valeurs aberrantes sémantiques par le clustering DBSCAN ont montré une précision factuelle plus faible par rapport aux réponses de référence pré-enregistrées que les modèles non-aberrants, soutenant l'hypothèse H2. Cela fournit une base empirique pour l'utilisation de la divergence comme portail de qualité pratique dans les systèmes de décision assistés par IA.

3. **La qualité de la synthèse varie selon la stratégie et le domaine.** La synthèse LLM-as-Judge (S3) a produit la précision factuelle la plus élevée sur les domaines A et B, tandis que le vote majoritaire (S1) a fourni la couverture la plus complète. Le centroïde sémantique (S2) a mieux fonctionné comme résumé représentatif concis. Aucune stratégie unique n'a dominé tous les types de prompts.

4. **La longueur des tokens n'est pas un proxy de qualité.** Nous avons observé une variation significative du nombre de tokens de réponse entre modèles sur des prompts identiques (jusqu'à un ratio de 6,5 pour certains prompts), sans corrélation cohérente entre la longueur de réponse et la précision factuelle. Gemini 2.5-pro était systématiquement le plus verbeux ; Sonar le plus concis. Ces différences stylistiques ne prédisent pas la convergence.

## 8.2 Enseignements pratiques

Pour les praticiens déployant des LLMs dans des environnements réglementés ou à enjeux élevés, BMAS suggère une architecture pratique : exécuter les prompts sur plusieurs fournisseurs de modèles indépendants, mesurer la convergence sémantique et router les réponses à faible confiance (forte divergence) vers une revue humaine. La charge est justifiée par le gain de fiabilité, particulièrement pour les questions critiques de conformité où une seule mauvaise réponse a des conséquences juridiques ou de sécurité.

Le protocole de pré-enregistrement utilisé dans cette étude - verrouiller les réponses de référence avant tout lancement de modèle - est transférable à tout effort d'évaluation multi-modèles et prévient les biais de confirmation qui peuvent survenir lorsque les évaluateurs connaissent les réponses avant de concevoir les métriques.

## 8.3 Relation avec AAHP et failprompt

BMAS a été développé dans le contexte d'AAHP (AI-to-AI Handoff Protocol), un cadre structuré d'orchestration multi-agents pour les pipelines d'IA en production, et de failprompt, un outil CLI pour valider les réponses IA dans les environnements CI/CD. Ensemble, ces trois projets forment un toolkit intégré pour le déploiement responsable d'IA multi-modèles : AAHP fournit la couche d'orchestration, failprompt fournit le portail CI, et BMAS fournit la base empirique pour comprendre quand et pourquoi le consensus multi-modèles est plus fiable que la sortie d'un modèle unique.

Tous les codes, prompts, réponses de référence pré-enregistrées et résultats expérimentaux sont publiés en tant que jeux de données ouverts pour soutenir la réplication et l'extension de ce travail.

---

*Le jeu de données BMAS, le runner, le pipeline de métriques et le code de synthèse sont disponibles à l'adresse : https://github.com/homeofe/BMAS*
