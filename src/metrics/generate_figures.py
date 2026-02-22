"""
BMAS Figure Generator

Produces all paper figures from results/aggregate.json and per-prompt metrics.

Figures:
    F1 - Mean pairwise cosine similarity matrix (NxN) per domain
    F2 - Box/strip plot: cosine similarity distribution by domain
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
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.gridspec import GridSpec

ROOT = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = ROOT / "paper" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Rich color palette
DOMAIN_COLORS = {
    "technical":  "#2563eb",   # vivid blue
    "regulatory": "#16a34a",   # vivid green
    "strategic":  "#dc2626",   # vivid red
}
DOMAIN_LIGHT = {
    "technical":  "#dbeafe",
    "regulatory": "#dcfce7",
    "strategic":  "#fee2e2",
}

MODEL_LABELS = {
    "M1":  "Claude Sonnet 4.6",
    "M2":  "Claude Opus 4.6",
    "M3":  "GPT-5.3 Codex",
    "M4":  "Gemini 2.5 Pro",
    "M5":  "Sonar Pro",
    "M6":  "Sonar Deep",
    "M7":  "Gemini 3 Pro",
    "M8":  "Gemini 3 Flash",
    "M9":  "Gemini 2.5 Flash",
    "M10": "GPT-5.2",
    "M11": "GPT-5.1",
    "M12": "Claude Sonnet 4.5",
}

SHORT_LABELS = {
    "M1":  "Sonnet 4.6",
    "M2":  "Opus 4.6",
    "M3":  "GPT-5.3",
    "M4":  "Gem 2.5P",
    "M5":  "Sonar Pro",
    "M6":  "Sonar Deep",
    "M7":  "Gem 3 Pro",
    "M8":  "Gem 3 Fls",
    "M9":  "Gem 2.5F",
    "M10": "GPT-5.2",
    "M11": "GPT-5.1",
    "M12": "Sonnet 4.5",
}


def _cosine_mean(cosine_dict: dict) -> float | None:
    """Robust getter for cosine mean - handles both old and new key formats."""
    if not cosine_dict or "error" in cosine_dict:
        return None
    return cosine_dict.get("mean", cosine_dict.get("mean_similarity"))


def _outlier_list(entry: dict) -> list[str]:
    """Robust getter for outlier model list."""
    out = entry.get("outliers", {})
    if isinstance(out, dict):
        return out.get("outliers", out.get("outlier_models", []))
    return []


def _get_models_from_reports(reports: list[dict]) -> list[str]:
    seen: set[str] = set()
    for r in reports:
        seen.update(r.get("model_ids", []))
    return sorted(seen, key=lambda m: int(m[1:]))


def load_aggregate() -> list[dict]:
    f = RESULTS_DIR / "aggregate.json"
    if not f.exists():
        raise FileNotFoundError(f"Run metric pipeline first: {f}")
    return json.loads(f.read_text())


# ---------------------------------------------------------------------------
# F1: Similarity matrix heatmap per domain (3 panels, fully annotated)
# ---------------------------------------------------------------------------

def figure_similarity_heatmaps(reports: list[dict]) -> None:
    domains = ["technical", "regulatory", "strategic"]
    models = _get_models_from_reports(reports)
    n_models = len(models)
    short = [SHORT_LABELS.get(m, m) for m in models]

    fig, axes = plt.subplots(1, 3, figsize=(22, 7))
    fig.suptitle(
        "BMAS Figure 1: Mean Pairwise Cosine Similarity Matrix by Domain\n"
        f"({n_models} models, embedding: all-MiniLM-L6-v2)",
        fontsize=14, fontweight="bold", y=1.01
    )

    global_vmin, global_vmax = 0.3, 1.0
    cmap = plt.cm.RdYlGn   # red (low) -> yellow -> green (high)

    for ax, domain in zip(axes, domains):
        domain_reports = [
            r for r in reports
            if r["domain"] == domain
            and "cosine" in r
            and "error" not in r.get("cosine", {})
            and "matrix" in r.get("cosine", {})
        ]

        color = DOMAIN_COLORS[domain]
        n = len(domain_reports)

        if not domain_reports:
            ax.set_title(f"{domain.capitalize()}\n(no matrix data)", color=color)
            ax.axis("off")
            continue

        # Build per-prompt model-ordered matrices and average
        matrices = []
        for r in domain_reports:
            cosine = r["cosine"]
            mat_raw = np.array(cosine["matrix"])
            mid_order = cosine.get("model_ids", models)
            if mat_raw.shape[0] != n_models:
                # Reorder/expand to full model list
                full_mat = np.zeros((n_models, n_models))
                for i, mi in enumerate(models):
                    for j, mj in enumerate(models):
                        if mi in mid_order and mj in mid_order:
                            ii = mid_order.index(mi)
                            jj = mid_order.index(mj)
                            full_mat[i, j] = mat_raw[ii, jj]
                        elif mi == mj:
                            full_mat[i, j] = 1.0
                matrices.append(full_mat)
            else:
                # Reorder if needed
                if mid_order != models:
                    perm = [mid_order.index(m) if m in mid_order else -1 for m in models]
                    reordered = np.zeros((n_models, n_models))
                    for i, pi in enumerate(perm):
                        for j, pj in enumerate(perm):
                            if pi >= 0 and pj >= 0:
                                reordered[i, j] = mat_raw[pi, pj]
                            elif i == j:
                                reordered[i, j] = 1.0
                    matrices.append(reordered)
                else:
                    matrices.append(mat_raw)

        avg_matrix = np.mean(matrices, axis=0)
        triu_vals = [avg_matrix[i][j] for i in range(n_models) for j in range(i + 1, n_models)]
        mean_val = float(np.mean(triu_vals)) if triu_vals else 0.0
        std_val = float(np.std(triu_vals)) if triu_vals else 0.0

        im = ax.imshow(avg_matrix, vmin=global_vmin, vmax=global_vmax, cmap=cmap, aspect="equal")

        ax.set_xticks(range(n_models))
        ax.set_yticks(range(n_models))
        fs = max(6, 9 - n_models // 3)
        ax.set_xticklabels(short, rotation=45, ha="right", fontsize=fs)
        ax.set_yticklabels(short, fontsize=fs)

        # Cell annotations
        cell_fs = max(5, 7 - n_models // 4)
        for i in range(n_models):
            for j in range(n_models):
                val = avg_matrix[i, j]
                norm_val = (val - global_vmin) / (global_vmax - global_vmin)
                text_color = "white" if norm_val > 0.75 or norm_val < 0.25 else "black"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                        fontsize=cell_fs, color=text_color, fontweight="normal")

        # Colored title
        ax.set_title(
            f"{domain.capitalize()}\nn={n} prompts   mean={mean_val:.3f} ± {std_val:.3f}",
            fontsize=11, color=color, fontweight="bold", pad=10
        )

        # Colored border
        for spine in ax.spines.values():
            spine.set_edgecolor(color)
            spine.set_linewidth(2.5)

        cbar = plt.colorbar(im, ax=ax, shrink=0.75, pad=0.02)
        cbar.set_label("Cosine Similarity", fontsize=9)
        cbar.ax.tick_params(labelsize=8)

    plt.tight_layout()
    out = FIGURES_DIR / "F1-similarity-heatmaps.png"
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  F1 saved: {out}")


# ---------------------------------------------------------------------------
# F2: Box + strip plot: cosine similarity distribution by domain
# ---------------------------------------------------------------------------

def figure_cosine_boxplot(reports: list[dict]) -> None:
    domains = ["technical", "regulatory", "strategic"]
    # Collect all pairwise cosine values per domain (not just per-prompt means)
    pairs_by_domain = {d: [] for d in domains}
    means_by_domain = {d: [] for d in domains}

    for r in reports:
        cosine = r.get("cosine", {})
        domain = r.get("domain", "")
        if domain not in domains or "error" in cosine:
            continue

        mean_val = _cosine_mean(cosine)
        if mean_val is not None:
            means_by_domain[domain].append(mean_val)

        # Collect all pairwise values
        pairs = cosine.get("pairs", [])
        for p in pairs:
            sim = p.get("cosine")
            if sim is not None:
                pairs_by_domain[domain].append(sim)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("BMAS Figure 2: Response Convergence by Domain (Cosine Similarity)",
                 fontsize=13, fontweight="bold")

    # --- Left panel: per-prompt means (boxplot) ---
    ax = axes[0]
    data = [means_by_domain[d] for d in domains]
    labels = [f"{d.capitalize()}\n(n={len(means_by_domain[d])} prompts)" for d in domains]

    bp = ax.boxplot(data, labels=labels, patch_artist=True, notch=False,
                    widths=0.5, showfliers=True)
    for patch, domain in zip(bp["boxes"], domains):
        patch.set_facecolor(DOMAIN_COLORS[domain])
        patch.set_alpha(0.75)
    for med in bp["medians"]:
        med.set_color("white")
        med.set_linewidth(2.5)
    for flier, domain in zip(bp["fliers"], domains):
        flier.set_markerfacecolor(DOMAIN_COLORS[domain])
        flier.set_markersize(5)

    # Overlay individual data points
    rng = np.random.default_rng(42)
    for i, (domain, vals) in enumerate(zip(domains, data)):
        jitter = rng.uniform(-0.12, 0.12, len(vals))
        ax.scatter(np.array([i + 1] * len(vals)) + jitter, vals,
                   color=DOMAIN_COLORS[domain], alpha=0.5, s=25, zorder=3, edgecolors="white", linewidths=0.3)

    ax.set_ylabel("Mean Pairwise Cosine Similarity (per prompt)", fontsize=10)
    ax.set_title("Per-Prompt Means", fontsize=11)
    ax.set_ylim(0.2, 0.85)
    ax.axhline(0.5, color="gray", linestyle="--", alpha=0.5, label="Baseline (0.5)")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3)

    # Domain mean annotations
    for i, (domain, vals) in enumerate(zip(domains, data)):
        if vals:
            ax.text(i + 1, max(vals) + 0.02, f"x={np.mean(vals):.3f}",
                    ha="center", fontsize=9, color=DOMAIN_COLORS[domain], fontweight="bold")

    # --- Right panel: all pairwise values (violin) ---
    ax2 = axes[1]
    pair_data = [pairs_by_domain[d] for d in domains]
    pair_labels = [f"{d.capitalize()}\n({len(pairs_by_domain[d])} pairs)" for d in domains]

    vp = ax2.violinplot(pair_data, positions=range(1, 4), showmeans=True, showmedians=True, widths=0.6)
    for i, (body, domain) in enumerate(zip(vp["bodies"], domains)):
        body.set_facecolor(DOMAIN_COLORS[domain])
        body.set_alpha(0.7)
        body.set_edgecolor(DOMAIN_COLORS[domain])
    vp["cmeans"].set_colors([DOMAIN_COLORS[d] for d in domains])
    vp["cmeans"].set_linewidth(2)
    vp["cmedians"].set_colors(["white", "white", "white"])
    vp["cbars"].set_linewidth(0)
    vp["cmins"].set_linewidth(0)
    vp["cmaxes"].set_linewidth(0)

    ax2.set_xticks(range(1, 4))
    ax2.set_xticklabels(pair_labels, fontsize=9)
    ax2.set_ylabel("Pairwise Cosine Similarity", fontsize=10)
    ax2.set_title("All Pairwise Values (Violin)", fontsize=11)
    ax2.set_ylim(0.0, 1.05)
    ax2.axhline(0.5, color="gray", linestyle="--", alpha=0.5)
    ax2.grid(axis="y", alpha=0.3)

    # H1 annotation
    for i, (domain, vals) in enumerate(zip(domains, pair_data)):
        if vals:
            ax2.text(i + 1, 1.01, f"x={np.mean(vals):.3f}",
                     ha="center", fontsize=9, color=DOMAIN_COLORS[domain], fontweight="bold")

    plt.tight_layout()
    out = FIGURES_DIR / "F2-cosine-boxplot.png"
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  F2 saved: {out}")


# ---------------------------------------------------------------------------
# F3: BERTScore F1 per prompt (sorted, domain-colored, with domain averages)
# ---------------------------------------------------------------------------

def figure_bertscore_bars(reports: list[dict]) -> None:
    # Sort A01-A15, B01-B15, C01-C15
    sorted_reports = sorted(reports, key=lambda r: r["prompt_id"])
    prompt_ids = [r["prompt_id"] for r in sorted_reports]
    domains = [r["domain"] for r in sorted_reports]
    scores = [r.get("bertscore", {}).get("mean_f1", 0) for r in sorted_reports]
    min_scores = [r.get("bertscore", {}).get("min_f1", 0) for r in sorted_reports]
    colors = [DOMAIN_COLORS[d] for d in domains]

    fig, ax = plt.subplots(figsize=(16, 6))
    x = range(len(prompt_ids))
    bars = ax.bar(x, scores, color=colors, alpha=0.85, edgecolor="white", linewidth=0.5, zorder=3)

    # Error bars: mean - min (lower bound)
    yerr_low = [s - m for s, m in zip(scores, min_scores)]
    ax.errorbar(x, scores, yerr=[yerr_low, [0]*len(scores)],
                fmt="none", color="#374151", linewidth=0.8, capsize=2, zorder=4)

    # Domain average lines
    for domain in ["technical", "regulatory", "strategic"]:
        domain_scores = [s for s, d in zip(scores, domains) if d == domain]
        domain_x = [i for i, d in enumerate(domains) if d == domain]
        if domain_scores:
            avg = np.mean(domain_scores)
            ax.hlines(avg, min(domain_x) - 0.4, max(domain_x) + 0.4,
                      colors=DOMAIN_COLORS[domain], linestyles="--", linewidth=2, alpha=0.8, zorder=5)
            ax.text(max(domain_x) + 0.5, avg, f"  {avg:.3f}", fontsize=8,
                    color=DOMAIN_COLORS[domain], va="center", fontweight="bold")

    ax.set_xticks(list(x))
    ax.set_xticklabels(prompt_ids, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Mean BERTScore F1", fontsize=11)
    ax.set_title(
        "BMAS Figure 3: Semantic Similarity per Prompt (BERTScore F1, roberta-large)\n"
        "Dashed lines = domain averages  |  Error bars = min F1 range",
        fontsize=12, fontweight="bold"
    )
    ax.set_ylim(0.65, 0.95)
    ax.grid(axis="y", alpha=0.3, zorder=0)

    # Domain separators + background shading
    prev_domain = None
    for i, d in enumerate(domains):
        if prev_domain and d != prev_domain:
            ax.axvline(i - 0.5, color="#9ca3af", linestyle="-", alpha=0.4, linewidth=1)
        prev_domain = d

    # Background shading per domain block
    starts = {}
    ends = {}
    for i, d in enumerate(domains):
        if d not in starts:
            starts[d] = i
        ends[d] = i
    for domain in ["technical", "regulatory", "strategic"]:
        if domain in starts:
            ax.axvspan(starts[domain] - 0.5, ends[domain] + 0.5,
                       alpha=0.06, color=DOMAIN_COLORS[domain], zorder=0)

    patches = [mpatches.Patch(color=DOMAIN_COLORS[d], alpha=0.85, label=d.capitalize())
               for d in ["technical", "regulatory", "strategic"]]
    ax.legend(handles=patches, fontsize=10, loc="lower right")

    plt.tight_layout()
    out = FIGURES_DIR / "F3-bertscore-bars.png"
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  F3 saved: {out}")


# ---------------------------------------------------------------------------
# F4: Token ratio vs cosine divergence (colored scatter)
# ---------------------------------------------------------------------------

def figure_token_vs_divergence(reports: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))

    for r in reports:
        tokens = r.get("response_tokens", {})
        cosine = r.get("cosine", {})
        if "error" in cosine:
            continue

        mean_val = _cosine_mean(cosine)
        if mean_val is None:
            continue

        token_vals = [v for v in tokens.values() if isinstance(v, (int, float)) and v > 0]
        if len(token_vals) < 2:
            continue

        ratio = max(token_vals) / min(token_vals)
        divergence = 1.0 - mean_val
        domain = r["domain"]
        color = DOMAIN_COLORS.get(domain, "gray")

        ax.scatter(ratio, divergence, color=color, alpha=0.8, s=80,
                   edgecolors="white", linewidths=0.8, zorder=3)
        ax.annotate(r["prompt_id"], (ratio, divergence),
                    textcoords="offset points", xytext=(5, 3),
                    fontsize=7.5, alpha=0.85,
                    color=DOMAIN_COLORS.get(domain, "gray"))

    # Trend line per domain
    for domain in ["technical", "regulatory", "strategic"]:
        xs, ys = [], []
        for r in reports:
            tokens = r.get("response_tokens", {})
            cosine = r.get("cosine", {})
            if r["domain"] != domain or "error" in cosine:
                continue
            mean_val = _cosine_mean(cosine)
            if mean_val is None:
                continue
            token_vals = [v for v in tokens.values() if isinstance(v, (int, float)) and v > 0]
            if len(token_vals) < 2:
                continue
            xs.append(max(token_vals) / min(token_vals))
            ys.append(1.0 - mean_val)

        if len(xs) >= 3:
            # Fit on log(x) for log-scale axis
            log_xs = np.log(xs)
            z = np.polyfit(log_xs, ys, 1)
            p = np.poly1d(z)
            x_line = np.logspace(np.log10(max(0.5, min(xs))), np.log10(max(xs)), 100)
            ax.plot(x_line, p(np.log(x_line)), color=DOMAIN_COLORS[domain],
                    alpha=0.7, linewidth=2.5, linestyle="--", zorder=2)

    ax.set_xscale("log")
    ax.set_xlabel("Token Count Ratio (max / min across models, log scale)", fontsize=11)
    ax.set_ylabel("Semantic Divergence (1 - cosine similarity)", fontsize=11)
    ax.set_title(
        "BMAS Figure 4: Token Length Variance vs. Semantic Divergence\n"
        "Dashed lines = domain trend (log-scale X axis)",
        fontsize=12, fontweight="bold"
    )
    patches = [mpatches.Patch(color=DOMAIN_COLORS[d], alpha=0.85, label=d.capitalize())
               for d in ["technical", "regulatory", "strategic"]]
    ax.legend(handles=patches, fontsize=10)
    ax.grid(alpha=0.3, zorder=0, which="both")
    plt.tight_layout()
    out = FIGURES_DIR / "F4-token-divergence-scatter.png"
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  F4 saved: {out}")


# ---------------------------------------------------------------------------
# F5: Outlier frequency by model (domain-stacked bars)
# ---------------------------------------------------------------------------

def figure_outlier_frequency(reports: list[dict]) -> None:
    models = _get_models_from_reports(reports)
    domains = ["technical", "regulatory", "strategic"]

    # Count outlier appearances per model per domain
    counts: dict[str, dict[str, int]] = {m: {d: 0 for d in domains} for m in models}
    total_by_domain: dict[str, int] = {d: 0 for d in domains}

    for r in reports:
        domain = r.get("domain", "")
        if domain not in domains:
            continue
        outlier_list = _outlier_list(r)
        # Only count prompts that have outlier data
        out = r.get("outliers", {})
        if not isinstance(out, dict) or "outliers" not in out:
            continue
        total_by_domain[domain] += 1
        for m in outlier_list:
            if m in counts:
                counts[m][domain] += 1

    total_prompts = sum(total_by_domain.values())
    if total_prompts == 0:
        print("  F5: no outlier data available")
        return

    model_names = [SHORT_LABELS.get(m, m) for m in models]
    total_counts = [sum(counts[m].values()) for m in models]
    total_pcts = [c / total_prompts * 100 for c in total_counts]

    # Sort both panels by total outlier % descending
    sorted_idx = np.argsort(total_pcts)[::-1]
    sorted_models = [models[i] for i in sorted_idx]
    sorted_names = [model_names[i] for i in sorted_idx]
    sorted_pcts = [total_pcts[i] for i in sorted_idx]

    fig, axes = plt.subplots(2, 1, figsize=(14, 10),
                              gridspec_kw={"height_ratios": [2, 1]})
    fig.suptitle(
        f"BMAS Figure 5: Outlier Detection Rate by Model (DBSCAN eps=0.15, n={total_prompts} prompts)",
        fontsize=13, fontweight="bold"
    )

    # --- Top: stacked bar by domain (sorted by total) ---
    ax = axes[0]
    x = np.arange(len(sorted_models))
    bottom = np.zeros(len(sorted_models))

    for domain in domains:
        domain_counts = np.array([counts[m][domain] for m in sorted_models])
        domain_pcts = domain_counts / total_prompts * 100
        ax.bar(x, domain_pcts, bottom=bottom,
               color=DOMAIN_COLORS[domain], alpha=0.85,
               label=f"{domain.capitalize()} (n={total_by_domain[domain]})",
               edgecolor="white", linewidth=0.5)
        bottom += domain_pcts

    for i, pct in enumerate(sorted_pcts):
        if pct > 3:
            ax.text(i, pct + 0.5, f"{pct:.0f}%", ha="center", va="bottom",
                    fontsize=9, fontweight="bold", color="#374151")

    ax.set_xticks(x)
    ax.set_xticklabels(sorted_names, rotation=30, ha="right", fontsize=10)
    ax.set_ylabel("Outlier Rate (%)", fontsize=11)
    ax.set_title("Stacked by Domain — sorted by total frequency", fontsize=11)
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(axis="y", alpha=0.3)

    # --- Bottom: rank bar (same order, plasma gradient) ---
    ax2 = axes[1]
    max_pct = max(sorted_pcts) if sorted_pcts else 1

    bars2 = ax2.bar(range(len(sorted_models)), sorted_pcts,
                    color=[plt.cm.plasma(p / (max_pct or 1)) for p in sorted_pcts],
                    alpha=0.85, edgecolor="white", linewidth=0.5)
    ax2.set_xticks(range(len(sorted_models)))
    ax2.set_xticklabels(sorted_names, rotation=30, ha="right", fontsize=10)
    ax2.set_ylabel("Total Outlier Rate (%)", fontsize=10)
    ax2.set_title("Total Outlier Rate (same order)", fontsize=11)
    ax2.grid(axis="y", alpha=0.3)

    sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(0, max_pct))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax2, orientation="vertical", shrink=0.8, pad=0.02)
    cbar.set_label("Outlier %", fontsize=8)

    plt.tight_layout()
    out = FIGURES_DIR / "F5-outlier-frequency.png"
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  F5 saved: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("[Figures] Loading aggregate results...")
    reports = load_aggregate()
    print(f"[Figures] {len(reports)} prompts loaded")

    # Quick data check
    n_with_cosine = sum(1 for r in reports if "error" not in r.get("cosine", {}) and _cosine_mean(r.get("cosine", {})) is not None)
    n_with_matrix = sum(1 for r in reports if "matrix" in r.get("cosine", {}) and "error" not in r.get("cosine", {}))
    n_with_outliers = sum(1 for r in reports if _outlier_list(r))
    print(f"  cosine available:  {n_with_cosine}/45")
    print(f"  matrix available:  {n_with_matrix}/45")
    print(f"  outlier data:      {n_with_outliers}/45")
    print()

    print("[F1] Similarity heatmaps by domain...")
    figure_similarity_heatmaps(reports)

    print("[F2] Cosine distribution (box + violin)...")
    figure_cosine_boxplot(reports)

    print("[F3] BERTScore bars per prompt...")
    figure_bertscore_bars(reports)

    print("[F4] Token ratio vs divergence scatter...")
    figure_token_vs_divergence(reports)

    print("[F5] Outlier frequency by model...")
    figure_outlier_frequency(reports)

    print(f"\n[Figures] All figures saved to: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
