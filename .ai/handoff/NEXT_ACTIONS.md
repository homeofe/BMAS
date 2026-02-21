# BMAS Next Actions

Last updated: 2026-02-22 00:50
Priority order: top = most critical.

---

## DONE

- [x] **Foundation** - README, design, 30 prompts, code scaffolding - commit 4772d04
- [x] **P1: Ground truth A+B** - 20 prompts pre-registered - commit 25a5395 (LOCKED)
- [x] **P2: Runner** - OpenClaw cron blind runner, live tested - commit 764f98c
- [x] **P3: Python deps** - all installed (sentence-transformers, bert-score, sklearn, matplotlib, etc.)
- [x] **P4: Paper related work** - 02-related-work.md - commit dafebe4
- [x] **P5: Pilot run** - 25/25 OK - commit ebd80d1
- [x] **Paper 00+01** - abstract + introduction - commit 4772d04
- [x] **Paper 03** - methodology (protocol, models, prompts, metrics, hypotheses) - commit dafebe4
- [x] **Paper 07** - discussion + limitations - commit dafebe4
- [x] **Paper 08** - conclusion - commit dafebe4
- [x] **Scripts** - finish_pipeline.sh + watch_and_finish.sh - commit dafebe4
- [x] **Metrics pipeline** - run_pipeline.py - commit dafebe4
- [x] **Figures generator** - generate_figures.py (F1-F5) - commit dafebe4
- [x] **Results sections generator** - generate_results_sections.py (auto-writes 04-06) - commit dafebe4

---

## IN PROGRESS (automated)

### P6 - Full experiment run (PID 1811694, watcher PID 1816456)
- 41/150 done at time of write
- Running: `python3 src/runner/runner.py --all --skip-existing --timeout 150`
- Log: /tmp/bmas-fullrun.log
- ETA: ~2-3 hours from start

### After P6 exits - fires automatically via watch_and_finish.sh:

**P7 - Metric pipeline**
- cosine similarity (all-mpnet-base-v2), BERTScore F1, Jaccard, DBSCAN outliers
- Output: results/aggregate.json + aggregate.csv

**P8 - Paper sections 04, 05, 06**
- Auto-generated from results data
- 04-results.md: stats tables, H1+H3 test results
- 05-divergence-analysis.md: outlier rates, H2 analysis
- 06-synthesis-evaluation.md: S1/S2/S3 comparison

**P9 - Figures (F1-F5)**
- F1: domain similarity heatmaps
- F2: cosine box plots by domain
- F3: BERTScore bars per prompt
- F4: token ratio vs divergence scatter
- F5: outlier rate by model

**P10 - Final docs + commit + push + WhatsApp**
- STATUS.md, DASHBOARD.md updated
- Git commit with full summary
- Push to origin main
- WA notification to +4915170113694

---

## REMAINING AFTER AUTOMATION (needs Emre)

- **Review paper sections 04-08** - data-driven, needs domain expert validation
- **Annotate ground truth scoring** - manual check of A01 CVSS, A10 BSI, B09 EDPB
- **arXiv LaTeX conversion** - Markdown -> LaTeX (P10: can be done after review)
- **Make repo public** - when Emre approves paper content
