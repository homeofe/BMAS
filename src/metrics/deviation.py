"""
BMAS Deviation Metrics

Computes inter-model divergence across multiple model responses to the same prompt.

Metrics:
    1. Cosine similarity via sentence-transformers (semantic)
    2. BERTScore F1 (token-level learned similarity)
    3. Jaccard similarity on extracted key claims (structural)
    4. DBSCAN outlier detection in embedding space

Dependencies:
    pip install sentence-transformers bert-score scikit-learn numpy
"""

import json
import re
from pathlib import Path
from typing import Any

import numpy as np


# --------------------------------------------------------------------------
# Cosine Similarity (sentence-transformers)
# --------------------------------------------------------------------------

def compute_cosine_matrix(responses: dict[str, str], model_name: str = "all-mpnet-base-v2") -> dict[str, Any]:
    """
    Compute pairwise cosine similarity matrix across model responses.

    Args:
        responses: dict of model_id -> response_text
        model_name: sentence-transformer model to use

    Returns:
        dict with 'matrix', 'model_ids', 'mean_similarity', 'min_similarity', 'embeddings'
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError("Run: pip install sentence-transformers")

    model_ids = sorted(responses.keys())
    texts = [responses[mid] for mid in model_ids]

    model = SentenceTransformer(model_name, device="cpu")
    embeddings = model.encode(texts, normalize_embeddings=True)

    matrix = np.inner(embeddings, embeddings)

    # Extract upper triangle (excluding diagonal) for summary stats
    n = len(model_ids)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append(matrix[i][j])

    return {
        "model_ids": model_ids,
        "matrix": matrix.tolist(),
        "embeddings": embeddings.tolist(),
        "mean_similarity": float(np.mean(pairs)),
        "min_similarity": float(np.min(pairs)),
        "max_similarity": float(np.max(pairs)),
        "std_similarity": float(np.std(pairs)),
        "pair_count": len(pairs),
    }


# --------------------------------------------------------------------------
# BERTScore
# --------------------------------------------------------------------------

def compute_bertscore(responses: dict[str, str], lang: str = "en") -> dict[str, Any]:
    """
    Compute pairwise BERTScore F1 across model responses.
    Uses each response as both candidate and reference alternately.

    Returns: dict with pairwise F1 scores and summary stats
    """
    try:
        from bert_score import score as bert_score
    except ImportError:
        raise ImportError("Run: pip install bert-score")

    model_ids = sorted(responses.keys())
    texts = [responses[mid] for mid in model_ids]
    n = len(texts)

    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            cands = [texts[i]]
            refs = [texts[j]]
            _, _, f1 = bert_score(cands, refs, lang=lang, verbose=False, device="cpu")
            score = float(f1[0].item())
            pairs.append({
                "model_a": model_ids[i],
                "model_b": model_ids[j],
                "bertscore_f1": score,
            })

    f1_values = [p["bertscore_f1"] for p in pairs]

    return {
        "model_ids": model_ids,
        "pairs": pairs,
        "mean_f1": float(np.mean(f1_values)),
        "min_f1": float(np.min(f1_values)),
        "max_f1": float(np.max(f1_values)),
        "std_f1": float(np.std(f1_values)),
    }


# --------------------------------------------------------------------------
# Jaccard on Key Claims
# --------------------------------------------------------------------------

def extract_claims(text: str) -> set[str]:
    """
    Extract normalized key claims from a response.
    Simple heuristic: split on sentence boundaries, normalize, deduplicate.
    For paper: replace with fine-tuned claim extraction or OpenIE.
    """
    # Split on newlines and sentence endings
    raw = re.split(r"[\n\.!?]+", text)
    claims = set()
    for line in raw:
        line = line.strip().lower()
        # Remove bullet markers
        line = re.sub(r"^[-*•\d]+[\.\)]\s*", "", line)
        # Remove very short lines (not informative)
        if len(line) > 20:
            claims.add(line)
    return claims


def compute_jaccard(responses: dict[str, str]) -> dict[str, Any]:
    """
    Compute pairwise Jaccard similarity on extracted claim sets.
    """
    model_ids = sorted(responses.keys())
    claim_sets = {mid: extract_claims(responses[mid]) for mid in model_ids}
    n = len(model_ids)

    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            a = claim_sets[model_ids[i]]
            b = claim_sets[model_ids[j]]
            if not a and not b:
                jaccard = 1.0
            elif not a or not b:
                jaccard = 0.0
            else:
                jaccard = len(a & b) / len(a | b)
            pairs.append({
                "model_a": model_ids[i],
                "model_b": model_ids[j],
                "jaccard": jaccard,
                "claims_a": len(a),
                "claims_b": len(b),
                "intersection": len(a & b),
                "union": len(a | b),
            })

    j_values = [p["jaccard"] for p in pairs]

    return {
        "model_ids": model_ids,
        "pairs": pairs,
        "mean_jaccard": float(np.mean(j_values)),
        "min_jaccard": float(np.min(j_values)),
        "max_jaccard": float(np.max(j_values)),
    }


# --------------------------------------------------------------------------
# Outlier Detection
# --------------------------------------------------------------------------

def detect_outliers(cosine_result: dict[str, Any], eps: float = 0.15, min_samples: int = 2) -> dict[str, Any]:
    """
    Detect outlier models using DBSCAN in embedding space.
    Outlier label = -1 in DBSCAN output.

    eps: maximum distance for neighborhood (1 - cosine_similarity)
    """
    try:
        from sklearn.cluster import DBSCAN
    except ImportError:
        raise ImportError("Run: pip install scikit-learn")

    model_ids = cosine_result["model_ids"]
    embeddings = np.array(cosine_result["embeddings"])

    # Convert cosine similarity matrix to distance matrix
    sim_matrix = np.array(cosine_result["matrix"])
    dist_matrix = 1 - sim_matrix
    np.fill_diagonal(dist_matrix, 0)

    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="precomputed")
    labels = clustering.fit_predict(dist_matrix)

    result = {
        "model_ids": model_ids,
        "labels": labels.tolist(),
        "outliers": [model_ids[i] for i, label in enumerate(labels) if label == -1],
        "clusters": {},
        "eps": eps,
        "min_samples": min_samples,
    }

    for i, label in enumerate(labels):
        if label == -1:
            continue
        cluster_key = str(label)
        if cluster_key not in result["clusters"]:
            result["clusters"][cluster_key] = []
        result["clusters"][cluster_key].append(model_ids[i])

    return result


# --------------------------------------------------------------------------
# Full Metric Pipeline
# --------------------------------------------------------------------------

def compute_all_metrics(prompt_id: str, responses: dict[str, str]) -> dict[str, Any]:
    """
    Run all BMAS metrics for a single prompt's responses.

    Args:
        prompt_id: the prompt identifier (e.g. "A01")
        responses: dict of model_id -> response_text

    Returns:
        Full metric report for this prompt
    """
    print(f"[Metrics] Computing metrics for prompt {prompt_id} ({len(responses)} models)")

    report: dict[str, Any] = {
        "prompt_id": prompt_id,
        "model_ids": sorted(responses.keys()),
        "n_models": len(responses),
    }

    print("  -> Cosine similarity...")
    try:
        cosine = compute_cosine_matrix(responses)
        report["cosine"] = cosine
    except Exception as e:
        print(f"  [WARN] Cosine failed: {e}")
        report["cosine"] = {"error": str(e)}
        cosine = None

    print("  -> BERTScore...")
    try:
        report["bertscore"] = compute_bertscore(responses)
    except Exception as e:
        print(f"  [WARN] BERTScore failed: {e}")
        report["bertscore"] = {"error": str(e)}

    print("  -> Jaccard...")
    try:
        report["jaccard"] = compute_jaccard(responses)
    except Exception as e:
        print(f"  [WARN] Jaccard failed: {e}")
        report["jaccard"] = {"error": str(e)}

    if cosine and "error" not in cosine:
        print("  -> Outlier detection...")
        try:
            report["outliers"] = detect_outliers(cosine)
        except Exception as e:
            print(f"  [WARN] Outlier detection failed: {e}")
            report["outliers"] = {"error": str(e)}

    return report


def load_responses_for_prompt(prompt_id: str, raw_output_dir: Path) -> dict[str, str]:
    """
    Load all model responses for a given prompt from the raw-outputs directory.
    """
    prompt_dir = raw_output_dir / prompt_id
    if not prompt_dir.exists():
        raise FileNotFoundError(f"No outputs found for prompt {prompt_id} at {prompt_dir}")

    responses = {}
    for f in sorted(prompt_dir.glob("*.json")):
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
        model_id = data["model_id"]
        response = data["response"]
        if response and response != "[DRY RUN - no actual model call made]":
            responses[model_id] = response

    return responses


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BMAS Deviation Metrics")
    parser.add_argument("--prompt-id", required=True, help="Prompt ID (e.g. A01)")
    parser.add_argument("--raw-outputs", default="experiments/raw-outputs", help="Raw outputs directory")
    parser.add_argument("--output", help="Output JSON file (default: results/<prompt_id>-metrics.json)")
    args = parser.parse_args()

    raw_dir = Path(args.raw_outputs)
    responses = load_responses_for_prompt(args.prompt_id, raw_dir)
    print(f"Loaded {len(responses)} model responses for {args.prompt_id}")

    report = compute_all_metrics(args.prompt_id, responses)

    output_path = Path(args.output) if args.output else Path("results") / f"{args.prompt_id}-metrics.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nMetrics saved to: {output_path}")
