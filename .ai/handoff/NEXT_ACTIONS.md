# BMAS Next Actions

Priority order: top = most critical.
Last updated: 2026-02-22

---

## DONE

- [x] **P1a: Prompt sets** - 30 prompts across 3 domains (A01-A10, B01-B10, C01-C10) - commit 4772d04
- [x] **P1b: Ground truth Domain A** - 10/10 prompts verified against NIST, NVD, IETF RFCs, OpenID specs, BSI - commit 25a5395
- [x] **P1c: Ground truth Domain B** - 10/10 prompts verified against GDPR, eIDAS 2.0, NIS2, BSI C5, ISO 27001, TISAX - commit 25a5395
- [x] **Paper: Abstract** - draft complete - commit 4772d04
- [x] **Paper: Introduction** - full section with related work positioning - commit 4772d04
- [x] **Code: metrics/deviation.py** - cosine, BERTScore, Jaccard, DBSCAN - commit 4772d04
- [x] **Code: synthesis/synthesizer.py** - S1, S2, S3 strategies - commit 4772d04
- [x] **P5: Pilot experiment** - 25/25 runs OK (A01, A05, B01, B05, C01 x M1-M5) - 2026-02-22

---

## OPEN (priority order)

## [P2] Implement runner.py API integration - IN PROGRESS
**Why:** Actual model calls needed to run experiments
**Approach:** OpenClaw sessions_spawn (isolated mode) for each model
**Output:** src/runner/runner.py with working run_model() function
**Also needed:** src/runner/__init__.py, tests/test_runner.py (dry-run test)
**Effort:** Medium

## [P3] Python environment setup
**Output:** verified requirements.txt + install instructions in README
**Deps to install:** sentence-transformers, bert-score, scikit-learn, numpy, tqdm, pandas, matplotlib, seaborn
**Who:** Sonnet
**Effort:** Low

## [P4] Paper: Related Work (section 02)
**Output:** paper/sections/02-related-work.md
**Topics:** Delphi method (Dalkey 1963), Self-Consistency (Wang 2022), MoA (Wang 2024), LLM-as-Judge (Zheng 2023), BERTScore (Zhang 2020), Constitutional AI (Anthropic 2022)
**Who:** Sonar (research) + Opus (writing)
**Effort:** Medium

## ~~[P5] Pilot experiment~~ - DONE
25/25 OK. Token spread: 3.6x-6.5x across prompts. M4 most verbose, M5 most concise.
Raw outputs in experiments/raw-outputs/ (A01-C01, M1-M5).

## [P6] Full experiment run (30 prompts x 5 models)
**Blocked by:** Emre approval (pilot passed, ready to go)
**Output:** 150 JSON files in experiments/raw-outputs/
**Effort:** Low execution, moderate cost (~300-500k tokens estimated)

## [P7] Metric pipeline execution
**Blocked by:** P6 (for full results) - can run on pilot data now for validation
**Output:** results/ folder with per-prompt metric reports + aggregate CSV
**Effort:** Medium (compute time + validation)

## [P8] Paper sections 03-07
**Blocked by:** P7 (need results)
**Sections:**
  - 03-methodology.md
  - 04-results.md
  - 05-divergence-analysis.md
  - 06-synthesis-evaluation.md
  - 07-discussion-limitations.md
  - 08-conclusion.md
**Effort:** High

## [P9] Figures
**Blocked by:** P7
**Types:** Similarity heatmap (NxN), box plot (metric by domain), scatter (divergence vs hallucination)
**Output:** paper/figures/
**Effort:** Medium

## [P10] Internal review + arXiv submission
**Blocked by:** P8, P9
**Format:** LaTeX (convert from Markdown sections)
**Effort:** Medium (Emre reviews; Akido formats)

---

## Manual Review Required (before first model runs)
- A01: Verify exact Fortinet CVSS vector string (9.6 vs 9.8 discrepancy)
- A10: Verify BSI TR-03116-4 directly from BSI PDF
- B09: Verify correct EDPB guideline number for DPIA (WP248 vs 09/2022)
