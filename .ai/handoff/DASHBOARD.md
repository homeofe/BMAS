# BMAS Dashboard

Last updated: 2026-02-22

| Task | Priority | Status | Ready? | Owner |
|---|---|---|---|---|
| ~~Ground truth Domain A~~ | P1b | **DONE** | - | Akido |
| ~~Ground truth Domain B~~ | P1c | **DONE** | - | Akido |
| Runner API integration | P2 | **IN PROGRESS** | Yes | Akido/Sonnet |
| Python env setup | P3 | Open | Yes | Sonnet |
| Paper: Related Work (section 02) | P4 | Open | Yes | Sonar+Opus |
| ~~Pilot experiment (5 prompts)~~ | P5 | **DONE** | - | Akido |
| Full experiment (30x5) | P6 | Open | Blocked (P5) | Akido |
| Metric pipeline | P7 | Open | Blocked (P6) | Sonnet |
| Paper: sections 03-07 | P8 | Open | Blocked (P7) | Opus |
| Figures | P9 | Open | Blocked (P7) | Sonnet |
| Internal review + arXiv | P10 | Open | Blocked (P8+P9) | Emre+Akido |

## Stats

| Item | Count |
|---|---|
| Prompts written | 30/30 |
| Ground truth Domain A | 10/10 (LOCKED) |
| Ground truth Domain B | 10/10 (LOCKED) |
| Paper sections done | 2/8 (abstract, intro) |
| Models integrated | 0/5 |
| Experiment runs | 25/150 (pilot done) |
| Partial verification flags | 3 (manual review needed) |

## Partial Verification Flags
- A01: CVSS score discrepancy (9.6 vs 9.8) - verify Fortinet advisory vector string
- A10: BSI TR-03116-4 - primary PDF not directly accessed
- B09: EDPB DPIA guideline number (WP248 vs 09/2022) - confirm correct reference
