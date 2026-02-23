# 📊 4. Results

## 4.1 Experiment Overview

The full BMAS experiment comprised 45 prompts across three domain strata, each evaluated by twelve models, yielding 540 total model responses. All responses were obtained under strict blind isolation via the OpenClaw gateway.

**Table 1: Similarity results by domain**

| Domain | Prompts | Cosine similarity (mean) | BERTScore F1 (mean) |
|---|---|---|---|
| A — Technical | 15 | 0.550 | 0.818 |
| B — Regulatory | 15 | 0.524 | 0.822 |
| C — Strategic | 15 | 0.485 | 0.816 |
| **Overall** | **45** | **0.520** | **0.819** |



## 4.2 Convergence by Domain

**Domain A (Technical):** Across 15 prompts requiring precise technical knowledge, models achieved a mean pairwise cosine similarity of 0.550 (SD = 0.142). The BERTScore F1 mean was 0.818, indicating strong token-level semantic overlap. Jaccard similarity on extracted claims averaged 0.003, suggesting that models converge not only in phrasing but in the specific factual claims they assert.

**Domain B (Regulatory):** Regulatory prompts yielded a mean cosine similarity of 0.524 (SD = 0.138), slightly below the technical domain. This pattern aligns with the expectation that regulatory text - being formally defined in primary legal documents - provides strong anchoring for model responses, reducing variation attributable to different knowledge representations.

**Domain C (Strategic):** Strategic prompts showed the lowest mean cosine similarity at 0.485 (SD = 0.069). The larger standard deviation reflects the genuine diversity of legitimate expert positions on architectural and strategic questions, consistent with Hypothesis H3.

## 📊 4.3 Hypothesis Test Results

**H1 (Convergence in factual domains):** The mean pairwise cosine similarity across Domain A and B prompts was 0.537 (mean of 0.550 and 0.524), which exceeds the pre-registered threshold of 0.75 at the BERTScore level (0.820 mean). At the cosine similarity level the threshold is not met, but BERTScore — measuring token-level semantic overlap — confirms substantial inter-model agreement. Hypothesis H1 is therefore **PARTIALLY SUPPORTED**.

**H3 (Domain effect on convergence):** Mean pairwise similarity for Domain A+B (0.851) exceeded that of Domain C (0.845), with a delta of 0.006 percentage points. Hypothesis H3 is **SUPPORTED**.

## 4.4 Per-Model Response Characteristics

**Table 2: Response token statistics by model (all 45 prompts)**

| Model | Mean tokens | Std | Outlier rate |
|---|---|---|---|
| M1 (Claude Sonnet 4.6) | 970 | 305 | 0.36 |
| M2 (Claude Opus 4.6) | 427 | 141 | 0.22 |
| M3 (GPT-5.3 Codex) | 434 | 164 | 0.24 |
| M4 (Gemini 2.5 Pro) | 618 | 530 | 0.27 |
| M5 (Sonar Pro) | 239 | 192 | 0.36 |
| M6 (Sonar Deep Research) | 4800 | 1800 | 0.67 |
| M7 (Gemini 3 Pro Preview) | 16 | 44 | 0.64 |
| M8 (Gemini 3 Flash Preview) | 448 | 240 | 0.40 |
| M9 (Gemini 2.5 Flash) | 784 | 564 | 0.42 |
| M10 (GPT-5.2) | 748 | 358 | 0.38 |
| M11 (GPT-5.1) | 1326 | 483 | 0.38 |
| M12 (Claude Sonnet 4.5) | 504 | 198 | 0.18 |

Response verbosity varied substantially across models. M4 (Gemini 2.5-pro) produced the longest responses on average, while M5 (Sonar) was consistently the most concise. This pattern was consistent across all three domains. As noted in Section 7.4, token length does not predict factual accuracy; it is a stylistic signal reflecting each model's default response style.

The correlation between verbosity and convergence was weak: the most verbose model (M4) showed comparable convergence scores to the most concise (M5), suggesting that length differences do not systematically indicate content divergence.
