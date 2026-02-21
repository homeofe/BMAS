"""
BMAS Runner - Blind Multi-Agent Synthesis prompt runner.

Sends identical prompts to multiple models in strict isolation.
No model output is shared with any other model during this phase.

Usage:
    python runner.py --prompt experiments/prompts/domain-A-technical.md --prompt-id A01 --all-models
    python runner.py --prompt-file prompts.json --output experiments/raw-outputs/
"""

import argparse
import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Model registry - mirrors the BMAS model table
MODELS = {
    "M1": {
        "id": "M1",
        "name": "claude-sonnet-4-6",
        "provider": "anthropic",
        "model_string": "claude-sonnet-4-6",
    },
    "M2": {
        "id": "M2",
        "name": "claude-opus-4-6",
        "provider": "anthropic",
        "model_string": "claude-opus-4-6",
    },
    "M3": {
        "id": "M3",
        "name": "gpt-5.3-codex",
        "provider": "openai-codex",
        "model_string": "openai-codex/gpt-5.3-codex",
    },
    "M4": {
        "id": "M4",
        "name": "gemini-2.5-pro",
        "provider": "google-gemini-cli",
        "model_string": "google-gemini-cli/gemini-2.5-pro",
    },
    "M5": {
        "id": "M5",
        "name": "sonar-pro",
        "provider": "perplexity",
        "model_string": "perplexity/sonar-pro",
    },
}

# Strict isolation system prompt - no hints about other models or this being a study
ISOLATION_SYSTEM_PROMPT = (
    "You are a knowledgeable expert assistant. Answer the following question "
    "as accurately and completely as possible. Be precise, factual, and structured. "
    "If you are uncertain about any specific detail, say so explicitly."
)


def build_run_record(
    prompt_id: str,
    model_id: str,
    prompt_text: str,
    domain: str,
    response: str,
    response_tokens: int,
    latency_ms: int,
) -> dict[str, Any]:
    return {
        "run_id": f"{prompt_id}-{model_id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "bmas_version": "1.0",
        "prompt_id": prompt_id,
        "model_id": model_id,
        "model": MODELS[model_id]["model_string"],
        "domain": domain,
        "prompt": prompt_text,
        "system": ISOLATION_SYSTEM_PROMPT,
        "response": response,
        "response_tokens": response_tokens,
        "latency_ms": latency_ms,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def run_model_via_openclaw(model_id: str, prompt: str) -> tuple[str, int, int]:
    """
    Calls a model via OpenClaw sessions_spawn (isolated).
    Returns (response_text, estimated_tokens, latency_ms).

    NOTE: In v1, this is a stub. The actual implementation calls the OpenClaw
    API or CLI to spawn isolated sub-agent sessions per model.
    Replace with real API call once runner is integrated with OpenClaw.
    """
    # TODO: implement via openclaw CLI or direct API
    # openclaw sessions spawn --agent <model> --task "<prompt>" --mode run
    raise NotImplementedError(
        f"Model runner for {model_id} not yet implemented. "
        "Implement via OpenClaw sessions_spawn or direct provider API."
    )


def save_output(output_dir: Path, record: dict[str, Any]) -> Path:
    prompt_dir = output_dir / record["prompt_id"]
    prompt_dir.mkdir(parents=True, exist_ok=True)
    out_path = prompt_dir / f"{record['model_id']}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {out_path}")
    return out_path


def run_blind_prompt(
    prompt_id: str,
    prompt_text: str,
    domain: str,
    model_ids: list[str],
    output_dir: Path,
    dry_run: bool = False,
) -> list[dict[str, Any]]:
    """
    Run a single prompt against all specified models in isolation.
    Outputs one JSON file per model under output_dir/<prompt_id>/<model_id>.json
    """
    print(f"\n[BMAS] Running prompt {prompt_id} ({domain}) against {len(model_ids)} models")

    results = []
    for model_id in model_ids:
        model = MODELS[model_id]
        print(f"  -> {model_id}: {model['model_string']}")

        if dry_run:
            record = build_run_record(
                prompt_id=prompt_id,
                model_id=model_id,
                prompt_text=prompt_text,
                domain=domain,
                response="[DRY RUN - no actual model call made]",
                response_tokens=0,
                latency_ms=0,
            )
            save_output(output_dir, record)
            results.append(record)
            continue

        try:
            start = time.time()
            response, tokens = run_model_via_openclaw(model_id, prompt_text)
            latency = int((time.time() - start) * 1000)

            record = build_run_record(
                prompt_id=prompt_id,
                model_id=model_id,
                prompt_text=prompt_text,
                domain=domain,
                response=response,
                response_tokens=tokens,
                latency_ms=latency,
            )
            save_output(output_dir, record)
            results.append(record)

        except NotImplementedError as e:
            print(f"  [SKIP] {e}")
        except Exception as e:
            print(f"  [ERROR] {model_id}: {e}")

    return results


def main():
    parser = argparse.ArgumentParser(description="BMAS Blind Multi-Agent Prompt Runner")
    parser.add_argument("--prompt-id", required=True, help="Prompt ID (e.g. A01, B05, C03)")
    parser.add_argument("--prompt", required=True, help="Prompt text (or @file.txt to read from file)")
    parser.add_argument("--domain", required=True, choices=["technical", "regulatory", "strategic"])
    parser.add_argument("--models", nargs="+", default=list(MODELS.keys()), help="Model IDs to run (default: all)")
    parser.add_argument("--output-dir", default="experiments/raw-outputs", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (no actual model calls)")
    args = parser.parse_args()

    prompt_text = args.prompt
    if prompt_text.startswith("@"):
        with open(prompt_text[1:], encoding="utf-8") as f:
            prompt_text = f.read().strip()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_blind_prompt(
        prompt_id=args.prompt_id,
        prompt_text=prompt_text,
        domain=args.domain,
        model_ids=args.models,
        output_dir=output_dir,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
