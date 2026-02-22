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

## Compute Infrastructure

### Hardware

The metrics pipeline (BERTScore via `roberta-large`, semantic embeddings via `sentence-transformers`) was executed using a remote GPU bridge over the local network, rather than the workstation GPU available in the development machine.

| | Local Workstation | GPU Bridge (remote) |
|---|---|---|
| **GPU** | NVIDIA Quadro M2000 | NVIDIA GeForce RTX 2080 Ti |
| **Architecture** | Maxwell (GM206) | Turing (TU102) |
| **Released** | February 2016 | September 2018 |
| **CUDA Cores** | 768 | 4,352 |
| **Tensor Cores** | — | 544 |
| **VRAM** | 4 GB GDDR5 | 11 GB GDDR6 |
| **Memory Bandwidth** | 106 GB/s | 616 GB/s |
| **FP32 Throughput** | ~1.7 TFLOPS | ~13.6 TFLOPS |
| **TDP** | 75 W | 260 W |
| **CUDA Compute Capability** | 5.0 | 7.5 |

The Quadro M2000 could not be used for inference at all: current versions of PyTorch (2.x) and `bert-score` require CUDA compute capability 6.0 or higher. Attempting to run the pipeline locally produced a hard failure (`cudaErrorNoKernelImageForDevice`) — not a performance degradation, but a complete incompatibility. A workstation GPU from 2016, less than a decade old, is already below the minimum requirements of modern ML frameworks.

### Remote GPU Bridge

The GPU bridge is a FastAPI service (`openclaw-gpu-bridge`) running on the RTX 2080 Ti machine and exposing a simple HTTP API (`/bertscore`, `/embed`). The BMAS metrics pipeline calls it via `GPU_BRIDGE_URL` environment variable and falls back gracefully to CPU if the bridge is unavailable.

```
Development machine (CPU only)
        │
        │  HTTP POST /bertscore  (LAN, ~1 ms RTT)
        ▼
GPU Bridge  (localhost:8765)
  ├── roberta-large  (BERTScore)
  └── all-MiniLM-L6-v2  (Embeddings / Cosine)
        │
        ▼
  NVIDIA RTX 2080 Ti — 11 GB VRAM
```

### Performance

Measured on the full BMAS dataset: 45 prompts × 12 models = 66 pairwise BERTScore comparisons per prompt.

| Metric | CPU (estimated) | GPU Bridge (measured) | Speedup |
|---|---|---|---|
| BERTScore per prompt (66 pairs) | ~4 min | ~0.6 s | **~400x** |
| Full pipeline (45 prompts) | ~3 h | ~5 min | **~36x** |
| Embedding (12 texts) | ~30 s | ~0.1 s | **~300x** |

The network overhead (HTTP over LAN) was negligible: round-trip latency was under 2 ms, and payload sizes were small enough that transfer time was not measurable against compute time.

> **Note:** The speedup figures reflect the difference between CPU inference and GPU inference, not between the two specific GPU models. The local GPU would have failed regardless of compute time due to the architecture incompatibility described above. The comparison illustrates the practical impact of running compute-heavy ML workloads on hardware released within the supported CUDA compute capability range.

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
