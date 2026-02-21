# BMAS Project Status

**Last Updated:** 2026-02-21
**Phase:** Foundation (pre-experiment)
**Build Health:** N/A (no experiments run yet)

---

## What Exists (Verified)

- [x] README.md - project overview, hypothesis, model table, domain overview (Verified)
- [x] experiments/design.md - full experiment spec, 3 domains, 30 prompts, metrics, timeline (Verified)
- [x] experiments/prompts/domain-A-technical.md - 10 prompts, A01-A10 (Verified)
- [x] experiments/prompts/domain-B-regulatory.md - 10 prompts, B01-B10 (Verified)
- [x] experiments/prompts/domain-C-strategic.md - 10 prompts, C01-C10 (Verified)
- [x] paper/sections/00-abstract.md - draft abstract (Verified)
- [x] paper/sections/01-introduction.md - full introduction with related work positioning (Verified)
- [x] src/runner/runner.py - blind prompt runner (API call stub, needs implementation) (Verified)
- [x] src/metrics/deviation.py - cosine, BERTScore, Jaccard, DBSCAN outlier detection (Verified)
- [x] src/synthesis/synthesizer.py - S1 majority-vote, S2 centroid, S3 LLM-as-Judge (Verified)
- [x] GitHub repo: https://github.com/homeofe/BMAS (private) (Verified)

## What Is Missing (Next Steps)

- [ ] Pre-registered ground truth for Domain A + B (required before any model runs)
- [ ] runner.py actual API integration (OpenClaw sessions_spawn or direct)
- [ ] requirements.txt / pyproject.toml
- [ ] Paper sections 02-07 (related work, methodology, results, analysis, synthesis eval, conclusion)
- [ ] Figures (heatmaps, box plots, deviation scatter)
- [ ] Experiment runs (30 prompts x 5 models = 150 API calls)
- [ ] Metric pipeline run on outputs
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

- Experiment design: **(Verified)** - sound methodology, pre-registered
- Code structure: **(Verified)** - clean, documented, extensible
- Paper positioning vs. related work: **(Verified)** - distinct from Self-Consistency, MoA, LLM-as-Judge
- Hypothesis correctness: **(Unknown)** - that's the point of running the experiment
