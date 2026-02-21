# BMAS Next Actions

Priority order: top = most critical.

---

## [P1] Write Ground Truth for Domain A + B
**Why:** Must be pre-registered BEFORE any model runs. Scientific integrity.
**Output:** `experiments/prompts/domain-A-ground-truth.md` + `domain-B-ground-truth.md`
**Who:** Sonnet or Opus (research phase); Emre reviews
**Effort:** Medium (requires reading primary sources: NIST FIPS, RFCs, GDPR text, TISAX)

## [P2] Implement runner.py API integration
**Why:** Actual model calls needed to run experiments
**Option A:** OpenClaw sessions_spawn (isolated, already available)
**Option B:** Direct provider APIs (Anthropic, OpenAI, Google, Perplexity)
**Output:** `src/runner/runner.py` with working `run_model_via_openclaw()`
**Who:** Sonnet (implementation)
**Effort:** Medium

## [P3] Add requirements.txt + pyproject.toml
**Output:** `requirements.txt`, `pyproject.toml`
**Deps:** sentence-transformers, bert-score, scikit-learn, numpy, tqdm
**Who:** Sonnet
**Effort:** Low

## [P4] Write paper section 02 - Related Work
**Output:** `paper/sections/02-related-work.md`
**Content:** Delphi method, Self-Consistency, MoA, LLM-as-Judge, BERTScore, Constitutional AI
**Who:** Sonar (research) + Opus (writing)
**Effort:** Medium

## [P5] Run Pilot Experiment (5 prompts, all 5 models)
**Scope:** A01, A05, B01, B05, C01 - one from each sub-domain
**Purpose:** Validate runner, check output quality, estimate token costs
**Who:** Akido (orchestrate), Sonnet (debug if needed)
**Effort:** Low (once runner works)

## [P6] Write paper sections 03-07 (after pilot results)
**Sections:**
- 03-methodology.md
- 04-results.md
- 05-divergence-analysis.md
- 06-synthesis-evaluation.md
- 07-discussion-limitations.md
- 08-conclusion.md
**Who:** Opus (primary), Sonnet (review)
**Effort:** High

## [P7] Generate figures
**Types:** Similarity heatmap (NxN per prompt), box plot (metric by domain), scatter (divergence vs. hallucination rate)
**Tools:** matplotlib, seaborn
**Output:** `paper/figures/`
**Who:** Sonnet
**Effort:** Medium (after results available)

## [P8] Internal review round
**Emre reviews:** methodology, claims, conclusions
**Akido reviews:** references, formatting, consistency
**Effort:** Emre's time

## [P9] arXiv preprint submission
**Target:** cs.AI or cs.CL category
**Format:** LaTeX (convert from Markdown sections)
**Effort:** Low-Medium (once paper is written)

---

## Blocked

- All experiment runs: blocked on [P1] ground truth + [P2] runner implementation
