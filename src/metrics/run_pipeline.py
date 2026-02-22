"""
BMAS Metrics Pipeline Runner

Runs all metrics on all completed experiment outputs and saves
structured results to results/ folder.

Usage:
    python run_pipeline.py                     # all prompts with all 5 models done
    python run_pipeline.py --min-models 3      # accept prompts with >= 3 models
    python run_pipeline.py --prompt-ids A01 B05  # specific prompts only
"""

import argparse
import json
import csv
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from metrics.deviation import (
    compute_cosine_matrix,
    compute_bertscore,
    compute_jaccard,
    detect_outliers,
    load_responses_for_prompt,
)

RAW_OUTPUTS = ROOT / "experiments" / "raw-outputs"
RESULTS_DIR = ROOT / "results"

DOMAIN_MAP = {
    # Technical (A01-A15)
    "A01": "technical", "A02": "technical", "A03": "technical", "A04": "technical",
    "A05": "technical", "A06": "technical", "A07": "technical", "A08": "technical",
    "A09": "technical", "A10": "technical",
    "A11": "technical", "A12": "technical", "A13": "technical", "A14": "technical",
    "A15": "technical",
    # Regulatory (B01-B15)
    "B01": "regulatory", "B02": "regulatory", "B03": "regulatory", "B04": "regulatory",
    "B05": "regulatory", "B06": "regulatory", "B07": "regulatory", "B08": "regulatory",
    "B09": "regulatory", "B10": "regulatory",
    "B11": "regulatory", "B12": "regulatory", "B13": "regulatory", "B14": "regulatory",
    "B15": "regulatory",
    # Strategic (C01-C15)
    "C01": "strategic", "C02": "strategic", "C03": "strategic", "C04": "strategic",
    "C05": "strategic", "C06": "strategic", "C07": "strategic", "C08": "strategic",
    "C09": "strategic", "C10": "strategic",
    "C11": "strategic", "C12": "strategic", "C13": "strategic", "C14": "strategic",
    "C15": "strategic",
}


def run_metrics_for_prompt(prompt_id: str, responses: dict[str, str]) -> dict:
    """Run all metrics for one prompt. Returns metric report."""
    report = {
        "prompt_id": prompt_id,
        "domain": DOMAIN_MAP.get(prompt_id, "unknown"),
        "model_ids": sorted(responses.keys()),
        "n_models": len(responses),
    }

    # Token counts (from raw output files)
    raw_dir = RAW_OUTPUTS / prompt_id
    token_counts = {}
    for mid in responses:
        f = raw_dir / f"{mid}.json"
        if f.exists():
            d = json.loads(f.read_text())
            token_counts[mid] = d.get("response_tokens", 0)
    report["response_tokens"] = token_counts

    # 1. Cosine similarity
    print(f"  cosine...", end="", flush=True)
    try:
        cosine = compute_cosine_matrix(responses)
        report["cosine"] = {
            "mean": cosine["mean"],
            "min": cosine["min"],
            "max": cosine["max"],
            "std": cosine["std"],
            "matrix": cosine["matrix"],
            "model_ids": cosine["model_ids"],
            "embeddings": cosine["embeddings"],
            "pair_count": cosine["pair_count"],
            "pairs": cosine.get("pairs", []),
        }
        print(f" {cosine['mean']:.3f}", end="", flush=True)
    except Exception as e:
        report["cosine"] = {"error": str(e)}
        cosine = None
        print(f" ERROR: {e}", end="", flush=True)

    # 2. BERTScore
    print(f" | bertscore...", end="", flush=True)
    try:
        bs = compute_bertscore(responses)
        report["bertscore"] = {
            "mean_f1": bs["mean_f1"],
            "min_f1": bs["min_f1"],
            "max_f1": bs["max_f1"],
            "std_f1": bs["std_f1"],
            "pairs": bs["pairs"],
        }
        print(f" {bs['mean_f1']:.3f}", end="", flush=True)
    except Exception as e:
        report["bertscore"] = {"error": str(e)}
        print(f" ERROR: {e}", end="", flush=True)

    # 3. Jaccard
    print(f" | jaccard...", end="", flush=True)
    try:
        jac = compute_jaccard(responses)
        report["jaccard"] = {
            "mean_jaccard": jac["mean_jaccard"],
            "min_jaccard": jac["min_jaccard"],
            "max_jaccard": jac["max_jaccard"],
            "pairs": jac["pairs"],
        }
        print(f" {jac['mean_jaccard']:.3f}", end="", flush=True)
    except Exception as e:
        report["jaccard"] = {"error": str(e)}
        print(f" ERROR: {e}", end="", flush=True)

    # 4. Outliers
    if cosine and "error" not in cosine:
        print(f" | outliers...", end="", flush=True)
        try:
            out = detect_outliers(cosine)
            report["outliers"] = {
                "outlier_models": out["outliers"],
                "n_outliers": len(out["outliers"]),
                "labels": out["labels"],
                "model_ids": out["model_ids"],
            }
            print(f" {out['outliers'] or 'none'}", end="", flush=True)
        except Exception as e:
            report["outliers"] = {"error": str(e)}
            print(f" ERROR: {e}", end="", flush=True)

    print()
    return report


