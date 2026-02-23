# 📝 1. Introduction

Large language models have become capable enough that they are being deployed in domains where accuracy is not optional: legal analysis, medical diagnostics, regulatory compliance, and government identity systems. In these domains, a single model's confident but wrong answer is not a minor inconvenience -- it is a failure with real consequences.

The dominant approach to improving LLM reliability is either better training (RLHF, Constitutional AI) or better prompting (chain-of-thought, retrieval augmentation). Both operate within a single-model paradigm: one model, one output, one answer to trust or not.

This paper takes a different approach. Instead of asking "how do we make one model more reliable," we ask: **what can we learn from disagreement between multiple models that are not allowed to influence each other?**

## 1.1 The Core Insight

When five independent experts answer the same question without consulting each other, and four of them give the same answer while one gives a different one, we do not conclude that the four are wrong. We examine the dissenting answer more carefully -- but we trust the consensus as a prior.

This is the Delphi method, applied since 1963 to expert forecasting. Its strength is structural: **isolation prevents groupthink; consensus emerges from independent reasoning, not social pressure.**

BMAS applies this logic to LLMs. Each model is an expert with a particular training distribution, knowledge cutoff, and set of biases. When they are isolated from each other and given the same question, their convergence or divergence is itself informative.

## 1.2 What Is New

Several prior works are related but distinct:

**Self-Consistency** (Wang et al., 2022) generates multiple reasoning chains from a *single* model and uses majority voting. BMAS uses *different* models -- this tests across training distributions, not just decoding variance.

**Mixture of Agents** (Wang et al., 2024) allows models to see each other's outputs in aggregation rounds. This produces collaborative refinement, but introduces the risk of error propagation: if one model produces a confident hallucination in round one, subsequent models may anchor to it.

**LLM-as-Judge** (Zheng et al., 2023) uses one model to evaluate another. BMAS uses one model to *synthesize* the outputs of several others -- the judge role is confined to the final synthesis phase, not the evaluation of correctness.

BMAS is the first framework to combine:
1. Strict blind isolation (no cross-contamination)
2. Multi-model diversity (different providers, architectures, training distributions)
3. Domain-stratified analysis (factual, regulatory, strategic)
4. Divergence-as-signal (not as failure)

## 1.3 Practical Motivation

This research emerged from operational experience building AEGIS, a cross-border EU government identity verification system, and AAHP (AI-to-AI Handoff Protocol), a structured multi-agent orchestration framework. In both systems, multi-agent pipelines are used for architecture decisions, compliance analysis, and implementation review.

A practical question arose: when multiple LLMs are used as independent reviewers in a pipeline, how much does their output actually differ? And when they differ, who is right?

BMAS is the formal answer to that question.

## 1.4 Contributions

This paper makes the following contributions:

1. **BMAS methodology**: A formalized blind multi-agent synthesis protocol with isolation constraints, metric suite, and synthesis strategies.
2. **Empirical study**: Results from 45 prompts across 12 LLMs in 3 domain strata, with pre-registered ground truth for Domains A and B.
3. **Divergence-as-signal hypothesis validation**: Statistical evidence that inter-model divergence predicts factual error rate.
4. **Synthesis strategy comparison**: Empirical evaluation of majority-vote, semantic centroid, and LLM-as-Judge synthesis against ground truth.
5. **Open dataset**: All prompts, raw model outputs, and metric scores released as a public benchmark.

## 1.5 Paper Structure

Section 2 reviews related work. Section 3 describes the BMAS methodology and experimental design. Section 4 presents results. Section 5 analyzes the divergence-hallucination correlation. Section 6 evaluates synthesis strategies. Section 7 discusses implications, limitations, and future work. Section 8 concludes.
