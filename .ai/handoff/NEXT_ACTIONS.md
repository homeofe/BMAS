# BMAS Next Actions

Last updated: 2026-02-22 01:00
Priority: top = most critical.

---

## ✅ Done

- ✅ Foundation - README, design, 30 prompts, code scaffolding - commit 4772d04
- ✅ P1: Ground truth A+B - 20 prompts pre-registered - commit 25a5395 (🔒 LOCKED)
- ✅ P2: Runner - OpenClaw cron blind runner, live tested - commit 764f98c
- ✅ P3: Python deps - sentence-transformers, bert-score, sklearn, matplotlib all installed
- ✅ P4: Paper related work - 02-related-work.md - commit dafebe4
- ✅ P5: Pilot run - 25/25 OK - commit ebd80d1
- ✅ Paper 00 + 01 - abstract + introduction - commit 4772d04
- ✅ Paper 03 - methodology (protocol, models, prompts, metrics, hypotheses) - commit dafebe4
- ✅ Paper 07 - discussion + limitations - commit dafebe4
- ✅ Paper 08 - conclusion - commit dafebe4
- ✅ Automation scripts - finish_pipeline.sh + watch_and_finish.sh - commit dafebe4
- ✅ Metrics pipeline - run_pipeline.py - commit dafebe4
- ✅ Figures generator - generate_figures.py (F1-F5) - commit dafebe4
- ✅ Results sections generator - generate_results_sections.py (auto-writes 04-06) - commit dafebe4
- ✅ German translations - paper/sections/de/ (6 sections) - commit 4e0cd61
- ✅ French translations - paper/sections/fr/ (6 sections) - commit 4e0cd61
- ✅ Language index - paper/sections/README.md with EN/DE/FR links - commit 4e0cd61

---

## 🔄 In Progress (automated)

### P6 - Full experiment run (PID 1811694, watcher PID 1816456)
- ~72/150 done at time of write
- Running: `python3 src/runner/runner.py --all --skip-existing --timeout 150`
- Log: /tmp/bmas-fullrun.log

---

## ⏳ Auto-fires when P6 exits (watch_and_finish.sh)

- ⏳ **P7** - Metric pipeline (cosine, BERTScore, Jaccard, DBSCAN)
  - Output: results/aggregate.json + aggregate.csv
- ⏳ **P8** - Paper sections 04, 05, 06 (auto-generated from results data)
  - 04-results.md, 05-divergence-analysis.md, 06-synthesis-evaluation.md
- ⏳ **P9** - Figures F1-F5 (paper/figures/)
- ⏳ **P10** - Final docs update + git commit + push + WhatsApp notification

---

## 👤 Needs Emre (after P10)

- 👤 Review paper sections 04-08 (data-driven, needs domain expert validation)
- 👤 Annotate ground truth scoring for 3 flagged items (A01, A10, B09)
- 👤 Decide: arXiv submission timing
- 👤 Decide: make repo public

---

## ⏳ Pending (after Emre review)

- ⏳ Translate sections 04-06 to German + French (after English versions are final)
- ⏳ arXiv LaTeX conversion (Markdown -> LaTeX)
- ⏳ arXiv submission
