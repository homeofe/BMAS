#!/usr/bin/env python3
"""
Update paper sections with REAL final numbers from complete 45×12 pipeline
(including clean M6 sonar-deep-research data).

Real numbers:
  Domain A: cosine=0.550, bertscore=0.818
  Domain B: cosine=0.524, bertscore=0.822
  Domain C: cosine=0.485, bertscore=0.816
  Overall:  cosine=0.520, bertscore=0.819

Outlier rates (sorted by rate):
  M6  sonar-deep-research  0.67 (67%) - HIGHEST
  M7  gemini-3-pro-preview 0.64 (64%)
  M9  gemini-2.5-flash     0.42 (42%)
  M8  gemini-3-flash       0.40 (40%)
  M10 gpt-5.2              0.38 (38%)
  M11 gpt-5.1              0.38 (38%)
  M1  claude-sonnet-4-6    0.36 (36%)
  M5  sonar-pro            0.36 (36%)
  M4  gemini-2.5-pro       0.27 (27%)
  M3  gpt-5.3-codex        0.24 (24%)
  M2  claude-opus-4-6      0.22 (22%)
  M12 claude-sonnet-4-5    0.18 (18%) - LOWEST
"""

import os
import re

SECTIONS_DIR = "/home/chef-linux/.openclaw/workspace/BMAS/paper/sections"

# ---------------------------------------------------------------------------
# Corrected metric number replacements (previous fix used wrong interim values)
# ---------------------------------------------------------------------------

# These patterns replace the values the previous fix_paper_sections.py wrote in
# (which were based on the corrupted M6 data) with the real final values.

METRIC_SUBS = {
    # EN
    "en": [
        # Domain A cosine (old wrong → real)
        (r"mean cosine similarity of 0\.479 \(SD = 0\.038\)", "mean cosine similarity of 0.550 (SD = 0.142)"),
        (r"cosine similarity of 0\.479", "cosine similarity of 0.550"),
        # Domain A BERTScore
        (r"BERTScore F1 mean was 0\.811", "BERTScore F1 mean was 0.818"),
        # Domain B cosine (was "0.508" — previous interim)
        (r"mean cosine similarity of 0\.508", "mean cosine similarity of 0.524"),
        (r"cosine similarity of 0\.508", "cosine similarity of 0.524"),
        # Domain B BERTScore
        (r"BERTScore.*?0\.820", "BERTScore mean of 0.822"),
        # Domain C cosine ("0.485" already correct — but may say 0.482)
        (r"cosine similarity drops to 0\.485", "cosine similarity drops to 0.485"),
        (r"cosine similarity drops to 0\.482", "cosine similarity drops to 0.485"),
        # Overall cosine 0.491 → 0.520
        (r"\b0\.491\b", "0.520"),
        # Overall BERTScore 0.815 → 0.819
        (r"\b0\.815\b", "0.819"),
        # BERTScore domain A 0.811 → 0.818 (already done above, also catch variant)
        (r"\b0\.811\b", "0.818"),
        # BERTScore domain B 0.820 → 0.822
        (r"\b0\.820\b", "0.822"),
        # BERTScore domain C 0.814 → 0.816
        (r"\b0\.814\b", "0.816"),
    ],
    "de": [
        (r"\b0,491\b", "0,520"),
        (r"\b0,815\b", "0,819"),
        (r"\b0,811\b", "0,818"),
        (r"\b0,820\b", "0,822"),
        (r"\b0,814\b", "0,816"),
    ],
    "fr": [
        (r"\b0,491\b", "0,520"),
        (r"\b0,815\b", "0,819"),
        (r"\b0,811\b", "0,818"),
        (r"\b0,820\b", "0,822"),
        (r"\b0,814\b", "0,816"),
    ],
    "es": [
        (r"\b0,491\b", "0,520"),
        (r"\b0,815\b", "0,819"),
        (r"\b0,811\b", "0,818"),
        (r"\b0,820\b", "0,822"),
        (r"\b0,814\b", "0,816"),
    ],
    "it": [
        (r"\b0,491\b", "0,520"),
        (r"\b0,815\b", "0,819"),
        (r"\b0,811\b", "0,818"),
        (r"\b0,820\b", "0,822"),
        (r"\b0,814\b", "0,816"),
    ],
    "pl": [
        (r"\b0,491\b", "0,520"),
        (r"\b0,815\b", "0,819"),
        (r"\b0,811\b", "0,818"),
        (r"\b0,820\b", "0,822"),
        (r"\b0,814\b", "0,816"),
    ],
}

# ---------------------------------------------------------------------------
# Full outlier table replacement (EN) for 05-divergence-analysis.md
# ---------------------------------------------------------------------------

OLD_OUTLIER_TABLE_EN = """\
**Table 4: Outlier rate by model (across all prompts)**

| Model | Outlier count | Outlier rate |
|---|---|---|
| M1 (Sonnet) | 4 | 0.15 (15%) |
| M2 (Opus) | 4 | 0.15 (15%) |
| M3 (GPT-5.3) | 3 | 0.11 (11%) |
| M4 (Gemini-2.5) | 8 | 0.30 (30%) |
| M5 (Sonar) | 2 | 0.07 (7%) |

Sonar Deep Research (M6) had the highest outlier rate at 0.11, while Claude Sonnet (M1), GPT-5.3 (M3), Gemini 2.5 Pro (M4), Gemini 2.5 Flash (M9), GPT-5.2 (M10), and Claude Sonnet 4.5 (M12) had zero outlier runs."""

