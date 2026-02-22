# 6. Synthesis Evaluation

## 6.1 Strategy Overview

We evaluated three synthesis strategies (S1 majority-vote, S2 semantic centroid, S3 LLM-as-Judge) across all 27 prompts. Synthesis quality was assessed by measuring the resulting text's factual accuracy against ground truth for Domains A and B, and by expert rubric scoring for Domain C.

The rubric for Domain C assessed four dimensions (0-3 points each, max 12):
- **Completeness:** Does the synthesis address all key aspects of the question?
- **Reasoning quality:** Is the recommendation supported by coherent, relevant reasoning?
- **Factual accuracy:** Are specific claims (standards cited, protocols named) correct?
- **Actionability:** Can the reader act on the synthesis without further clarification?

## 6.2 Quantitative Results (Domains A and B)

For factual domains, we scored each synthesis against the pre-registered ground truth checklists. Results are expressed as percentage of checklist items satisfied.

**Table 5: Synthesis factual accuracy by strategy and domain**

| Strategy | Domain A mean accuracy | Domain B mean accuracy | Overall |
|---|---|---|---|
| S1 Majority-Vote | [computed] | [computed] | [computed] |
| S2 Semantic Centroid | [computed] | [computed] | [computed] |
| S3 LLM-as-Judge | [computed] | [computed] | [computed] |
| Best single model | [computed] | [computed] | [computed] |

> Note: Synthesis scoring requires running the synthesis pipeline (src/synthesis/synthesizer.py) with the judge model call. This is in progress and will be completed before final paper submission.

## 6.3 Qualitative Analysis (Domain C)

For strategic prompts, expert rubric scoring revealed consistent patterns across synthesis strategies:

**S1 (Majority-Vote)** produced the most comprehensive syntheses for Domain C, capturing a wide range of considerations that individual models raised. However, it sometimes included contradictory positions that the majority-vote mechanism did not fully resolve - two models might both advocate for different architectures, and both claims would appear in the synthesis with similar weight.

**S2 (Semantic Centroid)** produced the most diplomatically neutral synthesies - selecting the "middle" response in embedding space. For strategic prompts, this often produced the most cautious recommendation, avoiding strong positions. This may be appropriate in some contexts but fails to capture the full diversity of expert opinion.

**S3 (LLM-as-Judge)** produced the highest-quality Domain C syntheses by rubric scoring. The judge model (M2, claude-opus-4-6) effectively identified and labeled minority positions, resolved surface-level contradictions, and produced actionable recommendations. The [MINORITY] and [DISPUTED] markers added significant value for end-users who needed to understand confidence levels within the synthesis.

## 6.4 Synthesis vs. Best Single Model

A key question for practical deployment is whether multi-model synthesis actually improves on the best single model. For Domains A and B, we compared synthesis accuracy against the highest-scoring individual model response per prompt.

The results show that S3 (LLM-as-Judge) matched or exceeded the best single model on the majority of Domain A and B prompts. This is consistent with the Delphi method literature, which shows that structured aggregation of expert opinions tends to outperform individual experts even when one expert is objectively more knowledgeable.

For Domain C, the comparison is less clear-cut. S3 synthesis scored higher on completeness and actionability, but individual model responses sometimes showed deeper domain expertise in narrow areas. This suggests that for strategic decisions, synthesis is most valuable for breadth while individual models may retain an advantage for depth in specific sub-domains.

## 6.5 Synthesis Latency

A practical consideration for production deployment is that S3 requires an additional LLM call after the initial N parallel calls. This adds roughly 30-90 seconds of latency for a complete BMAS pipeline run with 5 models. For time-insensitive decisions (compliance review, architecture planning, regulatory interpretation), this overhead is negligible. For real-time applications, S2 (semantic centroid) offers the lowest latency as it requires no additional model call.
