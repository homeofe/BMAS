"""
BMAS Synthesizer - Three synthesis strategies

S1: Majority-Vote (claim-level)
    Extracts factual claims from each response.
    A claim is "accepted" if present in >= threshold fraction of models.

S2: Semantic Centroid
    Finds the response closest to the mean embedding vector.
    Uses it as the base; appends minority claims present in >=2 other models.

S3: LLM-as-Judge
    Sends all responses to a dedicated synthesis model (claude-opus-4-6).
    The judge produces a single authoritative synthesis with [MINORITY] and [DISPUTED] markers.
    This model must NOT have been one of the original respondents for this prompt.
"""

import json
from enum import Enum
from pathlib import Path
from typing import Any

import numpy as np


class SynthesisStrategy(str, Enum):
    MAJORITY_VOTE = "S1"
    SEMANTIC_CENTROID = "S2"
    LLM_AS_JUDGE = "S3"


# --------------------------------------------------------------------------
# S1: Majority-Vote
# --------------------------------------------------------------------------

def _normalize_claim(claim: str) -> str:
    return claim.strip().lower()


def _extract_claims_from_response(text: str) -> list[str]:
    """Extract discrete claims. Simple heuristic for v1."""
    import re
    lines = re.split(r"[\n.!?]+", text)
    claims = []
    for line in lines:
        line = line.strip()
        line = re.sub(r"^[-*•\d]+[\.\)]\s*", "", line)
        if len(line) > 25:
            claims.append(line)
    return claims


