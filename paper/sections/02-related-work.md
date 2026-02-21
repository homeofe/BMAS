# 2. Related Work

BMAS draws on structured expert consensus methods, multi-sample and multi-model LLM techniques, automated evaluation metrics, and density-based clustering. This section reviews each and clarifies how BMAS relates to prior work.

## 2.1 The Delphi Method

Dalkey and Helmer (1963) introduced the Delphi method at the RAND Corporation as a structured approach to expert forecasting. In the original protocol, a panel of experts provided independent estimates without knowledge of one another's responses, and a facilitator aggregated the results across iterative rounds. The method's central strength was that isolation prevented anchoring and groupthink, allowing genuine disagreement to surface before consensus was sought. BMAS borrows this isolation principle directly: each LLM responds to prompts without observing the outputs of any other model, ensuring that convergence, when it occurs, reflects independent reasoning rather than imitation.

## 2.2 Self-Consistency

Wang et al. (2022) proposed self-consistency as a decoding strategy that samples multiple reasoning chains from a single language model and selects the final answer by majority vote. The method demonstrated significant improvements on arithmetic and commonsense reasoning benchmarks by exploiting the intuition that correct reasoning paths are more likely to converge on the same answer than incorrect ones. However, because all reasoning chains originate from the same model, self-consistency captures only intra-model decoding variance, not the deeper differences in training data, architecture, and alignment that distinguish separate providers. BMAS extends the convergence-as-quality-signal intuition to the cross-provider setting, where agreement among independently trained models constitutes a stronger prior for correctness.

## 2.3 Mixture of Agents

Wang et al. (2024) introduced the Mixture-of-Agents (MoA) framework, in which multiple LLMs participate in iterative aggregation rounds where each model can observe and refine the outputs of others. MoA demonstrated that collaborative refinement across models improved performance on benchmarks such as AlpacaEval and MT-Bench, achieving scores competitive with frontier models. The critical difference from BMAS is that MoA is not blind: models in later rounds are exposed to prior outputs, which introduces the risk of error propagation, where a confident hallucination in an early round can anchor subsequent models and suppress legitimate dissent. BMAS deliberately avoids this by enforcing strict isolation throughout the response phase and deferring all cross-model interaction to a separate synthesis stage.

## 2.4 LLM-as-Judge

Zheng et al. (2023) investigated the use of large language models as evaluators of other models' outputs, introducing the MT-Bench and Chatbot Arena benchmarks. Their work showed that strong LLMs could serve as scalable proxies for human evaluation, achieving high agreement with expert annotators on pairwise preference judgments. In BMAS, by contrast, the judge role is confined to one of three synthesis strategies (S3): a sixth model synthesizes the five blind responses into a single output, but correctness is ultimately measured against pre-registered ground truth, not against the judge's preferences.

## 2.5 BERTScore

Zhang et al. (2020) proposed BERTScore, an automatic evaluation metric that computes token-level similarity between candidate and reference texts using contextual embeddings from pretrained transformer models. Unlike n-gram overlap metrics such as BLEU or ROUGE, BERTScore captures semantic equivalence across different surface forms, making it robust to paraphrasing. BMAS adopts BERTScore F1 as its primary pairwise similarity metric for measuring inter-model convergence, complemented by cosine similarity on sentence-level embeddings for computational efficiency.

## 2.6 Constitutional AI

Bai et al. (2022) introduced Constitutional AI (CAI) at Anthropic, a training methodology in which a model critiques and revises its own outputs according to a set of principles (a "constitution") before reinforcement learning from human feedback. CAI demonstrated that self-critique could reduce harmful outputs while maintaining helpfulness, representing a single-model approach to quality improvement through iterative refinement. BMAS can be viewed as extending the critique-and-revise intuition from a single-model loop to a multi-model, multi-provider setting: rather than one model judging itself, multiple independently trained models serve as implicit critics of one another through the divergence signal.

## 2.7 DBSCAN

Ester et al. (1996) proposed DBSCAN (Density-Based Spatial Clustering of Applications with Noise), a clustering algorithm that groups data points based on density connectivity and identifies points in low-density regions as noise or outliers. Unlike k-means, DBSCAN does not require specifying the number of clusters a priori and naturally handles irregularly shaped clusters. BMAS employs DBSCAN on the embedding space of model responses to detect outlier outputs: in factual domains, an outlier response, one that falls outside the epsilon-neighborhood of the consensus cluster, is treated as a candidate hallucination, while in strategic domains, outliers may represent legitimate minority viewpoints.

## 2.8 Positioning

BMAS is, to our knowledge, the first framework that combines four properties absent from any single prior approach. First, it enforces cross-provider blind isolation: unlike self-consistency, which samples from one model, BMAS collects responses from independently trained models across different providers, capturing variation in training data, architecture, and alignment rather than mere decoding stochasticity. Second, it introduces domain-stratified analysis, partitioning prompts into factual, regulatory, and strategic strata to test whether convergence patterns are domain-dependent, a dimension not explored by MoA or LLM-as-Judge evaluations. Third, it treats divergence as an anomaly signal rather than a coordination failure: high inter-model disagreement in well-constrained domains is hypothesized to predict factual error, transforming disagreement from a nuisance into a diagnostic tool. Fourth, it provides a controlled comparison of synthesis strategies (majority-vote, semantic centroid, and LLM-as-Judge) evaluated against pre-registered ground truth, offering empirical guidance on how best to aggregate independent model outputs in practice.
