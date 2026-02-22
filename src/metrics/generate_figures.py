"""
BMAS Figure Generator

Produces all paper figures from results/aggregate.json and per-prompt metrics.

Figures:
    F1 - Similarity heatmap (mean cosine similarity NxN by domain)
    F2 - Box plot: cosine similarity distribution by domain
    F3 - Bar chart: mean BERTScore F1 per prompt, grouped by domain
    F4 - Scatter: cosine divergence vs token count ratio
    F5 - Outlier frequency by model

Usage:
    python generate_figures.py
"""

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = ROOT / "paper" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

DOMAIN_COLORS = {
    "technical":  "#2563eb",  # blue
    "regulatory": "#16a34a",  # green
    "strategic":  "#dc2626",  # red
}

MODEL_LABELS = {
    "M1":  "Sonnet 4.6",
    "M2":  "Opus 4.6",
    "M3":  "GPT-5.3",
    "M4":  "Gemini 2.5 Pro",
    "M5":  "Sonar Pro",
    "M6":  "Sonar Deep",
    "M7":  "Gemini 3 Pro",
    "M8":  "Gemini 3 Flash",
    "M9":  "Gemini 2.5 Flash",
    "M10": "GPT-5.2",
    "M11": "GPT-5.1",
    "M12": "Sonnet 4.5",
}

ALL_KNOWN_MODELS = list(MODEL_LABELS.keys())


def _get_models_from_reports(reports: list[dict]) -> list[str]:
    """Dynamically detect which models appear in the data."""
    seen: set[str] = set()
    for r in reports:
        seen.update(r.get("model_ids", []))
    return sorted(seen, key=lambda m: int(m[1:]))


def load_aggregate() -> list[dict]:
    f = RESULTS_DIR / "aggregate.json"
    if not f.exists():
        raise FileNotFoundError(f"Run metric pipeline first: {f}")
    return json.loads(f.read_text())


def load_prompt_metrics(prompt_id: str) -> dict:
    f = RESULTS_DIR / f"{prompt_id}-metrics.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text())


# ---------------------------------------------------------------------------
# F1: Similarity matrix heatmap per domain
# ---------------------------------------------------------------------------

