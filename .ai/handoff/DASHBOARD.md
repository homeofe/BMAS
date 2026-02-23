# 📈 BMAS Dashboard

Last updated: 2026-02-22 01:00

| Task | Priority | Status | Owner |
|---|---|---|---|
| Ground truth Domain A+B | P1 | ✅ Done | Akido |
| Runner API integration | P2 | ✅ Done | Akido |
| Python env setup | P3 | ✅ Done | Akido |
| Paper: Related Work (02) | P4 | ✅ Done | Opus sub-agent |
| Pilot experiment (5x5) | P5 | ✅ Done | Akido |
| Paper sections 00, 01, 02, 03, 07, 08 | - | ✅ Done | Akido |
| German + French translations | - | ✅ Done | Akido |
| Automation scripts | - | ✅ Done | Akido |
| Full experiment (30x5=150) | P6 | 🔄 In Progress (PID 1811694) | Akido |
| Metric pipeline | P7 | ⏳ Auto after P6 | finish_pipeline.sh |
| Paper: sections 04-06 (data) | P8 | ⏳ Auto after P7 | generate_results_sections.py |
| Figures F1-F5 | P9 | ⏳ Auto after P7 | generate_figures.py |
| Final commit + WA notify | P10 | ⏳ Auto after P8+P9 | finish_pipeline.sh |
| Paper review | - | 👤 Waiting for Emre | Emre |
| Ground truth manual check | - | 👤 Waiting for Emre | Emre (3 items) |
| arXiv LaTeX conversion | - | ⏳ After review | Akido |
| Make repo public | - | 👤 Emre decision | Emre |

## Stats

| Item | Value | Status |
|---|---|---|
| Prompts written | 30/30 | ✅ |
| Ground truth Domain A | 10/10 | 🔒 Locked |
| Ground truth Domain B | 10/10 | 🔒 Locked |
| Paper sections (EN) | 6/8 (04-06 pending) | 🔄 |
| Paper sections (DE) | 6/8 (04-06 pending) | 🔄 |
| Paper sections (FR) | 6/8 (04-06 pending) | 🔄 |
| Models integrated | 5/5 | ✅ |
| Experiment runs | ~72/150 | 🔄 |
| Figures generated | 0/5 | ⏳ |

## Active Processes

| Process | PID | Log | Status |
|---|---|---|---|
| P6 Full runner | 1811694 | /tmp/bmas-fullrun.log | 🔄 Running |
| P6 Watcher | 1816456 | /tmp/bmas-watch.log | 🔄 Running |

## ⚠️ Manual Review Needed (3 items)

| Item | Flag | Action |
|---|---|---|
| A01 | CVSS 9.6 vs 9.8 discrepancy | Verify Fortinet advisory vector string |
| A10 | BSI TR-03116-4 PDF not accessed | Access primary source directly |
| B09 | EDPB ref WP248 vs 09/2022 | Confirm correct guideline number |
