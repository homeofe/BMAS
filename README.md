# BMAS - Blind Multi-Agent Synthesis

**Research Project** | Private (until paper is ready for submission)

---

## What Is This?

BMAS is a methodology and experimental framework for measuring **convergence and divergence** across multiple large language models (LLMs) responding to identical prompts in isolation.

Inspired by the **Delphi method** in expert forecasting, BMAS enforces strict blind isolation: each model answers independently, with no knowledge of other models' responses. A synthesis layer then aggregates, compares, and validates the outputs.

**Core Hypothesis:**
> In factual, well-constrained domains (security, engineering, law, compliance), LLM response deviation is a function of *question ambiguity*, not model capability. Precise questions yield convergent answers. Divergence signals either hallucination, knowledge gap, or an underspecified question.

This hypothesis is testable, falsifiable, and has direct practical implications for high-stakes AI deployments.

---

## Why It Matters

Most multi-agent AI research focuses on **cooperative** agents that communicate and coordinate. BMAS takes the opposite approach: **competitive isolation** -- like independent peer review rather than a committee.

Practical applications:
- Use **convergence** as a quality signal in compliance, medical, and legal AI systems
- Use **divergence** to detect hallucinations or underspecified prompts
- Build **synthesis layers** that are more trustworthy than any single model

---

## Repository Structure

```
BMAS/
├── paper/                  # The research paper
│   ├── sections/           # LaTeX/Markdown sections (abstract, intro, ...)
│   ├── figures/            # Charts, heatmaps, deviation plots
│   └── references/         # BibTeX + reference notes
├── experiments/            # Experiment design and execution
│   ├── design.md           # Full experiment specification
│   ├── prompts/            # Prompt sets by domain
│   ├── raw-outputs/        # Raw model responses (JSON)
│   └── processed/          # Cleaned, scored, annotated outputs
├── src/                    # Implementation
│   ├── runner/             # Blind multi-model prompt runner
│   ├── metrics/            # Deviation measurement (BERTScore, cosine, jaccard)
│   ├── synthesis/          # Synthesis layer (majority-vote, centroid, LLM-as-Judge)
│   └── cli/                # CLI interface (failprompt integration)
├── results/                # Final experiment results and analysis
└── .ai/handoff/            # AAHP project state (STATUS, NEXT_ACTIONS, LOG, DASHBOARD)
```

---

## Models Under Study

| Model | Provider | Role |
|---|---|---|
| claude-sonnet-4-6 | Anthropic | Primary |
| claude-opus-4-6 | Anthropic | Primary |
| gpt-5.3-codex | OpenAI (via openai-codex) | Comparison |
| gemini-2.5-pro | Google | Comparison |
| perplexity/sonar-pro | Perplexity | Comparison |

All models receive identical prompts. No model sees another's output until the synthesis phase.

---

## Experiment Domains

1. **High-Precision Technical** - CVSS scores, PQC standards, cryptographic primitives
2. **Regulatory/Compliance** - GDPR articles, eIDAS clauses, TISAX requirements
3. **Strategic/Ambiguous** - Architecture decisions, security trade-offs, design choices

---

## Paper Status

- [ ] Experiment design finalized
- [ ] Prompt set v1 (20-30 prompts across 3 domains)
- [ ] Blind runs complete
- [ ] Metrics implementation
- [ ] Results analysis
- [ ] Paper draft
- [ ] Internal review
- [ ] arXiv preprint
- [ ] Submission (workshop/conference TBD)

---

## Connection to AAHP and failprompt

BMAS is built on the [AAHP protocol](https://github.com/homeofe/AAHP) for agent orchestration.
The runner integrates with [failprompt](https://github.com/homeofe/failprompt) as the CI/CD layer for automated experiment runs.

---

## Author

**Emre Kohler** | [Elvatis](https://elvatis.com)

---

## Available Languages

The paper is available in three languages. Sections 04-06 (Results, Divergence Analysis, Synthesis Evaluation) are auto-generated from experiment data and will be added to all language folders after the full experiment completes.

| Language | Index | Sections available |
|---|---|---|
| English (original) | [paper/sections/README.md](paper/sections/README.md) | 00, 01, 02, 03, 07, 08 (04-06 pending data) |
| Deutsch | [paper/sections/de/README.md](paper/sections/de/README.md) | 00, 01, 02, 03, 07, 08 (04-06 pending data) |
| Francais | [paper/sections/fr/README.md](paper/sections/fr/README.md) | 00, 01, 02, 03, 07, 08 (04-06 pending data) |
