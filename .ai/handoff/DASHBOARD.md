# BMAS Dashboard

Last updated: 2026-02-22 00:50

| Task | Priority | Status | Owner |
|---|---|---|---|
| ~~Ground truth Domain A+B~~ | P1 | DONE | Akido |
| ~~Runner API integration~~ | P2 | DONE | Akido |
| ~~Python env setup~~ | P3 | DONE | Akido |
| ~~Paper: Related Work (02)~~ | P4 | DONE | Opus sub-agent |
| ~~Pilot experiment (5x5)~~ | P5 | DONE | Akido |
| Full experiment (30x5=150) | P6 | **IN PROGRESS** (PID 1811694) | Akido |
| Metric pipeline | P7 | AUTO after P6 | finish_pipeline.sh |
| Paper: sections 04-06 (data) | P8 | AUTO after P7 | generate_results_sections.py |
| Figures F1-F5 | P9 | AUTO after P7 | generate_figures.py |
| Final commit + WA notify | P10 | AUTO after P8+P9 | finish_pipeline.sh |
| Paper review | - | Waiting for Emre | Emre |
| Ground truth manual check | - | Waiting for Emre | Emre (3 items) |
| arXiv LaTeX conversion | - | After review | Akido |
| Make repo public | - | After paper ready | Emre decision |

## Stats

| Item | Count |
|---|---|
| Prompts written | 30/30 |
| Ground truth Domain A | 10/10 (LOCKED) |
| Ground truth Domain B | 10/10 (LOCKED) |
| Paper sections written | 6/8 (00,01,02,03,07,08) |
| Paper sections pending (auto) | 3/8 (04,05,06) |
| Models integrated | 5/5 |
| Experiment runs | ~41/150 (in progress) |
| Figures generated | 0/5 (pending P7) |

## Active Processes

| Process | PID | Log | Status |
|---|---|---|---|
| P6 Full runner | 1811694 | /tmp/bmas-fullrun.log | Running |
| P6 Watcher | 1816456 | /tmp/bmas-watch.log | Running |

## Partial Verification Flags (manual review before final)
- A01: CVSS score 9.6 vs 9.8 - verify Fortinet advisory vector string
- A10: BSI TR-03116-4 primary PDF not directly accessed
- B09: EDPB guideline number (WP248 vs 09/2022)