def run_all(prompt_ids: list[str] | None = None, min_models: int = 5) -> list[dict]:
    """Run metrics pipeline on all completed prompts."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Discover available prompts
    available = sorted(p.name for p in RAW_OUTPUTS.iterdir() if p.is_dir())
    if prompt_ids:
        available = [p for p in available if p in prompt_ids]

    all_reports = []

    for prompt_id in available:
        try:
            responses = load_responses_for_prompt(prompt_id, RAW_OUTPUTS)
        except FileNotFoundError:
            continue

        if len(responses) < min_models:
            print(f"[skip] {prompt_id}: only {len(responses)}/{min_models} models")
            continue

        print(f"\n[{prompt_id}] ({DOMAIN_MAP.get(prompt_id,'?')}) {len(responses)} models:", end="", flush=True)
        report = run_metrics_for_prompt(prompt_id, responses)

        # Save individual report
        out_file = RESULTS_DIR / f"{prompt_id}-metrics.json"
        out_file.write_text(json.dumps(report, indent=2, ensure_ascii=False))

        all_reports.append(report)

    # Save aggregate summary CSV
    _save_aggregate_csv(all_reports)
    # Save full aggregate JSON
    agg_file = RESULTS_DIR / "aggregate.json"
    # Remove embeddings from aggregate to keep size manageable
    slim = []
    for r in all_reports:
        s = dict(r)
        if "cosine" in s and "embeddings" in s["cosine"]:
            s["cosine"] = {k: v for k, v in s["cosine"].items() if k != "embeddings"}
        slim.append(s)
    agg_file.write_text(json.dumps(slim, indent=2, ensure_ascii=False))

    print(f"\n\n[Pipeline] Complete. {len(all_reports)} prompts processed.")
    print(f"Results saved to: {RESULTS_DIR}")
    return all_reports


ALL_MODEL_IDS_FOR_CSV = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12"]


def _save_aggregate_csv(reports: list[dict]) -> None:
    """Save a flat CSV with one row per prompt for easy analysis."""
    csv_file = RESULTS_DIR / "aggregate.csv"
    token_cols = [f"tokens_{m}" for m in ALL_MODEL_IDS_FOR_CSV]
    fields = [
        "prompt_id", "domain", "n_models",
        "cosine_mean", "cosine_min", "cosine_std",
        "bertscore_mean_f1", "bertscore_min_f1",
        "jaccard_mean", "jaccard_min",
        "n_outliers", "outlier_models",
        *token_cols,
    ]
    rows = []
    for r in reports:
        row = {
            "prompt_id": r["prompt_id"],
            "domain": r["domain"],
            "n_models": r["n_models"],
            "cosine_mean":       r.get("cosine", {}).get("mean", r.get("cosine", {}).get("mean_similarity", "")),
            "cosine_min":        r.get("cosine", {}).get("min",  r.get("cosine", {}).get("min_similarity",  "")),
            "cosine_std":        r.get("cosine", {}).get("std",  r.get("cosine", {}).get("std_similarity",  "")),
            "bertscore_mean_f1": r.get("bertscore", {}).get("mean_f1", ""),
            "bertscore_min_f1":  r.get("bertscore", {}).get("min_f1", ""),
            "jaccard_mean":      r.get("jaccard", {}).get("mean_jaccard", ""),
            "jaccard_min":       r.get("jaccard", {}).get("min_jaccard", ""),
            "n_outliers":        r.get("outliers", {}).get("n_outliers", ""),
            "outlier_models":    ",".join(
                r.get("outliers", {}).get("outlier_models",
                r.get("outliers", {}).get("outliers", []))),
        }
        tokens = r.get("response_tokens", {})
        for m in ALL_MODEL_IDS_FOR_CSV:
            row[f"tokens_{m}"] = tokens.get(m, "")
        rows.append(row)

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  CSV: {csv_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BMAS Metrics Pipeline")
    parser.add_argument("--min-models", type=int, default=5)
    parser.add_argument("--prompt-ids", nargs="+")
    args = parser.parse_args()
    run_all(prompt_ids=args.prompt_ids, min_models=args.min_models)
