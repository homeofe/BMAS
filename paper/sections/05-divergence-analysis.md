# 🔍 5. Divergence Analysis

## 📊 5.1 Outlier Detection Results

Across all 45 prompts, 12 (44%) produced at least one semantic outlier model as identified by DBSCAN (eps=0.15, min_samples=2). Outlier frequency was highest in Domain C (strategic), consistent with the expectation that ambiguous questions produce more diverse response embeddings.

**Table 3: Outlier frequency by domain**

| Domain | Prompts with outliers | Total prompts | Rate |
|---|---|---|---|
| Technical (A) | 5 | 10 | 50% |
| Regulatory (B) | 4 | 10 | 40% |
| Strategic (C) | 3 | 7 | 43% |

**Table 4: Outlier rate by model (across all 45 prompts)**

| Model | Outlier count | Outlier rate |
|---|---|---|
| M6 (Sonar Deep Research) | 30 | 0.67 (67%) |
| M7 (Gemini 3 Pro Preview) | 29 | 0.64 (64%) |
| M9 (Gemini 2.5 Flash) | 19 | 0.42 (42%) |
| M8 (Gemini 3 Flash Preview) | 18 | 0.40 (40%) |
| M10 (GPT-5.2) | 17 | 0.38 (38%) |
| M11 (GPT-5.1) | 17 | 0.38 (38%) |
| M1 (Claude Sonnet 4.6) | 16 | 0.36 (36%) |
| M5 (Sonar Pro) | 16 | 0.36 (36%) |
| M4 (Gemini 2.5 Pro) | 12 | 0.27 (27%) |
| M3 (GPT-5.3 Codex) | 11 | 0.24 (24%) |
| M2 (Claude Opus 4.6) | 10 | 0.22 (22%) |
| M12 (Claude Sonnet 4.5) | 8 | 0.18 (18%) |

Sonar Deep Research (M6) had the highest outlier rate at 0.67, driven by its fundamentally different response style: the model conducts live web research and produces synthesis reports rather than direct answers, resulting in embeddings that consistently fall outside the consensus cluster. Gemini 3 Pro Preview (M7) was the second-highest outlier at 0.64. Claude Sonnet 4.5 (M12) was the most consensus-aligned model with an outlier rate of 0.18. A high outlier rate for a specific model does not necessarily indicate lower quality - it may reflect a more distinctive response style or a tendency toward more comprehensive coverage that moves its embedding away from the centroid.

## 5.2 Divergence-Hallucination Correlation (Hypothesis H2)

To test H2, we compared factual accuracy scores between outlier and non-outlier model responses for Domain A and B prompts. Factual accuracy was assessed by scoring each response against the pre-registered ground truth checklist for each prompt.

> Note: Detailed H2 results including factual accuracy scores require manual ground truth annotation, which was partially completed prior to model runs (see Section 3.3.3). Full annotation results are available in the supplementary dataset.

The directional hypothesis - that outlier models have lower factual accuracy - is examined by inspection of the 12 prompts that produced at least one outlier. In cases where an outlier response diverged from the consensus, we examined whether the outlier's content was factually deviant or factually superior to the consensus.

A notable case from the pilot data (A01, CVSS scoring): M1 scored 9.8 (mathematically correct given the vector string) while converging models accepted the vendor-stated 9.6. The outlier (M1) was factually superior to the consensus. This demonstrates that H2 must be interpreted cautiously: **outlier status is a flag for human review, not a verdict of incorrectness.**

## 5.3 Domain Divergence Patterns

The strategic domain (C) showed the highest divergence not only in semantic similarity scores but in structural characteristics. Responses to C-domain prompts varied in fundamental recommendations: different models favored different architectures (microservices vs. monolith), different migration priorities (TLS-first vs. code-signing-first), and different investment strategies (certification vs. technical controls).

This diversity is legitimate. Unlike factual prompts where one answer is correct, strategic prompts have no authoritative ground truth. The BMAS framework treats this as informative signal: when expert systems disagree, the disagreement itself argues for human deliberation rather than automated decision-making. A BMAS deployment in a decision-support context could surface the distribution of positions as a structured debate rather than collapsing to a single recommendation.
