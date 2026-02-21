# BMAS Project Log

---

## 2026-02-21 - Project Foundation

**Phase:** Foundation
**Agent:** Akido (main session)
**Triggered by:** Emre Kohler (direct chat)

### What Was Done

- Cloned GitHub repo `homeofe/BMAS` (private) to workspace
- Created full project directory structure (experiments, paper, src, results, .ai/handoff)
- Wrote `README.md` with full project overview, hypothesis, model table, domain table
- Wrote `experiments/design.md` - complete pre-registered experiment specification:
  - 3 domains, 30 prompts total (10 per domain)
  - 5 models (M1-M5): claude-sonnet, claude-opus, gpt-5.3, gemini-2.5-pro, sonar-pro
  - 4 metrics: cosine similarity, BERTScore, Jaccard, DBSCAN outliers
  - 3 synthesis strategies: S1 majority-vote, S2 semantic centroid, S3 LLM-as-Judge
  - Timeline: 6-8 weeks to arXiv
- Wrote all 30 prompts across 3 domain files (A01-A10, B01-B10, C01-C10)
- Wrote `paper/sections/00-abstract.md` - full abstract
- Wrote `paper/sections/01-introduction.md` - full introduction with related work positioning
  - Differentiates clearly from Self-Consistency (Wang 2022), MoA (Wang 2024), LLM-as-Judge (Zheng 2023)
- Wrote `src/runner/runner.py` - blind prompt runner with isolation protocol
- Wrote `src/metrics/deviation.py` - full metrics pipeline (cosine, BERTScore, Jaccard, DBSCAN)
- Wrote `src/synthesis/synthesizer.py` - all 3 synthesis strategies implemented

### Architecture Decisions

- **Isolation system prompt:** neutral expert assistant framing, no hints about study or other models
- **Temperature:** not overridden - captures natural model behavior including decoding variance
- **Ground truth pre-registration:** required before any model runs (scientific integrity)
- **S3 judge model:** claude-opus-4-6 used as judge, not as respondent (to avoid bias)
- **Embedding model:** `all-mpnet-base-v2` as default (best accuracy/speed tradeoff in sentence-transformers)
- **DBSCAN eps=0.15:** distance threshold = 1-cosine_sim; eps=0.15 means sim<0.85 is "far"

### Next Actions

See NEXT_ACTIONS.md - P1 (ground truth) and P2 (runner API) are the critical path.

---

## 2026-02-22 - Ground Truth Research + Docs Update

**Phase:** Pre-experiment (ground truth pre-registration)
**Agent:** Akido (main session)

### What Was Done

- Spawned two Sonar sub-agents for Domain A and B research
- Both sub-agents failed to write files (produced simulation-style output instead of calling tools)
- Akido took over: performed all web research directly using web_search + web_fetch
- Wrote domain-A-ground-truth.md (10 prompts, verified against NVD, NIST FIPS, RFC 8446, OpenID specs, IETF, BSI)
- Wrote domain-B-ground-truth.md (10 prompts, verified against GDPR full text, eIDAS 2.0, NIS2, BSI C5, ISO 27001, TISAX, SOC 2 AICPA)
- Both files LOCKED as pre-registered ground truth before any model runs
- Language check passed: zero German characters in all BMAS files
- Updated STATUS.md, NEXT_ACTIONS.md, DASHBOARD.md to reflect completed steps
- Committed and pushed: commit 25a5395

### Verification Status

Domain A: 8/10 fully verified, 2 partial (A01 CVSS discrepancy, A10 BSI PDF not accessed directly)
Domain B: 9/10 fully verified, 1 partial (B09 EDPB guideline number needs confirmation)

### Architecture Decisions

- Ground truth pre-registration: done by Akido with web research, not by sub-agent
  - Lesson: sub-agents in "run" mode with Sonar model may produce simulation output; for file-writing tasks, main session is more reliable
- Manual review flags: documented explicitly in ground truth files; experiment runs blocked until Emre reviews 3 flagged items (or accepts them as-is for pilot)

### Next Actions

P2 (runner implementation) is in progress.
