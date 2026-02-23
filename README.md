# BMAS - Blind Multi-Agent Synthesis

**Research Project** | Status: **COMPLETE — Paper ready for arXiv**

---

## What Is This?

BMAS is a methodology and experimental framework for measuring **convergence and divergence** across multiple large language models (LLMs) responding to identical prompts in isolation.

Inspired by the **Delphi method** in expert forecasting, BMAS enforces strict blind isolation: each model answers independently, with no knowledge of other models' responses. A synthesis layer then aggregates, compares, and validates the outputs.

**Core Hypothesis:**
> In factual, well-constrained domains (security, engineering, law, compliance), LLM response deviation is a function of *question ambiguity*, not model capability. Precise questions yield convergent answers. Divergence signals either hallucination, knowledge gap, or an underspecified question.

This hypothesis is testable, falsifiable, and has direct practical implications for high-stakes AI deployments.

---

## Why It Matters

Most multi-agent AI research focuses on **cooperative** agents that communicate and coordinate. BMAS takes the opposite approach: **competitive isolation** — like independent peer review rather than a committee.

Practical applications:
- Use **convergence** as a quality signal in compliance, medical, and legal AI systems
- Use **divergence** to detect hallucinations or underspecified prompts
- Build **synthesis layers** that are more trustworthy than any single model

---

## Dataset

| | |
|---|---|
| **Prompts** | 45 (A01–A15, B01–B15, C01–C15) |
| **Models** | 12 (M1–M12) |
| **Domains** | 3 (High-Precision Technical, Regulatory/Compliance, Strategic/Ambiguous) |
| **Total responses** | 540 (45 × 12) |
| **Pairwise comparisons** | 66 per prompt × 45 = 2,970 total |

### 📊 Key Results

| Metric | Overall Mean | Overall Min |
|---|---|---|
| **Cosine similarity** (all-MiniLM-L6-v2) | **0.491** | — |
| **BERTScore F1** (roberta-large) | **0.815** | — |

- Convergence is highest in the **Technical domain** (precise, well-constrained prompts)
- Divergence is highest in the **Strategic domain** (ambiguous, open-ended prompts)
- DBSCAN outlier detection identified outlier models in 43/45 prompts analyzed

---

## Repository Structure

```
BMAS/
├── paper/                  # The research paper
│   ├── sections/           # Paper sections (EN + 5 translations)
│   │   ├── *.md            # English originals (00-abstract … 08-conclusion)
│   │   ├── de/             # Deutsch
│   │   ├── es/             # Español
│   │   ├── fr/             # Français
│   │   ├── it/             # Italiano
│   │   └── pl/             # Polski
│   ├── figures/            # Charts: F1-heatmaps, F2-boxplot, F3-bertscore,
│   │                       #         F4-token-scatter, F5-outlier-frequency
│   └── references/         # BibTeX + reference notes
├── experiments/            # Experiment design and execution
│   ├── design.md           # Full experiment specification
│   ├── prompts/            # Prompt sets by domain
│   └── raw-outputs/        # Raw model responses (JSON)
├── src/                    # Implementation
│   ├── metrics/            # Deviation measurement (BERTScore, cosine, jaccard, DBSCAN)
│   └── runner/             # Blind multi-model prompt runner
├── results/                # Metric results per prompt + aggregate
│   ├── A01-metrics.json … C15-metrics.json  # 45 individual result files
│   ├── aggregate.csv       # Summary table (45 rows)
│   └── aggregate.json      # Full structured results
└── .ai/handoff/            # AAHP project state (STATUS, NEXT_ACTIONS, LOG)
```

---

## Models Under Study

12 models (M1–M12) spanning major frontier LLM providers. All models receive identical prompts in parallel. No model sees another's output until the synthesis phase.

---

## Experiment Domains

| Domain | Prompts | Description |
|---|---|---|
| **A — High-Precision Technical** | A01–A15 | CVSS scores, PQC standards, cryptographic primitives |
| **B — Regulatory/Compliance** | B01–B15 | GDPR articles, eIDAS clauses, TISAX requirements |
| **C — Strategic/Ambiguous** | C01–C15 | Architecture decisions, security trade-offs, design choices |