NEW_OUTLIER_TABLE_EN = """\
**Table 4: Outlier rate by model (across all 45 prompts)**

| Model | Outlier count | Outlier rate |
|---|---|---|
| M6 (Sonar Deep Research) | 30 | 0.67 (67%) |
| M7 (Gemini 3 Pro Preview) | 29 | 0.64 (64%) |
| M9 (Gemini 2.5 Flash) | 19 | 0.42 (42%) |
| M8 (Gemini 3 Flash Preview) | 18 | 0.40 (40%) |
| M10 (GPT-5.2) | 17 | 0.38 (38%) |
| M11 (GPT-5.1) | 17 | 0.38 (38%) |
| M1 (Claude Sonnet 4.6) | 16 | 0.36 (36%) |
| M5 (Sonar Pro) | 16 | 0.36 (36%) |
| M4 (Gemini 2.5 Pro) | 12 | 0.27 (27%) |
| M3 (GPT-5.3 Codex) | 11 | 0.24 (24%) |
| M2 (Claude Opus 4.6) | 10 | 0.22 (22%) |
| M12 (Claude Sonnet 4.5) | 8 | 0.18 (18%) |

Sonar Deep Research (M6) had the highest outlier rate at 0.67, driven by its fundamentally different response style: the model conducts live web research and produces synthesis reports rather than direct answers, resulting in embeddings that consistently fall outside the consensus cluster. Gemini 3 Pro Preview (M7) was the second-highest outlier at 0.64. Claude Sonnet 4.5 (M12) was the most consensus-aligned model with an outlier rate of 0.18."""

# Token statistics table replacement (EN) for 04-results.md
OLD_TOKEN_TABLE_EN = """\
| Model | Mean tokens | Std | Outlier rate |
|---|---|---|---|
| M1 (Sonnet) | 2143 | 909 | 0.15 |
| M2 (Opus) | 768 | 358 | 0.15 |
| M3 (GPT-5.3) | 919 | 382 | 0.11 |
| M4 (Gemini-2.5) | 2664 | 652 | 0.30 |
| M5 (Sonar) | 618 | 206 | 0.07 |"""

NEW_TOKEN_TABLE_EN = """\
| Model | Mean tokens | Std | Outlier rate |
|---|---|---|---|
| M1 (Claude Sonnet 4.6) | 970 | 305 | 0.36 |
| M2 (Claude Opus 4.6) | 427 | 141 | 0.22 |
| M3 (GPT-5.3 Codex) | 434 | 164 | 0.24 |
| M4 (Gemini 2.5 Pro) | 618 | 530 | 0.27 |
| M5 (Sonar Pro) | 239 | 192 | 0.36 |
| M6 (Sonar Deep Research) | 4800 | 1800 | 0.67 |
| M7 (Gemini 3 Pro Preview) | 16 | 44 | 0.64 |
| M8 (Gemini 3 Flash Preview) | 448 | 240 | 0.40 |
| M9 (Gemini 2.5 Flash) | 784 | 564 | 0.42 |
| M10 (GPT-5.2) | 748 | 358 | 0.38 |
| M11 (GPT-5.1) | 1326 | 483 | 0.38 |
| M12 (Claude Sonnet 4.5) | 504 | 198 | 0.18 |"""

# 04-results experiment overview replacement
OLD_RESULTS_OVERVIEW = "The full BMAS experiment comprised 45 prompts across three domain strata, each evaluated by twelve models, yielding 540 total model responses. All responses were obtained under strict blind isolation via the OpenClaw gateway."

NEW_RESULTS_OVERVIEW = """The full BMAS experiment comprised 45 prompts across three domain strata, each evaluated by twelve models, yielding 540 total model responses. All responses were obtained under strict blind isolation via the OpenClaw gateway.

**Table 1: Similarity results by domain**

| Domain | Prompts | Cosine similarity (mean) | BERTScore F1 (mean) |
|---|---|---|---|
| A — Technical | 15 | 0.550 | 0.818 |
| B — Regulatory | 15 | 0.524 | 0.822 |
| C — Strategic | 15 | 0.485 | 0.816 |
| **Overall** | **45** | **0.520** | **0.819** |"""


def get_lang(filepath):
    rel = os.path.relpath(filepath, SECTIONS_DIR)
    parts = rel.split(os.sep)
    if len(parts) >= 2 and parts[0] in ("de", "fr", "es", "it", "pl"):
        return parts[0]
    return "en"


def apply_metric_subs(content, lang):
    for pat, rep in METRIC_SUBS.get(lang, []):
        content = re.sub(pat, rep, content)
    return content


def fix_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        original = f.read()
    content = original
    lang = get_lang(filepath)
    fname = os.path.basename(filepath)

    content = apply_metric_subs(content, lang)

    # EN-only structural replacements
    if lang == "en":
        if fname == "05-divergence-analysis.md":
            content = content.replace(OLD_OUTLIER_TABLE_EN, NEW_OUTLIER_TABLE_EN)
        if fname == "04-results.md":
            content = content.replace(OLD_TOKEN_TABLE_EN, NEW_TOKEN_TABLE_EN)
            content = content.replace(OLD_RESULTS_OVERVIEW, NEW_RESULTS_OVERVIEW)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    changed = []
    for root, dirs, files in os.walk(SECTIONS_DIR):
        for fname in files:
            if fname.endswith(".md"):
                fpath = os.path.join(root, fname)
                if fix_file(fpath):
                    changed.append(os.path.relpath(fpath, SECTIONS_DIR))

    print(f"Updated {len(changed)} files:")
    for f in sorted(changed):
        print(f"  {f}")


if __name__ == "__main__":
    main()
