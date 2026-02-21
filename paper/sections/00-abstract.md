# Abstract

We introduce **Blind Multi-Agent Synthesis (BMAS)**, a methodology for measuring convergence and divergence across multiple large language models (LLMs) responding to identical prompts in strict isolation. Inspired by the Delphi method in expert forecasting, BMAS enforces per-model response isolation: no model observes another's output before the synthesis phase.

We evaluate five state-of-the-art LLMs across three domain strata: (A) high-precision technical questions with verifiable ground truth, (B) regulatory and compliance questions with authoritative legal sources, and (C) strategic and architectural questions with legitimate expert disagreement. Using semantic similarity (BERTScore, cosine embedding distance), factual accuracy against pre-registered ground truth, and outlier detection via DBSCAN clustering, we quantify inter-model deviation and its relationship to domain type and hallucination rate.

Our central hypothesis is that in well-constrained, factual domains, LLM responses converge to a degree that allows **consensus as a quality signal**: high inter-model agreement predicts factual correctness, while significant divergence signals either model hallucination or an underspecified question. We further evaluate three synthesis strategies -- majority-vote claim aggregation, semantic centroid selection, and LLM-as-Judge synthesis -- against ground truth, measuring which produces the most accurate and complete synthesized output.

BMAS has direct practical implications for high-stakes AI deployments in government, healthcare, and legal systems, where no single model output can be trusted unconditionally. By treating **divergence as an anomaly signal** rather than a coordination failure, BMAS provides a practical quality assurance layer for production LLM systems.

**Keywords:** large language models, multi-agent systems, consensus, hallucination detection, Delphi method, semantic similarity, AI quality assurance
