# 3. Methodology

## 3.1 BMAS Protocol Overview

Blind Multi-Agent Synthesis (BMAS) is a four-phase protocol for eliciting, comparing, and synthesizing responses from multiple LLMs on identical prompts. The four phases are:

1. **Blind Elicitation** - Each model receives the same prompt with no knowledge of the study, other models, or other responses.
2. **Metric Computation** - Pairwise semantic similarity, factual accuracy, and outlier detection are computed across all model responses.
3. **Synthesis** - Three synthesis strategies aggregate the individual responses into a single output.
4. **Evaluation** - Synthesis outputs are scored against pre-registered ground truth (Domains A and B) or expert evaluation (Domain C).

The protocol enforces a strict **no-contamination rule**: no model response is made available to any other model at any phase prior to synthesis. This mirrors the isolation requirement of the Delphi method and distinguishes BMAS from cooperative multi-agent approaches such as MoA (Wang et al., 2024).

## 3.2 Models

We evaluate twelve state-of-the-art LLMs from four distinct providers (Anthropic, OpenAI, Google, Perplexity):

| ID | Model | Provider | Context window |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M tokens |
| M2 | claude-opus-4-6 | Anthropic | 1M tokens |
| M3 | gpt-5.3-codex | OpenAI | 272k tokens |
| M4 | gemini-2.5-pro | Google | 1M tokens |
| M5 | sonar-pro | Perplexity | 127k tokens |

Multi-provider diversity is deliberate. Models from the same provider share architectural lineage and training data pipelines, which may reduce divergence even under blind conditions. Including models from four separate providers maximizes the independence of responses.

**Isolation implementation:** Each model runs in a separate isolated session with no shared context. The system prompt is identical across all models:

> *"You are a knowledgeable expert assistant. Answer the following question as accurately and completely as possible. Be precise, factual, and structured. If you are uncertain about any specific detail, state that explicitly."*

Temperature is not overridden. We deliberately preserve each model's default sampling behavior to capture natural response variance, not to normalize it.

## 3.3 Prompt Design

### 3.3.1 Domain Structure

We constructed 45 prompts across three domain strata:

**Domain A - High-Precision Technical (A01-A10):** Questions with objectively correct answers verifiable against primary authoritative sources (NIST FIPS standards, NVD, IETF RFCs, OpenID Foundation specifications). Examples: CVSS scoring rationale, PQC algorithm key sizes, TLS 1.3 cipher suite enumeration.

**Domain B - Regulatory/Compliance (B01-B10):** Questions grounded in legal and regulatory text with authoritative sources (GDPR, eIDAS 2.0, NIS2, ISO 27001, BSI C5). Some interpretive judgment is required at the edges, but the core answers are defined in formal text. Examples: GDPR Article 17(3) erasure exceptions, NIS2 sector classifications, TISAX assessment level differences.

**Domain C - Strategic/Ambiguous (C01-C10):** Questions with no single correct answer, requiring expert judgment and architectural reasoning. Multiple defensible positions exist. Examples: zero-trust architecture decisions, PQC migration prioritization, compliance investment trade-offs.

### 3.3.2 Prompt Requirements

All prompts were designed to satisfy four criteria:

1. **Self-contained** - answerable without external context or document retrieval
2. **Structured response** - each prompt specifies a required output format (list, comparison, decision with rationale)
3. **Bounded length** - expected response of 300-600 tokens for Domains A-B; 400-800 for Domain C
4. **Testable** - for Domains A and B, a verifiable answer exists; for Domain C, expert evaluation is tractable

### 3.3.3 Pre-Registration

Following open science best practice, ground truth for Domains A and B was documented and locked prior to any model runs. This prevents unconscious confirmation bias in scoring. Ground truth documents are published alongside the dataset.

Domain C has no pre-registered ground truth. Expert evaluation (the lead author as domain expert) assesses synthesis quality against a rubric of completeness, reasoning quality, and practical actionability.

## 3.4 Metrics

### 3.4.1 Semantic Similarity (Primary)

We compute pairwise cosine similarity between response embeddings using the `all-mpnet-base-v2` sentence-transformer model (Reimers and Gurevych, 2019). For N models, this produces an N x N similarity matrix per prompt. We report:

- **Mean pairwise similarity (MPS):** average of all N(N-1)/2 pairwise scores
- **Min pairwise similarity:** most divergent pair
- **Similarity standard deviation:** variance within the prompt's response cluster

### 3.4.2 BERTScore

We compute pairwise BERTScore F1 (Zhang et al., 2020) as a secondary token-level semantic similarity measure. BERTScore captures lexical proximity beyond sentence-level embeddings and is sensitive to factual claim overlap.

### 3.4.3 Jaccard on Key Claims

We extract discrete factual claims from each response using sentence segmentation and compute pairwise Jaccard similarity on normalized claim sets. This metric captures structural agreement - whether models identify the same key points - independently of phrasing.

### 3.4.4 Outlier Detection

We apply DBSCAN (Ester et al., 1996) to the embedding space with eps=0.15 (equivalent to cosine similarity < 0.85) and min_samples=2. Models whose embeddings fall outside all neighborhood clusters receive an outlier label (-1). We treat outlier status as a signal for potential hallucination in Domains A and B, and as a minority-view indicator in Domain C.

### 3.4.5 Factual Accuracy (Domains A and B only)

For each Domain A and B response, we score factual accuracy against the pre-registered ground truth checklist. Each checklist item is binary (present and correct, or absent/incorrect). The factual accuracy score is the fraction of checklist items satisfied.

## 3.5 Synthesis Strategies

We evaluate three synthesis strategies:

**S1 - Majority-Vote (claim-level):** Factual claims are extracted from all responses. A claim is accepted into the synthesis if it appears in responses from at least 58% of models (seven of twelve). Minority claims (below threshold) are appended with a [MINORITY] marker.

**S2 - Semantic Centroid:** The response whose embedding is closest to the mean of all response embeddings is selected as the synthesis base. This captures the "most representative" single response. No new content is added.

**S3 - LLM-as-Judge:** All twelve anonymized responses are presented to a thirteenth model instance (M2, claude-opus-4-6) with the instruction to produce a single authoritative synthesis, marking minority claims ([MINORITY]) and contradictions ([DISPUTED]). The judge model receives no information identifying which model produced which response.

Synthesis quality is evaluated by measuring the resulting text's factual accuracy against the pre-registered ground truth (Domains A and B) and by expert rubric scoring (Domain C).

## 3.6 Hypotheses

We test three pre-registered hypotheses:

**H1 (Convergence in factual domains):** Mean pairwise semantic similarity for Domain A and B prompts will exceed 0.75 (BERTScore F1).

**H2 (Divergence signals error):** Among Domain A and B responses, outlier models (DBSCAN label -1) will have significantly lower factual accuracy scores than non-outlier models (one-sided t-test, alpha=0.05).

**H3 (Domain effect on convergence):** Mean pairwise similarity for Domain C will be significantly lower than for Domains A and B (one-way ANOVA, post-hoc Tukey HSD, alpha=0.05).

## 3.7 Experimental Setup

All model runs were executed via the OpenClaw gateway, which routes to each provider's API independently. Each prompt runs in a separate isolated session with no shared state. Run outputs are stored as structured JSON with prompt ID, model ID, response text, token counts, and latency. The full dataset of 540 runs (45 prompts x 5 models) is released alongside this paper.
