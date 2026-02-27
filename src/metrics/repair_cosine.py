"""
BMAS Cosine Repair Script

Re-computes cosine similarity for all prompts where it failed (CUDA error on local GPU).
Uses the GPU bridge /embed endpoint instead of local SentenceTransformer.

Usage:
    GPU_BRIDGE_URL=http://localhost:8765 python3 repair_cosine.py
    # or just run without env var - defaults to localhost:8765
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import requests

RESULTS_DIR = Path(__file__).parent.parent.parent / "results"
RAW_OUTPUTS_DIR = Path(__file__).parent.parent.parent / "experiments" / "raw-outputs"
GPU_BRIDGE_URL = os.environ.get("GPU_BRIDGE_URL", "http://localhost:8765")


def embed_via_bridge(texts: list[str]) -> list[list[float]]:
    """Send texts to GPU bridge /embed endpoint, return embeddings."""
    resp = requests.post(
        f"{GPU_BRIDGE_URL}/embed",
        json={"texts": texts, "batch_size": 32},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["embeddings"]


def compute_cosine(embeddings: list[list[float]], model_ids: list[str]) -> dict:
    """Compute pairwise cosine similarity from normalized embeddings."""
    emb = np.array(embeddings)
    # Normalize (should already be, but just in case)
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    emb_norm = emb / norms

    matrix = np.inner(emb_norm, emb_norm)

    n = len(model_ids)
    pairs = []
    pair_details = []
    for i in range(n):
        for j in range(i + 1, n):
            sim = float(matrix[i][j])
            pairs.append(sim)
            pair_details.append({
                "model_a": model_ids[i],
                "model_b": model_ids[j],
                "cosine": sim,
            })

    return {
        "model_ids": model_ids,
        "matrix": matrix.tolist(),
        "embeddings": emb_norm.tolist(),
        "mean": float(np.mean(pairs)) if pairs else 0.0,
        "min": float(np.min(pairs)) if pairs else 0.0,
        "max": float(np.max(pairs)) if pairs else 0.0,
        "std": float(np.std(pairs)) if pairs else 0.0,
        "pair_count": len(pairs),
        "pairs": pair_details,
    }


def needs_repair(cosine_data: dict) -> bool:
    """Check if cosine result is missing or errored."""
    if not cosine_data:
        return True
    if "error" in cosine_data:
        return True
    if "mean" not in cosine_data and "mean_similarity" not in cosine_data:
        return True
    return False


def main():
    # Check GPU bridge reachability
    try:
        r = requests.get(f"{GPU_BRIDGE_URL}/health", timeout=5)
        r.raise_for_status()
        print(f"GPU bridge reachable at {GPU_BRIDGE_URL}")
    except Exception as e:
        print(f"ERROR: GPU bridge not reachable: {e}")
        sys.exit(1)

    result_files = sorted(RESULTS_DIR.glob("*-metrics.json"))
    print(f"Found {len(result_files)} result files")

    repaired = 0
    skipped = 0
    errors = []

    for fpath in result_files:
        prompt_id = fpath.stem.replace("-metrics", "")

        with open(fpath) as f:
            data = json.load(f)

        cosine_data = data.get("cosine", {})
        if not needs_repair(cosine_data):
            print(f"[{prompt_id}] cosine OK - skip")
            skipped += 1
            continue

        # Load model responses from raw-outputs
        raw_dir = RAW_OUTPUTS_DIR / prompt_id
        if not raw_dir.exists():
            print(f"[{prompt_id}] WARNING: no raw-outputs dir {raw_dir} - skip")
            errors.append(prompt_id)
            continue

        responses = {}
        for rf in sorted(raw_dir.glob("M*.json")):
            with open(rf) as f:
                rd = json.load(f)
            mid = rd.get("model_id", rf.stem)
            text = rd.get("response", "")
            if text:
                responses[mid] = text

        if not responses:
            print(f"[{prompt_id}] WARNING: no valid responses found - skip")
            errors.append(prompt_id)
            continue

        model_ids = sorted(responses.keys())
        texts = [responses[mid] for mid in model_ids]

        print(f"[{prompt_id}] computing cosine for {len(texts)} models via GPU bridge...", end="", flush=True)
        t0 = time.time()

        try:
            embeddings = embed_via_bridge(texts)
            cosine_result = compute_cosine(embeddings, model_ids)
            elapsed = time.time() - t0
            print(f" {elapsed:.2f}s - mean={cosine_result['mean']:.4f}")

            # Update the data
            data["cosine"] = cosine_result

            # Also update outlier detection if embeddings are available
            # (DBSCAN uses embeddings from cosine result)
            try:
                sys.path.insert(0, str(Path(__file__).parent))
                from deviation import detect_outliers
                outlier_result = detect_outliers(cosine_result)
                data["outliers"] = outlier_result
                print(f"  outliers updated: {outlier_result.get('outliers', [])}")
            except Exception as oe:
                print(f"  outlier update skipped: {oe}")

            with open(fpath, "w") as f:
                json.dump(data, f, indent=2)

            repaired += 1

        except Exception as e:
            print(f" ERROR: {e}")
            errors.append(prompt_id)

    print()
    print(f"Done: {repaired} repaired, {skipped} skipped, {len(errors)} errors")
    if errors:
        print(f"Errors: {errors}")

    # Rebuild aggregate CSV
    if repaired > 0:
        print("\nRebuilding aggregate CSV...")
        rebuild_aggregate(result_files)


def rebuild_aggregate(result_files):
    """Rebuild aggregate.csv and aggregate.json from all result files."""
    rows = []
    all_data = []

    for fpath in sorted(result_files):
        with open(fpath) as f:
            data = json.load(f)

        prompt_id = data.get("prompt_id", fpath.stem.replace("-metrics", ""))
        domain = data.get("domain", "unknown")
        model_ids = data.get("model_ids", [])
        n_models = len(model_ids)

        cosine = data.get("cosine", {})
        bertscore = data.get("bertscore", {})
        jaccard = data.get("jaccard", {})
        response_tokens = data.get("response_tokens", {})

        cos_mean = cosine.get("mean", cosine.get("mean_similarity", None))
        cos_min = cosine.get("min", cosine.get("min_similarity", None))
        cos_std = cosine.get("std", cosine.get("std_similarity", None))

        bs_mean = bertscore.get("mean_f1", None)
        bs_min = bertscore.get("min_f1", None)

        jac_mean = jaccard.get("mean_jaccard", None)
        jac_min = jaccard.get("min_jaccard", None)

        outliers = data.get("outliers", {})
        n_outliers = outliers.get("n_outliers", len(outliers.get("outliers", [])))
        outlier_list = outliers.get("outliers", outliers.get("outlier_models", []))
        outlier_models = ",".join(outlier_list) if isinstance(outlier_list, list) else str(outlier_list)

        # Token columns for M1-M12
        token_cols = {}
        for i in range(1, 13):
            mid = f"M{i}"
            token_cols[f"tokens_{mid}"] = response_tokens.get(mid, 0)

        row = {
            "prompt_id": prompt_id,
            "domain": domain,
            "n_models": n_models,
            "cosine_mean": cos_mean,
            "cosine_min": cos_min,
            "cosine_std": cos_std,
            "bertscore_mean_f1": bs_mean,
            "bertscore_min_f1": bs_min,
            "jaccard_mean": jac_mean,
            "jaccard_min": jac_min,
            "n_outliers": n_outliers,
            "outlier_models": outlier_models,
            **token_cols,
        }
        rows.append(row)
        all_data.append(data)

    # Write CSV
    import csv
    csv_path = RESULTS_DIR / "aggregate.csv"
    if rows:
        fieldnames = list(rows[0].keys())
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"aggregate.csv written ({len(rows)} rows)")

    # Write JSON
    json_path = RESULTS_DIR / "aggregate.json"
    with open(json_path, "w") as f:
        json.dump(all_data, f, indent=2)
    print(f"aggregate.json written ({len(all_data)} entries)")


if __name__ == "__main__":
    main()
