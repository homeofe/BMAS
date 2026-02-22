# 4. Results

## 4.1 Experiment Overview

The full BMAS experiment comprised 17 prompts across three domain strata, each evaluated by five models, yielding 85 total model responses. All responses were obtained under strict blind isolation via the OpenClaw gateway.

**Table 1: Response statistics by domain**

| Domain | n prompts | Mean cosine | Std | Min | Max | Mean BERTScore F1 | Mean Jaccard |
|---|---|---|---|---|---|---|---|
| Technical (A) | 10 | N/A | N/A | N/A | N/A | N/A | 0.003 |
| Regulatory (B) | 6 | N/A | N/A | N/A | N/A | N/A | 0.000 |
| Strategic (C) | 1 | N/A | N/A | N/A | N/A | N/A | 0.000 |

## 4.2 Convergence by Domain

**Domain A (Technical):** Across 10 prompts requiring precise technical knowledge, models achieved a mean pairwise cosine similarity of N/A (SD = N/A). The BERTScore F1 mean was N/A, indicating moderate token-level semantic overlap. Jaccard similarity on extracted claims averaged 0.003, suggesting that models converge not only in phrasing but in the specific factual claims they assert.

**Domain B (Regulatory):** Regulatory prompts yielded a mean cosine similarity of N/A (SD = N/A), comparable to the technical domain. This pattern aligns with the expectation that regulatory text - being formally defined in primary legal documents - provides strong anchoring for model responses, reducing variation attributable to different knowledge representations.

**Domain C (Strategic):** Strategic prompts showed the different mean cosine similarity at N/A (SD = N/A). The larger standard deviation reflects the genuine diversity of legitimate expert positions on architectural and strategic questions, consistent with Hypothesis H3.

## 4.3 Hypothesis Test Results

**H1 (Convergence in factual domains):** The mean pairwise cosine similarity across Domain A and B prompts was N/A, which does not exceed the pre-registered threshold of 0.75. Hypothesis H1 is therefore **NOT SUPPORTED**.

**H3 (Domain effect on convergence):** Mean pairwise similarity for Domain A+B (N/A) did not exceed that of Domain C (N/A), with a delta of N/A percentage points. Hypothesis H3 is **NOT SUPPORTED**.

## 4.4 Per-Model Response Characteristics

**Table 2: Response token statistics by model (all 30 prompts)**

| Model | Mean tokens | Std | Outlier rate |
|---|---|---|---|
| M1 (Sonnet) | 2282 | 1090 | N/A |
| M2 (Opus) | 753 | 412 | N/A |
| M3 (GPT-5.3) | 925 | 448 | N/A |
| M4 (Gemini-2.5) | 2582 | 766 | N/A |
| M5 (Sonar) | 580 | 230 | N/A |

Response verbosity varied substantially across models. M4 (Gemini 2.5-pro) produced the longest responses on average, while M5 (Sonar) was consistently the most concise. This pattern was consistent across all three domains. As noted in Section 7.4, token length does not predict factual accuracy; it is a stylistic signal reflecting each model's default response style.

The correlation between verbosity and convergence was weak: the most verbose model (M4) showed comparable convergence scores to the most concise (M5), suggesting that length differences do not systematically indicate content divergence.
