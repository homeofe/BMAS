# 7. Discussion

## 7.1 Interpreting Convergence and Divergence

The central claim of BMAS is that inter-model convergence is informative - not just a statistical property of the experiment, but a practical signal for downstream applications. Our results [see Section 4] support this claim for factual domains while revealing important nuances.

High convergence in Domains A and B validates the intuition that well-calibrated models trained on the same authoritative sources tend toward the same correct answers when the questions are unambiguous. This is not a trivial finding: it suggests that for compliance verification, regulatory interpretation, and technical standard citation, a consensus of multiple independent models can substitute for - or at minimum augment - single-expert review in time-critical contexts.

Low convergence in Domain C (strategic and ambiguous prompts) is equally informative. Rather than representing model failure, it reflects the genuine epistemic difficulty of the questions. When twelve independent expert systems disagree on optimal architecture decisions or security investment trade-offs, the disagreement itself is meaningful - it signals that the question has no dominant correct answer and deserves human deliberation. BMAS thus serves as a **complexity oracle** in addition to a quality signal.

## 7.2 The Divergence-Hallucination Connection

Our outlier analysis [see Section 5] provides preliminary evidence for the divergence-as-signal hypothesis. Models that score as outliers in embedding space tend to have lower factual accuracy scores, suggesting that semantic isolation from the consensus cluster correlates with factual deviation from ground truth.

This finding has practical implications for AI deployment in regulated industries. A production system implementing BMAS-style monitoring could flag responses that deviate significantly from the consensus cluster for human review, reducing reliance on manual verification of every model output while maintaining accuracy guarantees.

We caution, however, that correlation is not causation. An outlier response may be correct while the consensus is wrong - particularly for recently published information or domain-specific knowledge not well-represented in the training data of most models. The M1 response to A01 (CVE-2024-21762 CVSS scoring) demonstrated this: the outlier score was mathematically correct while the consensus converged on the vendor-stated score, which differs due to rounding convention. Any production implementation of divergence-based filtering must retain human override capability.

## 7.3 Synthesis Strategy Comparison

The three synthesis strategies evaluated - majority-vote (S1), semantic centroid (S2), and LLM-as-Judge (S3) - each exhibit distinct trade-offs [see Section 6].

S1 (majority-vote) produces comprehensive coverage but may be verbose and occasionally includes low-confidence minority claims despite the 60% threshold. It is most appropriate when completeness is prioritized over conciseness.

S2 (semantic centroid) reliably produces the most "average" response - informative as a benchmark but potentially masking important minority insights. It works best when a representative single response is needed and the question is well-constrained.

S3 (LLM-as-Judge) produces the highest factual accuracy on Domains A and B [see Section 6] but introduces a new dependency - the judge model's own biases. When the judge model is itself an outlier on a given prompt, its synthesis may systematically under-represent the majority view. Using a held-out model (one that did not participate in the blind run) as judge mitigates this risk.

## 7.4 Limitations

**Sample size.** With 45 prompts across three domains, this study establishes initial evidence for the BMAS methodology but does not permit broad statistical generalization. A follow-up study with 100+ prompts per domain would substantially strengthen the claims.

**Model selection.** The twelve models used represent a convenience sample of accessible frontier models at the time of study. Model composition affects the consensus distribution: a study using twelve Anthropic models would show different variance characteristics than a cross-provider study. Future work should systematically vary model composition.

**Ground truth quality.** Domain A and B ground truth was compiled via web research against primary sources. Three items were flagged as requiring manual verification (A01 CVSS discrepancy, A10 BSI source access, B09 EDPB guideline reference). These items are noted in the dataset but may introduce minor scoring inaccuracies.

**Temporal validity.** LLM knowledge cutoffs and model versions change. Results reported here reflect specific model versions at a specific point in time. Replication studies should document model version and knowledge cutoff precisely.

**Temperature and sampling.** We did not control temperature across models. Default sampling behavior was preserved to capture natural model variance. This means some of the observed variance may be attributable to decoding randomness rather than true knowledge differences. Controlled-temperature replication would isolate this variable.

**Token length is not information density.** Our observation that M4 (Gemini 2.5-pro) consistently produces more tokens does not imply greater accuracy or completeness. Token count is a stylistic signal, not a quality signal. All factual accuracy claims are based on ground truth scoring, not response length.

## 7.5 Implications for AI Deployment

BMAS has three direct deployment implications:

**1. Consensus as a quality gate.** In high-stakes AI systems (legal, medical, government), a BMAS-style layer can run multiple models on the same query and withhold the response until consensus meets a defined threshold. Disagreement triggers human review rather than automated action.

**2. Domain routing.** BMAS results suggest that for factual queries with authoritative sources, a single high-performing model may be sufficient. The multi-model overhead is most justified for strategic, ambiguous, or novel queries where the domain lacks a single authoritative ground truth.

**3. Diversity requirements.** BMAS performance depends on model diversity. Two highly similar models from the same provider add less information than two models from different architectural families. Procurement decisions for AI systems in regulated industries should consider provider diversity alongside individual model capability.

## 7.6 Future Work

Several extensions of the BMAS framework merit investigation:

- **Temporal drift study:** run the same prompts against the same models at 6-month intervals to measure whether convergence changes as models are updated
- **Domain expansion:** extend to medical diagnosis, financial analysis, and legal reasoning
- **Calibration analysis:** measure whether model confidence (when expressed) correlates with consensus agreement
- **Adaptive synthesis:** develop a synthesis strategy that selects S1, S2, or S3 dynamically based on measured convergence
- **Human evaluation:** compare BMAS synthesis quality against expert human responses using blind evaluation
