# BMAS Experiment Design v1.0

## Overview

**Research Question:**
How much do state-of-the-art LLMs deviate from each other when answering identical prompts in isolation, and does question domain predict convergence?

**Hypothesis H1 (Convergence):**
In factual, well-constrained domains, semantic similarity between model responses will exceed 0.85 (BERTScore F1).

**Hypothesis H2 (Divergence Signals):**
Factual errors (hallucinations) will correlate with inter-model divergence: a response that deviates significantly from the consensus cluster is more likely to be factually incorrect.

**Hypothesis H3 (Domain Effect):**
Strategic/ambiguous domain prompts will show significantly lower convergence than technical/regulatory prompts (expected delta: >0.15 BERTScore F1).

---

## Models

| ID | Model | Provider | Context |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M tokens |
| M2 | claude-opus-4-6 | Anthropic | 1M tokens |
| M3 | gpt-5.3-codex | OpenAI (openai-codex OAuth) | 272k tokens |
| M4 | gemini-2.5-pro | Google (gemini-cli) | 1M tokens |
| M5 | perplexity/sonar-pro | Perplexity | 127k tokens |

**Isolation Protocol:**
- Each model receives only the prompt - no system context about other models
- No few-shot examples that could bias output format
- Temperature: default (model-specific, not overridden) - captures natural model behavior
- No retry on first response - first output is the data point

---

## Prompt Design

### Total: 45 prompts (15 per domain)

### Domain A: High-Precision Technical (A01-A10)
Topics: CVSS scoring, PQC algorithms, TLS cipher suites, hash functions, cryptographic attacks, CVE analysis

Characteristics:
- Objectively correct answers exist
- Ground truth verifiable against NIST, IETF RFCs, NVD
- No opinion required

Example: "What is the CVSS 3.1 base score for CVE-2024-21762 (Fortinet FortiOS)? Explain the scoring rationale."

### Domain B: Regulatory / Compliance (B01-B10)
Topics: GDPR articles, eIDAS 2.0 requirements, TISAX AL levels, BSI C5, ISO 27001 controls

Characteristics:
- Authoritative sources exist (official legal text)
- Some interpretation required (ambiguity in application, not in text)
- Models may differ on edge cases

Example: "Under GDPR Article 17, under which conditions can a data subject's right to erasure be refused? List all valid legal bases."

### Domain C: Strategic / Ambiguous (C01-C10)
Topics: Architecture trade-offs, security design decisions, technology selection rationale

Characteristics:
- No single correct answer
- Expert opinions legitimately differ
- Tests whether models hedge, commit, or hallucinate confidence

Example: "For a zero-trust architecture handling cross-border EU government identity verification, should the orchestration layer be implemented as an event-driven microservice mesh or a stateless API gateway chain? Justify your recommendation."

---

## Prompt Requirements

Each prompt must:
1. Be self-contained (no context window dependency)
2. Have a defined expected answer structure (list, explanation, decision)
3. Be answerable within ~500 tokens
4. For Domain A+B: have a verifiable ground truth documented in `prompts/<domain>/ground-truth/`

---

## Metrics

### 1. Semantic Similarity (Primary)
- **Tool:** `sentence-transformers` (model: `all-MiniLM-L6-v2` for speed, `all-mpnet-base-v2` for accuracy)
- **Method:** Pairwise cosine similarity of response embeddings
- **Output:** N x N similarity matrix per prompt; average pairwise score

### 2. BERTScore (Secondary)
- **Tool:** `bert-score` Python package
- **Method:** Token-level F1 between each pair of responses
- **Output:** Precision, Recall, F1 per pair

### 3. Factual Accuracy (Domain A+B only)
- **Method:** Manual annotation against ground truth + automated key-fact extraction
- **Scoring:** 0-1 per response (fraction of ground truth facts present and correct)
- **Note:** Ground truth must be documented BEFORE running models (pre-registration)

