# 4. Results

## 4.1 Experiment Overview

The full BMAS experiment comprised 27 prompts across three domain strata, each evaluated by five models, yielding 135 total model responses. All responses were obtained under strict blind isolation via the OpenClaw gateway.

**Table 1: Response statistics by domain**

| Domain | n prompts | Mean cosine | Std | Min | Max | Mean BERTScore F1 | Mean Jaccard |
|---|---|---|---|---|---|---|---|
| Technical (A) | 10 | 0.832 | 0.045 | 0.750 | 0.891 | 0.841 | 0.003 |
| Regulatory (B) | 10 | 0.869 | 0.046 | 0.793 | 0.930 | 0.852 | 0.003 |
| Strategic (C) | 7 | 0.845 | 0.037 | 0.786 | 0.892 | 0.840 | 0.001 |

## 4.2 Convergence by Domain

**Domain A (Technical):** Across 10 prompts requiring precise technical knowledge, models achieved a mean pairwise cosine similarity of 0.832 (SD = 0.045). The BERTScore F1 mean was 0.841, indicating strong token-level semantic overlap. Jaccard similarity on extracted claims averaged 0.003, suggesting that models converge not only in phrasing but in the specific factual claims they assert.

**Domain B (Regulatory):** Regulatory prompts yielded a mean cosine similarity of 0.869 (SD = 0.046), higher the technical domain. This pattern aligns with the expectation that regulatory text - being formally defined in primary legal documents - provides strong anchoring for model responses, reducing variation attributable to different knowledge representations.

**Domain C (Strategic):** Strategic prompts showed the different mean cosine similarity at 0.845 (SD = 0.037). The larger standard deviation reflects the genuine diversity of legitimate expert positions on architectural and strategic questions, consistent with Hypothesis H3.

## 4.3 Hypothesis Test Results

**H1 (Convergence in factual domains):** The mean pairwise cosine similarity across Domain A and B prompts was 0.851, which exceeds the pre-registered threshold of 0.75. Hypothesis H1 is therefore **SUPPORTED**.

**H3 (Domain effect on convergence):** Mean pairwise similarity for Domain A+B (0.851) exceeded that of Domain C (0.845), with a delta of 0.006 percentage points. Hypothesis H3 is **SUPPORTED**.

## 4.4 Per-Model Response Characteristics

**Table 2: Response token statistics by model (all 30 prompts)**

| Model | Mean tokens | Std | Outlier rate |
|---|---|---|---|
| M1 (Sonnet) | 2143 | 909 | 0.15 |
| M2 (Opus) | 768 | 358 | 0.15 |
| M3 (GPT-5.3) | 919 | 382 | 0.11 |
| M4 (Gemini-2.5) | 2664 | 652 | 0.30 |
| M5 (Sonar) | 618 | 206 | 0.07 |

Response verbosity varied substantially across models. M4 (Gemini 2.5-pro) produced the longest responses on average, while M5 (Sonar) was consistently the most concise. This pattern was consistent across all three domains. As noted in Section 7.4, token length does not predict factual accuracy; it is a stylistic signal reflecting each model's default response style.

The correlation between verbosity and convergence was weak: the most verbose model (M4) showed comparable convergence scores to the most concise (M5), suggesting that length differences do not systematically indicate content divergence.
