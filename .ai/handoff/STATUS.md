# BMAS Project Status

**Last Updated:** 2026-02-22
**Phase:** Runner Implementation (P2)
**Build Health:** N/A (no experiments run yet)

---

## What Exists (Verified)

### Foundation (commit 4772d04)
- [x] README.md - project overview, hypothesis, model table, domain overview (Verified)
- [x] experiments/design.md - full experiment spec, 3 domains, 30 prompts, metrics, timeline (Verified)
- [x] experiments/prompts/domain-A-technical.md - 10 prompts, A01-A10 (Verified)
- [x] experiments/prompts/domain-B-regulatory.md - 10 prompts, B01-B10 (Verified)
- [x] experiments/prompts/domain-C-strategic.md - 10 prompts, C01-C10 (Verified)
- [x] paper/sections/00-abstract.md - draft abstract (Verified)
- [x] paper/sections/01-introduction.md - full introduction with related work positioning (Verified)
- [x] src/runner/runner.py - blind prompt runner structure (API call stub - not yet integrated) (Verified)
- [x] src/metrics/deviation.py - cosine, BERTScore, Jaccard, DBSCAN outlier detection (Verified)
- [x] src/synthesis/synthesizer.py - S1 majority-vote, S2 centroid, S3 LLM-as-Judge (Verified)
- [x] requirements.txt (Verified)
- [x] GitHub repo: https://github.com/homeofe/BMAS (private) (Verified)

### Ground Truth (commit 25a5395) - LOCKED
- [x] experiments/prompts/domain-A-ground-truth.md - 10/10 prompts (Verified)
  - 8/10 fully verified against primary sources
  - 2/10 partial: A01 (CVSS 9.6 vs 9.8 discrepancy - needs manual check), A10 (BSI TR-03116-4 direct PDF not accessed)
- [x] experiments/prompts/domain-B-ground-truth.md - 10/10 prompts (Verified)
  - 9/10 fully verified against primary sources
  - 1/10 partial: B09 (EDPB guideline number - WP248 vs 09/2022)
- [x] Both files LOCKED - pre-registered before any model runs

## What Is In Progress

- [ ] **P2: runner.py API integration** - OpenClaw sessions_spawn or direct provider API (IN PROGRESS)

## What Is Missing (Next Steps)

- [ ] requirements.txt Python env setup + install test
- [ ] Paper sections 02-07
- [ ] Figures
- [ ] Experiment runs (30 prompts x 5 models = 150 API calls)
- [ ] Metric pipeline run
- [ ] Analysis + writing

## Model Status

| Model | Integration | Test Run |
|---|---|---|
| M1 (claude-sonnet-4-6) | Pending | No |
| M2 (claude-opus-4-6) | Pending | No |
| M3 (gpt-5.3-codex) | Pending | No |
| M4 (gemini-2.5-pro) | Pending | No |
| M5 (sonar-pro) | Pending | No |

## Confidence Levels

- Experiment design: **(Verified)**
- Prompts (all 30): **(Verified)**
- Ground truth Domain A: **(Verified, 2 partial items flagged)**
- Ground truth Domain B: **(Verified, 1 partial item flagged)**
- Code structure (runner stub, metrics, synthesis): **(Verified)**
- Paper positioning: **(Verified)**
- Hypothesis correctness: **(Unknown)** - that is the experiment