---

## Paper Status

- ✅ Experiment design finalized
- ✅ Prompt set v1 — 45 prompts across 3 domains
- ✅ Blind runs complete — 540 model responses collected
- ✅ Metrics implementation (cosine, BERTScore, Jaccard, DBSCAN)
- ✅ Results analysis — all 45 prompts fully processed
- ✅ Figures generated (F1–F5)
- ✅ Paper draft — all 9 sections written (EN + 5 translations)
- ⬜ Internal review
- ⬜ arXiv preprint
- ⬜ Submission (workshop/conference TBD)

---

## Compute Infrastructure

### Hardware

The metrics pipeline (BERTScore via `roberta-large`, semantic embeddings via `all-MiniLM-L6-v2`) was executed using a remote GPU bridge over the local network.

| | Local Workstation | GPU Bridge (remote) |
|---|---|---|
| **GPU** | NVIDIA Quadro M2000 | NVIDIA GeForce RTX 2080 Ti |
| **Architecture** | Maxwell (GM206) | Turing (TU102) |
| **CUDA Compute Capability** | 5.0 | 7.5 |
| **VRAM** | 4 GB GDDR5 | 11 GB GDDR6 |
| **FP32 Throughput** | ~1.7 TFLOPS | ~13.6 TFLOPS |

The local GPU (Quadro M2000) was unusable for inference: PyTorch 2.x requires CUDA compute capability ≥ 6.0. Any attempt to run the pipeline locally produced `cudaErrorNoKernelImageForDevice` — a hard failure, not a performance issue.

### Remote GPU Bridge (`openclaw-gpu-bridge`)

A FastAPI service running on the RTX 2080 Ti machine, exposing a simple HTTP API:

```
Development machine (CPU only)
        │
        │  HTTP POST /embed | /bertscore  (LAN, ~1 ms RTT)
        ▼
openclaw-gpu-bridge  (your-gpu-host:8765)
  ├── roberta-large         (BERTScore)
  └── all-MiniLM-L6-v2     (Cosine embeddings)
        │
        ▼
  NVIDIA RTX 2080 Ti — 11 GB VRAM, 4352 CUDA Cores, 544 Tensor Cores
```

The metrics pipeline calls the bridge via `GPU_BRIDGE_URL` environment variable and falls back gracefully to CPU if the bridge is unavailable.

### Performance

Measured on the full BMAS dataset: 45 prompts × 12 models = 66 pairwise comparisons per prompt.

| Metric | CPU (estimated) | GPU Bridge (measured) | Speedup |
|---|---|---|---|
| BERTScore per prompt (66 pairs) | ~4 min | ~0.6 s | **~400×** |
| Full pipeline (45 prompts) | ~3 h | ~5 min | **~36×** |
| Embedding (12 texts) | ~30 s | ~0.1 s | **~300×** |

---

## Paper Sections

All 9 paper sections are available in English and 5 translations:

| Language | Directory | Sections |
|---|---|---|
| English (original) | `paper/sections/` | 00–08 (complete) |
| Deutsch | `paper/sections/de/` | 00–08 (complete) |
| Español | `paper/sections/es/` | 00–08 (complete) |
| Français | `paper/sections/fr/` | 00–08 (complete) |
| Italiano | `paper/sections/it/` | 00–08 (complete) |
| Polski | `paper/sections/pl/` | 00–08 (complete) |

Sections: `00-abstract`, `01-introduction`, `02-related-work`, `03-methodology`, `04-results`, `05-divergence-analysis`, `06-synthesis-evaluation`, `07-discussion-limitations`, `08-conclusion`.

---

## Connection to AAHP and failprompt

BMAS is built on the [AAHP protocol](https://github.com/homeofe/AAHP) for agent orchestration.
The runner integrates with [failprompt](https://github.com/homeofe/failprompt) as the CI/CD layer for automated experiment runs.

---

## Author

**Emre Kohler** | [Elvatis](https://elvatis.com)