### 4. Jaccard on Key Points
- **Method:** Extract bullet points / numbered claims from each response; compute Jaccard similarity on normalized claim sets
- **Use:** Captures structural agreement independent of phrasing

### 5. Outlier Detection
- **Method:** DBSCAN clustering on embedding space; models outside epsilon-neighborhood = outlier
- **Hypothesis:** Outliers in Domain A/B = likely hallucination; outliers in Domain C = legitimate minority view

---

## Synthesis Layer

Three synthesis strategies to compare:

### S1: Majority-Vote (Claim-Level)
Extract factual claims from each response. A claim is "accepted" if present in >=7/12 models (>=58%).

### S2: Semantic Centroid
Compute centroid of all response embeddings. Select the response closest to centroid as "representative." Use it as base; append claims unique to 2+ other models.

### S3: LLM-as-Judge
Feed all 5 raw responses to a 6th model (claude-opus-4-6) with the instruction: "You are a synthesis judge. Given these 5 independent expert responses to the same question, produce a single authoritative synthesis. Mark any claim that only one model made as [MINORITY]. Mark any claim where models contradict each other as [DISPUTED]."

**Evaluation of synthesis strategies:**
- Compare synthesized output against ground truth (Domain A+B)
- Human evaluation for Domain C (Emre as domain expert)

---

## Execution Protocol

```
Phase 1: Pre-Registration
  - Finalize prompt set (this doc + prompts/ folder)
  - Document ground truth for Domain A+B
  - Lock design (no changes after first model run)

Phase 2: Blind Runs
  - Run each prompt against each model independently
  - Store raw output in experiments/raw-outputs/<prompt-id>/<model-id>.json
  - No human review until all 12 models complete each prompt

Phase 3: Metric Computation
  - Run metrics pipeline (src/metrics/)
  - Generate similarity matrices
  - Detect outliers
  - Annotate factual accuracy (Domain A+B)

Phase 4: Synthesis
  - Apply S1, S2, S3 to each prompt
  - Compare synthesis quality against ground truth

Phase 5: Analysis
  - Statistical tests (ANOVA on domain x convergence)
  - Correlation: divergence x hallucination rate
  - Figures: heatmaps, box plots, scatter plots
  - Narrative: what did we find?

Phase 6: Paper
  - Write up results in paper/sections/
  - Generate figures in paper/figures/
  - Internal review
  - arXiv preprint
```

---

## Output Format (raw-outputs)

```json
{
  "run_id": "A01-M1-20260221",
  "prompt_id": "A01",
  "model_id": "M1",
  "model": "claude-sonnet-4-6",
  "domain": "technical",
  "prompt": "...",
  "response": "...",
  "response_tokens": 412,
  "latency_ms": 3200,
  "timestamp": "2026-02-21T22:00:00Z"
}
```

---

## Timeline (estimate)

| Phase | Duration |
|---|---|
| Prompt finalization | 1 week |
| Blind runs | 2-3 days |
| Metric computation | 3-5 days |
| Synthesis | 3-5 days |
| Analysis + figures | 1 week |
| Paper draft | 2 weeks |
| Review + polish | 1 week |
| arXiv submission | Day 1 after polish |

**Target: arXiv preprint within 6-8 weeks from today.**

---

## 📚 Related Work (to cite)

- Delphi method (Dalkey & Helmer, 1963) - original blind expert consensus
- Constitutional AI (Anthropic, 2022) - model self-critique
- LLM-as-Judge (Zheng et al., 2023) - model evaluation by model
- Self-Consistency (Wang et al., 2022) - multiple reasoning chains, majority vote
- Mixture of Agents (Wang et al., 2024) - collaborative LLM aggregation
- BERTScore (Zhang et al., 2020) - learned metric for text similarity

**Key differentiation from Self-Consistency and MoA:**
- Self-Consistency: same model, different reasoning chains
- MoA: models see each other's outputs (not blind)
- BMAS: different models, strict blind isolation, domain-stratified analysis
