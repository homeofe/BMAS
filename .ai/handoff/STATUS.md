# BMAS Project Status

**Last Updated:** 2026-02-22
**Phase:** Pilot Complete - Full Run (P6) + Metrics (P7) Ready
**Build Health:** Pilot 25/25 OK

---

## Completed (Verified)

### Foundation (commit 4772d04)
- [x] README.md (Verified)
- [x] experiments/design.md - 3 domains, 30 prompts, metrics, timeline (Verified)
- [x] experiments/prompts/domain-A-technical.md - A01-A10 (Verified)
- [x] experiments/prompts/domain-B-regulatory.md - B01-B10 (Verified)
- [x] experiments/prompts/domain-C-strategic.md - C01-C10 (Verified)
- [x] paper/sections/00-abstract.md (Verified)
- [x] paper/sections/01-introduction.md - full with related work positioning (Verified)
- [x] src/metrics/deviation.py - cosine, BERTScore, Jaccard, DBSCAN (Verified)
- [x] src/synthesis/synthesizer.py - S1, S2, S3 (Verified)
- [x] requirements.txt (Verified)
- [x] GitHub: https://github.com/homeofe/BMAS (private)

### Ground Truth (commit 25a5395) - LOCKED
- [x] domain-A-ground-truth.md - 10/10 (8 fully verified, 2 partial - A01 CVSS discrepancy, A10 BSI PDF)
- [x] domain-B-ground-truth.md - 10/10 (9 fully verified, 1 partial - B09 EDPB guideline ref)
- [x] Status: LOCKED, pre-registered before any model runs

### Runner (commit 764f98c + 350449d)
- [x] src/runner/runner.py - full OpenClaw cron-based blind runner (Verified)
  - Isolated cron session per model (strict blind isolation)
  - Reads full response from session JSONL (no truncation)
  - --dry-run, --pilot, --all, --skip-existing, --models filters
  - Live tested: A01/M1 = 3227 tokens, 63s

### Pilot Run (commit ebd80d1) - DONE
- [x] 25/25 runs OK (A01, A05, B01, B05, C01 x M1-M5)
- [x] Raw outputs in experiments/raw-outputs/

**Pilot token spread:**

| Prompt | Domain | M1 | M2 | M3 | M4 | M5 | Ratio |
|---|---|---|---|---|---|---|---|
| A01 | technical | 3227 | 674 | 523 | 3418 | 527 | 6.5x |
| A05 | technical | 5741 | 2189 | 1899 | 3956 | 1286 | 4.5x |
| B01 | regulatory | 1024 | 305 | 437 | 1106 | 374 | 3.6x |
| B05 | regulatory | 933 | 317 | 397 | 1658 | 412 | 5.2x |
| C01 | strategic | 1917 | 920 | 1145 | 2911 | 456 | 6.4x |

**Early observations:**
- Regulatory prompts show tightest spread (aligns with hypothesis)
- M4 (Gemini 2.5-pro): consistently most verbose
- M5 (Sonar): consistently most concise
- M2 (Opus) shorter than M1 (Sonnet) despite being "larger" model

## Model Status

| Model | Integration | Pilot Runs | Status |
|---|---|---|---|
| M1 (claude-sonnet-4-6) | Done | 5/5 | OK |
| M2 (claude-opus-4-6) | Done | 5/5 | OK |
| M3 (gpt-5.3-codex) | Done | 5/5 | OK |
| M4 (gemini-2.5-pro) | Done | 5/5 | OK |
| M5 (sonar-pro) | Done | 5/5 | OK |

## What Is Next

- [ ] **P6:** Full experiment (30 prompts x 5 = 150 calls) - awaiting Emre approval
- [ ] **P7:** Metric pipeline (sentence-transformers + BERTScore + Jaccard + DBSCAN) - can start on pilot data
- [ ] **P3:** Python env setup (pip install requirements.txt - needs venv or --break-system-packages)
- [ ] **P4:** Paper section 02 - Related Work
- [ ] **P8-P10:** Paper sections 03-07, figures, review, arXiv (blocked on P7)

## Confidence Levels

- Experiment design: **(Verified)**
- Prompts (all 30): **(Verified)**
- Ground truth A+B: **(Verified, 3 partial flags)**
- Runner: **(Verified - live tested)**
- Pilot data: **(Verified - 25/25 real model responses)**
- Hypothesis correctness: **(Unknown)** - semantic metrics needed to confirm