def figure_similarity_heatmaps(reports: list[dict]) -> None:
    domains = ["technical", "regulatory", "strategic"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("BMAS: Mean Pairwise Cosine Similarity by Domain", fontsize=14, y=1.02)

    models = _get_models_from_reports(reports)
    labels = [MODEL_LABELS.get(m, m) for m in models]
    n_models = len(models)

    for ax, domain in zip(axes, domains):
        domain_reports = [r for r in reports if r["domain"] == domain
                          and "cosine" in r and "matrix" not in ["error"]]
        if not domain_reports:
            ax.set_title(f"{domain.capitalize()}\n(no data)")
            continue

        # Average matrices across all prompts in domain (only use reports with full matrix)
        matrices = []
        for r in domain_reports:
            cosine = r.get("cosine", {})
            if "matrix" in cosine and isinstance(cosine["matrix"], list):
                mat = np.array(cosine["matrix"])
                if mat.shape == (n_models, n_models):
                    matrices.append(mat)

        if not matrices:
            ax.set_title(f"{domain.capitalize()}\n(no matrix data)")
            continue

        avg_matrix = np.mean(matrices, axis=0)
        triu_vals = [avg_matrix[i][j] for i in range(n_models) for j in range(i + 1, n_models)]
        mean_val = float(np.mean(triu_vals)) if triu_vals else 0.0

        im = ax.imshow(avg_matrix, vmin=0.5, vmax=1.0, cmap="Blues")
        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        fontsize = max(6, 9 - n_models // 4)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=fontsize)
        ax.set_yticklabels(labels, fontsize=fontsize)

        # Annotate cells
        for i in range(n_models):
            for j in range(n_models):
                val = avg_matrix[i, j]
                color = "white" if val > 0.85 else "black"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                        fontsize=max(5, 8 - n_models // 4), color=color)

        n = len(domain_reports)
        ax.set_title(f"{domain.capitalize()}\n(n={n} prompts, mean={mean_val:.3f})", fontsize=11)
        plt.colorbar(im, ax=ax, shrink=0.8)

    plt.tight_layout()
    out = FIGURES_DIR / "F1-similarity-heatmaps.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  F1 saved: {out}")


# ---------------------------------------------------------------------------
# F2: Box plots - cosine similarity by domain
# ---------------------------------------------------------------------------

def figure_cosine_boxplot(reports: list[dict]) -> None:
    domains = ["technical", "regulatory", "strategic"]
    data_by_domain = {d: [] for d in domains}

    for r in reports:
        cosine = r.get("cosine", {})
        if "mean_similarity" not in cosine:
            continue
        domain = r["domain"]
        if domain in data_by_domain:
            data_by_domain[domain].append(cosine["mean_similarity"])

    fig, ax = plt.subplots(figsize=(8, 5))
    bp_data = [data_by_domain[d] for d in domains]
    bp = ax.boxplot(bp_data, tick_labels=[d.capitalize() for d in domains],
                    patch_artist=True, notch=False)

    for patch, domain in zip(bp["boxes"], domains):
        patch.set_facecolor(DOMAIN_COLORS[domain])
        patch.set_alpha(0.7)

    ax.set_ylabel("Mean Pairwise Cosine Similarity", fontsize=11)
    ax.set_xlabel("Domain", fontsize=11)
    n_models = len(_get_models_from_reports(reports))
    ax.set_title(f"BMAS: Response Convergence by Domain\n(cosine similarity, {n_models} models)", fontsize=12)
    ax.set_ylim(0.4, 1.05)
    ax.axhline(0.75, color="gray", linestyle="--", alpha=0.5, label="H1 threshold (0.75)")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)

    # Add sample size annotations
    for i, (domain, vals) in enumerate(zip(domains, bp_data)):
        ax.text(i + 1, 0.42, f"n={len(vals)}", ha="center", va="bottom", fontsize=9, color="gray")

    plt.tight_layout()
    out = FIGURES_DIR / "F2-cosine-boxplot.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  F2 saved: {out}")


# ---------------------------------------------------------------------------
# F3: BERTScore F1 per prompt
# ---------------------------------------------------------------------------

def figure_bertscore_bars(reports: list[dict]) -> None:
    sorted_reports = sorted(reports, key=lambda r: (r["domain"], r["prompt_id"]))
    prompt_ids = [r["prompt_id"] for r in sorted_reports]
    domains = [r["domain"] for r in sorted_reports]
    scores = [r.get("bertscore", {}).get("mean_f1", 0) for r in sorted_reports]
    colors = [DOMAIN_COLORS[d] for d in domains]

    fig, ax = plt.subplots(figsize=(14, 5))
    bars = ax.bar(range(len(prompt_ids)), scores, color=colors, alpha=0.8, edgecolor="white")

    ax.set_xticks(range(len(prompt_ids)))
    ax.set_xticklabels(prompt_ids, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Mean BERTScore F1", fontsize=11)
    ax.set_title("BMAS: Semantic Similarity per Prompt (BERTScore F1)\nGrouped by Domain", fontsize=12)
    ax.set_ylim(0.5, 1.0)
    ax.grid(axis="y", alpha=0.3)

    # Domain legend
    patches = [mpatches.Patch(color=DOMAIN_COLORS[d], alpha=0.8, label=d.capitalize())
               for d in ["technical", "regulatory", "strategic"]]
    ax.legend(handles=patches, fontsize=10)

    # Domain separators
    for i, (p, d) in enumerate(zip(prompt_ids, domains)):
        if i > 0 and domains[i] != domains[i-1]:
            ax.axvline(i - 0.5, color="gray", linestyle="--", alpha=0.4)

    plt.tight_layout()
    out = FIGURES_DIR / "F3-bertscore-bars.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  F3 saved: {out}")