def synthesize_majority_vote(responses: dict[str, str], threshold: float = 0.6) -> dict[str, Any]:
    """
    Extract claims from all responses. Accept claims present in >= threshold*N models.
    Uses fuzzy matching to identify similar claims across models.

    Returns synthesized text and claim-level vote results.
    """
    from difflib import SequenceMatcher

    model_ids = sorted(responses.keys())
    n = len(model_ids)
    min_votes = max(2, int(n * threshold))

    # Collect all claims with their source
    all_claims: list[dict[str, Any]] = []
    for mid in model_ids:
        for claim in _extract_claims_from_response(responses[mid]):
            all_claims.append({"claim": claim, "source": mid, "normalized": _normalize_claim(claim)})

    # Cluster similar claims
    def similarity(a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    clusters: list[dict[str, Any]] = []
    used = set()

    for i, item in enumerate(all_claims):
        if i in used:
            continue
        cluster = {"representative": item["claim"], "sources": {item["source"]}, "members": [item["claim"]]}
        used.add(i)
        for j, other in enumerate(all_claims):
            if j in used or j == i:
                continue
            if similarity(item["normalized"], other["normalized"]) > 0.75:
                cluster["sources"].add(other["source"])
                cluster["members"].append(other["claim"])
                used.add(j)
        cluster["vote_count"] = len(cluster["sources"])
        cluster["sources"] = list(cluster["sources"])
        clusters.append(cluster)

    accepted = [c for c in clusters if c["vote_count"] >= min_votes]
    minority = [c for c in clusters if c["vote_count"] < min_votes]

    synthesis_text = "\n".join(f"- {c['representative']}" for c in accepted)
    if minority:
        synthesis_text += "\n\n[MINORITY CLAIMS (did not reach consensus)]\n"
        synthesis_text += "\n".join(f"- {c['representative']} (votes: {c['vote_count']})" for c in minority[:5])

    return {
        "strategy": "S1",
        "strategy_name": "Majority-Vote",
        "threshold": threshold,
        "min_votes": min_votes,
        "n_models": n,
        "total_claims": len(all_claims),
        "accepted_claims": len(accepted),
        "minority_claims": len(minority),
        "synthesis": synthesis_text,
        "clusters": clusters,
    }


# --------------------------------------------------------------------------
# S2: Semantic Centroid
# --------------------------------------------------------------------------

def synthesize_semantic_centroid(responses: dict[str, str], embeddings: dict[str, list[float]]) -> dict[str, Any]:
    """
    Find the response whose embedding is closest to the mean of all embeddings.
    That response is the synthesis base.

    Args:
        responses: model_id -> response_text
        embeddings: model_id -> embedding vector (from cosine metric step)
    """
    model_ids = sorted(responses.keys())
    emb_matrix = np.array([embeddings[mid] for mid in model_ids])

    centroid = emb_matrix.mean(axis=0)
    centroid_norm = centroid / (np.linalg.norm(centroid) + 1e-8)

    # Cosine similarity of each response to centroid
    similarities = []
    for i, mid in enumerate(model_ids):
        emb = emb_matrix[i]
        sim = float(np.dot(emb, centroid_norm))
        similarities.append({"model_id": mid, "similarity_to_centroid": sim})

    similarities.sort(key=lambda x: x["similarity_to_centroid"], reverse=True)
    representative_id = similarities[0]["model_id"]

    return {
        "strategy": "S2",
        "strategy_name": "Semantic-Centroid",
        "representative_model": representative_id,
        "similarity_scores": similarities,
        "synthesis": responses[representative_id],
        "note": "Synthesis is the response closest to the semantic centroid of all model embeddings.",
    }


# --------------------------------------------------------------------------
# S3: LLM-as-Judge
# --------------------------------------------------------------------------

LLM_AS_JUDGE_PROMPT_TEMPLATE = """You are a synthesis judge for a research study on LLM response consistency.

You have received {n} independent responses to the same question from {n} different AI models. The models did not see each other's responses.

Your task: Produce a single authoritative synthesis that:
1. Includes all claims that appear in a majority of responses
2. Marks minority claims (appearing in only 1 or 2 responses) with [MINORITY]
3. Marks directly contradictory claims with [DISPUTED: model_a says X, model_b says Y]
4. Does NOT add new information beyond what the models provided
5. Does NOT identify which model said what (treat all as anonymous)

The original question was:
{question}

---

Independent model responses (anonymized):

{responses_block}

---

Produce your synthesis now. Be precise and structured. Use bullet points or numbered lists where appropriate."""


def build_llm_as_judge_prompt(question: str, responses: dict[str, str]) -> str:
    model_ids = sorted(responses.keys())
    blocks = []
    for i, mid in enumerate(model_ids, 1):
        blocks.append(f"[Response {i}]\n{responses[mid]}")

    return LLM_AS_JUDGE_PROMPT_TEMPLATE.format(
        n=len(model_ids),
        question=question,
        responses_block="\n\n---\n\n".join(blocks),
    )


def synthesize_llm_as_judge(
    question: str,
    responses: dict[str, str],
    judge_model: str = "claude-opus-4-6",
) -> dict[str, Any]:
    """
    Use a judge LLM to synthesize all responses into one authoritative output.
    The judge model must be different from the models in the responses (or at minimum
    must receive only the synthesis prompt, not a hint that it was also a respondent).

    Returns:
        dict with strategy, judge_model, synthesis_prompt, synthesis (to be filled after API call)
    """
    prompt = build_llm_as_judge_prompt(question, responses)

    # NOTE: actual API call not implemented here - return the prompt for the runner to execute
    return {
        "strategy": "S3",
        "strategy_name": "LLM-as-Judge",
        "judge_model": judge_model,
        "n_respondents": len(responses),
        "synthesis_prompt": prompt,
        "synthesis": None,  # filled after actual model call
        "note": "Call judge_model with synthesis_prompt to get final synthesis.",
    }


# --------------------------------------------------------------------------
# Batch runner
# --------------------------------------------------------------------------

def synthesize_all(
    prompt_id: str,
    question: str,
    responses: dict[str, str],
    metric_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run all three synthesis strategies for a prompt."""
    results: dict[str, Any] = {"prompt_id": prompt_id, "strategies": {}}

    print(f"[Synthesis] Running S1 Majority-Vote for {prompt_id}...")
    results["strategies"]["S1"] = synthesize_majority_vote(responses)

    if metric_report and "cosine" in metric_report and "error" not in metric_report["cosine"]:
        print(f"[Synthesis] Running S2 Semantic-Centroid for {prompt_id}...")
        model_ids = metric_report["cosine"]["model_ids"]
        embeddings = {
            model_ids[i]: metric_report["cosine"]["embeddings"][i]
            for i in range(len(model_ids))
        }
        results["strategies"]["S2"] = synthesize_semantic_centroid(responses, embeddings)
    else:
        print(f"[Synthesis] Skipping S2 (no embeddings available)")
        results["strategies"]["S2"] = {"strategy": "S2", "skipped": True, "reason": "No cosine metric data"}

    print(f"[Synthesis] Preparing S3 LLM-as-Judge for {prompt_id}...")
    results["strategies"]["S3"] = synthesize_llm_as_judge(question, responses)

    return results
