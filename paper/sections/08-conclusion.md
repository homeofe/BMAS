# 🎯 8. Conclusion

This paper introduced **Blind Multi-Agent Synthesis (BMAS)**, a methodology for eliciting, comparing, and synthesizing responses from multiple large language models in strict isolation, and presented empirical results from a 540-run experiment across twelve frontier LLMs and three domain strata.

## 8.1 Summary of Contributions

We demonstrated that:

1. **Convergence is domain-dependent and measurable.** Across 45 prompts, Models A and B (technical and regulatory domains) showed consistently higher inter-model semantic similarity than Domain C (strategic and ambiguous prompts). [See Section 4 for exact values.]

2. **Divergence signals error in factual domains.** Models identified as semantic outliers by DBSCAN clustering showed lower factual accuracy against pre-registered ground truth than non-outlier models, supporting Hypothesis H2. This provides an empirical foundation for using divergence as a practical quality gate in AI-assisted decision systems.

3. **Synthesis quality varies by strategy and domain.** LLM-as-Judge (S3) synthesis produced the highest factual accuracy on Domains A and B, while majority-vote (S1) provided the most comprehensive coverage. Semantic centroid (S2) performed best as a concise representative summary. No single strategy dominated across all prompt types.

4. **Model verbosity is not a quality proxy.** We observed significant variation in response token counts across models on identical prompts (up to 6.5x ratio for some prompts), with no consistent correlation between response length and factual accuracy. Gemini 2.5-pro was consistently the most verbose; Sonar the most concise. These stylistic differences do not predict convergence.

## 8.2 Practical Takeaways

For practitioners deploying LLMs in regulated or high-stakes environments, BMAS suggests a practical architecture: run prompts against multiple independent model providers, measure semantic convergence, and route low-confidence (high-divergence) responses to human review. The overhead is justified by the reliability gain, particularly for compliance-critical questions where a single wrong answer has legal or safety consequences.

The pre-registration protocol used in this study - locking ground truth before any model runs - is transferable to any multi-model evaluation effort and prevents the confirmation bias that can arise when evaluators know the answers before designing the metrics.

## 8.3 Relationship to AAHP and failprompt

BMAS was developed in the context of AAHP (AI-to-AI Handoff Protocol), a structured multi-agent orchestration framework for production AI pipelines, and failprompt, a CLI tool for validating AI responses in CI/CD environments. Together, these three projects form an integrated toolkit for responsible multi-model AI deployment: AAHP provides the orchestration layer, failprompt provides the CI gate, and BMAS provides the empirical foundation for understanding when and why multi-model consensus is more reliable than single-model output.

All code, prompts, pre-registered ground truth, and experimental results are released as open datasets to support replication and extension of this work.

---

*The BMAS dataset, runner, metrics pipeline, and synthesis code are available at: https://github.com/homeofe/BMAS*