# ---------------------------------------------------------------------------
# F4: Token ratio vs cosine divergence
# ---------------------------------------------------------------------------

def figure_token_vs_divergence(reports: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    for r in reports:
        tokens = r.get("response_tokens", {})
        cosine = r.get("cosine", {})
        if not tokens or "mean_similarity" not in cosine:
            continue

        token_vals = [v for v in tokens.values() if v > 0]
        if not token_vals or min(token_vals) == 0:
            continue

        ratio = max(token_vals) / min(token_vals)
        divergence = 1 - cosine["mean_similarity"]
        domain = r["domain"]
        color = DOMAIN_COLORS.get(domain, "gray")

        ax.scatter(ratio, divergence, color=color, alpha=0.75, s=60, edgecolors="white", linewidths=0.5)
        ax.annotate(r["prompt_id"], (ratio, divergence),
                    textcoords="offset points", xytext=(4, 2), fontsize=7, alpha=0.7)

    ax.set_xlabel("Token Count Ratio (max/min across models)", fontsize=11)
    ax.set_ylabel("Semantic Divergence (1 - mean cosine similarity)", fontsize=11)
    ax.set_title("BMAS: Token Ratio vs. Semantic Divergence\nby Prompt and Domain", fontsize=12)

    patches = [mpatches.Patch(color=DOMAIN_COLORS[d], alpha=0.8, label=d.capitalize())
               for d in ["technical", "regulatory", "strategic"]]
    ax.legend(handles=patches, fontsize=10)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out = FIGURES_DIR / "F4-token-divergence-scatter.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  F4 saved: {out}")


# ---------------------------------------------------------------------------
# F5: Outlier frequency by model
# ---------------------------------------------------------------------------

def figure_outlier_frequency(reports: list[dict]) -> None:
    models = _get_models_from_reports(reports)
    outlier_counts = {m: 0 for m in models}
    total_prompts = 0

    for r in reports:
        out = r.get("outliers", {})
        if "outlier_models" not in out:
            continue
        total_prompts += 1
        for m in out["outlier_models"]:
            if m in outlier_counts:
                outlier_counts[m] += 1

    if total_prompts == 0:
        print("  F5: no outlier data")
        return

    fig_width = max(8, len(models) * 0.9)
    fig, ax = plt.subplots(figsize=(fig_width, 4))
    model_names = [MODEL_LABELS.get(m, m) for m in models]
    counts = [outlier_counts[m] for m in models]
    pcts = [c / total_prompts * 100 for c in counts]
    max_pct = max(pcts) if pcts else 1

    bars = ax.bar(model_names, pcts, color="#7c3aed", alpha=0.75, edgecolor="white")
    ax.set_ylabel("Outlier Rate (%)", fontsize=11)
    ax.set_xlabel("Model", fontsize=11)
    ax.set_title(f"BMAS: Outlier Detection Rate by Model\n(n={total_prompts} prompts, DBSCAN eps=0.15)", fontsize=12)
    ax.set_ylim(0, max_pct * 1.3 + 5)
    ax.tick_params(axis="x", rotation=30)

    for bar, pct, cnt in zip(bars, pcts, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{pct:.0f}%\n({cnt})", ha="center", va="bottom", fontsize=9)

    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    out = FIGURES_DIR / "F5-outlier-frequency.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  F5 saved: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("[Figures] Loading aggregate results...")
    reports = load_aggregate()
    print(f"[Figures] {len(reports)} prompts loaded")
    print()

    print("[Figures] F1: Similarity heatmaps by domain...")
    figure_similarity_heatmaps(reports)

    print("[Figures] F2: Cosine similarity box plots...")
    figure_cosine_boxplot(reports)

    print("[Figures] F3: BERTScore bars per prompt...")
    figure_bertscore_bars(reports)

    print("[Figures] F4: Token ratio vs divergence scatter...")
    figure_token_vs_divergence(reports)

    print("[Figures] F5: Outlier frequency by model...")
    figure_outlier_frequency(reports)

    print(f"\n[Figures] All figures saved to: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
