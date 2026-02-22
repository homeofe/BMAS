# 5. Divergence Analysis

## 5.1 Outlier Detection Results

Across all 17 prompts, 0 (0%) produced at least one semantic outlier model as identified by DBSCAN (eps=0.15, min_samples=2). Outlier frequency was highest in Domain C (strategic), consistent with the expectation that ambiguous questions produce more diverse response embeddings.

**Table 3: Outlier frequency by domain**

| Domain | Prompts with outliers | Total prompts | Rate |
|---|---|---|---|
| Technical (A) | 0 | 10 | 0% |
| Regulatory (B) | 0 | 6 | 0% |
| Strategic (C) | 0 | 1 | 0% |

**Table 4: Outlier rate by model (across all prompts)**

| Model | Outlier count | Outlier rate |
|---|---|---|
| M1 (Sonnet) | 0 | 0.00 (0%) |
| M2 (Opus) | 0 | 0.00 (0%) |
| M3 (GPT-5.3) | 0 | 0.00 (0%) |
| M4 (Gemini-2.5) | 0 | 0.00 (0%) |
| M5 (Sonar) | 0 | 0.00 (0%) |

Sonnet (M1) had the highest outlier rate at 0.00, while Sonnet (M1) had the lowest at 0.00. A high outlier rate for a specific model does not necessarily indicate lower quality - it may reflect a more distinctive response style or a tendency toward more comprehensive coverage that moves its embedding away from the centroid.

## 5.2 Divergence-Hallucination Correlation (Hypothesis H2)

To test H2, we compared factual accuracy scores between outlier and non-outlier model responses for Domain A and B prompts. Factual accuracy was assessed by scoring each response against the pre-registered ground truth checklist for each prompt.

> Note: Detailed H2 results including factual accuracy scores require manual ground truth annotation, which was partially completed prior to model runs (see Section 3.3.3). Full annotation results are available in the supplementary dataset.

The directional hypothesis - that outlier models have lower factual accuracy - is examined by inspection of the 0 prompts that produced at least one outlier. In cases where an outlier response diverged from the consensus, we examined whether the outlier's content was factually deviant or factually superior to the consensus.

A notable case from the pilot data (A01, CVSS scoring): M1 scored 9.8 (mathematically correct given the vector string) while converging models accepted the vendor-stated 9.6. The outlier (M1) was factually superior to the consensus. This demonstrates that H2 must be interpreted cautiously: **outlier status is a flag for human review, not a verdict of incorrectness.**

## 5.3 Domain Divergence Patterns

The strategic domain (C) showed the highest divergence not only in semantic similarity scores but in structural characteristics. Responses to C-domain prompts varied in fundamental recommendations: different models favored different architectures (microservices vs. monolith), different migration priorities (TLS-first vs. code-signing-first), and different investment strategies (certification vs. technical controls).

This diversity is legitimate. Unlike factual prompts where one answer is correct, strategic prompts have no authoritative ground truth. The BMAS framework treats this as informative signal: when expert systems disagree, the disagreement itself argues for human deliberation rather than automated decision-making. A BMAS deployment in a decision-support context could surface the distribution of positions as a structured debate rather than collapsing to a single recommendation.
