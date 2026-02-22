# BMAS Paper Sections

This directory contains the full BMAS research paper in Markdown format, organized by section and language.

## Available Languages

| Language | Directory | Status |
|---|---|---|
| English (original) | `/paper/sections/` | 6/8 sections complete (04-06 pending experiment data) |
| German | `/paper/sections/de/` | 6/8 sections complete (04-06 pending experiment data) |
| French | `/paper/sections/fr/` | 6/8 sections complete (04-06 pending experiment data) |

## English Sections

| Section | Title | File | Status |
|---|---|---|---|
| 00 | Abstract | [00-abstract.md](00-abstract.md) | Done |
| 01 | Introduction | [01-introduction.md](01-introduction.md) | Done |
| 02 | Related Work | [02-related-work.md](02-related-work.md) | Done |
| 03 | Methodology | [03-methodology.md](03-methodology.md) | Done |
| 04 | Results | [04-results.md](04-results.md) | Auto-generated after P7 |
| 05 | Divergence Analysis | [05-divergence-analysis.md](05-divergence-analysis.md) | Auto-generated after P7 |
| 06 | Synthesis Evaluation | [06-synthesis-evaluation.md](06-synthesis-evaluation.md) | Auto-generated after P7 |
| 07 | Discussion and Limitations | [07-discussion-limitations.md](07-discussion-limitations.md) | Done |
| 08 | Conclusion | [08-conclusion.md](08-conclusion.md) | Done |

## Language Indexes

- [Deutsch (German)](de/README.md)
- [Francais (French)](fr/README.md)

## Notes on Translated Sections

- Sections 04, 05, 06 are auto-generated from experiment data and will be added to all language folders after the full experiment (P6) and metric pipeline (P7) complete.
- Technical terms, model names, dataset identifiers, and formula notation are kept in English across all languages.
- Citation author names and publication years are kept in their original form.
- The data-driven generation script (`src/paper/generate_results_sections.py`) will need a separate translation pass for sections 04-06 after the English versions are generated.
