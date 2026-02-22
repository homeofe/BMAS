#!/usr/bin/env python3
"""
BMAS Direct Re-Runner for failed M6/M7 responses.

Calls provider APIs directly (bypasses OpenClaw gateway timeouts).
- M6 (sonar-deep-research): Perplexity API, 300s timeout
- M7 (gemini-3-pro-preview): Google Generative AI API (needs GOOGLE_API_KEY env var)

Usage:
    # Re-run M6 failed prompts
    python rerun_failed.py --models M6

    # Re-run M7 (after billing enabled)
    GOOGLE_API_KEY=... python rerun_failed.py --models M7

    # Re-run both
    GOOGLE_API_KEY=... python rerun_failed.py --models M6 M7

    # Dry run
    python rerun_failed.py --models M6 --dry-run
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import urllib.request
import urllib.error

# -------------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------------

BMAS_DIR    = Path(__file__).resolve().parent.parent.parent
RAW_OUTPUTS = BMAS_DIR / "experiments" / "raw-outputs"

# -------------------------------------------------------------------------
# Provider configs
# -------------------------------------------------------------------------

OPENCLAW_JSON = Path.home() / ".openclaw" / "openclaw.json"

def _get_perplexity_key() -> str:
    raw = OPENCLAW_JSON.read_text()
    m = re.search(r'"(pplx-[^"]+)"', raw)
    return m.group(1) if m else ""

MODEL_CONFIGS = {
    "M6": {
        "name": "sonar-deep-research",
        "model_string": "perplexity/sonar-deep-research",
        "provider": "perplexity",
        "api_url": "https://api.perplexity.ai/chat/completions",
        "model_id_in_api": "sonar-deep-research",
        "timeout": 360,  # 6 minutes - deep research is slow
    },
    "M7": {
        "name": "gemini-3-pro-preview",
        "model_string": "google-gemini-cli/gemini-3-pro-preview",
        "provider": "google",
        "api_url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "model_id_in_api": "gemini-2.0-pro-exp",  # preview model
        "timeout": 120,
    },
}

ISOLATION_SYSTEM = (
    "You are a knowledgeable expert assistant. "
    "Answer the following question as accurately and completely as possible. "
    "Be precise, factual, and structured. "
    "If you are uncertain about any specific detail, state that explicitly."
)

# -------------------------------------------------------------------------
# Detect failed responses
# -------------------------------------------------------------------------

ERROR_PATTERNS = [
    "401 ", "Authorization Required", "rate limit", "Rate limit",
    "API rate limit", "429", "openresty",
]

def is_error_response(text: str) -> bool:
    if len(text.split()) < 25:
        return any(p in text for p in ERROR_PATTERNS)
    return False

def get_failed_prompts(model_id: str) -> list[str]:
    """Return list of prompt_ids where the model has error/missing responses."""
    failed = []
    for pid in sorted(os.listdir(RAW_OUTPUTS)):
        pdir = RAW_OUTPUTS / pid
        if not pdir.is_dir():
            continue
        fpath = pdir / f"{model_id}.json"
        if not fpath.exists():
            failed.append(pid)
            continue
        with open(fpath) as f:
            d = json.load(f)
        resp = d.get("response", "")
        if is_error_response(resp):
            failed.append(pid)
    return failed

# -------------------------------------------------------------------------
# Load prompts from runner.py (same module)
# -------------------------------------------------------------------------

def load_prompts() -> dict[str, tuple[str, str]]:
    """Load prompt registry from runner.py via importlib."""
    import importlib.util
    runner_path = Path(__file__).parent / "runner.py"
    spec = importlib.util.spec_from_file_location("runner", runner_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod.ALL_PROMPTS

# -------------------------------------------------------------------------
# Direct API call
# -------------------------------------------------------------------------

def call_perplexity(prompt_text: str, config: dict, pplx_key: str) -> tuple[str, dict]:
    """Call Perplexity API directly. Returns (response_text, usage_dict)."""
    payload = json.dumps({
        "model": config["model_id_in_api"],
        "messages": [
            {"role": "system", "content": ISOLATION_SYSTEM},
            {"role": "user",   "content": prompt_text},
        ],
        "max_tokens": 8192,
        "stream": False,
    }).encode()

    req = urllib.request.Request(
        config["api_url"],
        data=payload,
        headers={
            "Authorization": f"Bearer {pplx_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=config["timeout"]) as resp:
        body = json.loads(resp.read().decode())

    choices = body.get("choices", [])
    content = choices[0].get("message", {}).get("content", "") if choices else ""
    usage   = body.get("usage", {})
    return content, usage


def call_google(prompt_text: str, config: dict, google_key: str) -> tuple[str, dict]:
    """Call Google Generative AI API directly. Returns (response_text, usage_dict)."""
    payload = json.dumps({
        "model": config["model_id_in_api"],
        "messages": [
            {"role": "system", "content": ISOLATION_SYSTEM},
            {"role": "user",   "content": prompt_text},
        ],
        "max_tokens": 8192,
    }).encode()

    req = urllib.request.Request(
        config["api_url"],
        data=payload,
        headers={
            "Authorization": f"Bearer {google_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=config["timeout"]) as resp:
        body = json.loads(resp.read().decode())

    if isinstance(body, list):
        body = body[0]

    choices = body.get("choices", [])
    content = choices[0].get("message", {}).get("content", "") if choices else ""
    usage   = body.get("usage", {})
    return content, usage


def run_model(model_id: str, prompt_id: str, prompt_text: str,
              domain: str, config: dict, api_key: str,
              dry_run: bool = False) -> dict:
    """Run one prompt for one model. Returns record dict."""
    print(f"  {model_id} / {prompt_id} ({domain})... ", end="", flush=True)
    start = time.time()

    if dry_run:
        print("DRY RUN")
        return {"prompt_id": prompt_id, "model_id": model_id, "response": "[DRY RUN]"}

    try:
        if config["provider"] == "perplexity":
            content, usage = call_perplexity(prompt_text, config, api_key)
        elif config["provider"] == "google":
            content, usage = call_google(prompt_text, config, api_key)
        else:
            raise ValueError(f"Unknown provider: {config['provider']}")

        latency = int((time.time() - start) * 1000)
        tokens_out = usage.get("completion_tokens", usage.get("output_tokens", 0))
        tokens_in  = usage.get("prompt_tokens",     usage.get("input_tokens",  0))

        print(f"OK ({tokens_out} tokens, {latency}ms)")

        record = {
            "run_id":          f"{prompt_id}-{model_id}-rerun-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "bmas_version":    "1.0",
            "prompt_id":       prompt_id,
            "model_id":        model_id,
            "model":           config["model_string"],
            "domain":          domain,
            "prompt":          prompt_text,
            "response":        content,
            "response_tokens": tokens_out,
            "input_tokens":    tokens_in,
            "latency_ms":      latency,
            "rerun":           True,
            "timestamp":       datetime.now(timezone.utc).isoformat(),
        }
        return record

    except Exception as e:
        latency = int((time.time() - start) * 1000)
        print(f"FAILED ({latency}ms): {e}")
        return {
            "prompt_id": prompt_id, "model_id": model_id,
            "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def save_record(record: dict) -> None:
    pid = record["prompt_id"]
    mid = record["model_id"]
    out_path = RAW_OUTPUTS / pid / f"{mid}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)


# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="BMAS Direct Re-Runner for failed responses")
    parser.add_argument("--models", nargs="+", choices=["M6", "M7"], required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--prompt-ids", nargs="+", help="Limit to specific prompt IDs")
    args = parser.parse_args()

    all_prompts = load_prompts()
    pplx_key    = _get_perplexity_key()
    google_key  = os.environ.get("GOOGLE_API_KEY", "")

    for model_id in args.models:
        config = MODEL_CONFIGS[model_id]

        # Select API key
        if config["provider"] == "perplexity":
            api_key = pplx_key
            if not api_key:
                print(f"ERROR: No Perplexity API key found for {model_id}")
                sys.exit(1)
        elif config["provider"] == "google":
            api_key = google_key
            if not api_key:
                print(f"ERROR: Set GOOGLE_API_KEY env var to re-run {model_id}")
                sys.exit(1)
        else:
            api_key = ""

        failed = get_failed_prompts(model_id)
        if args.prompt_ids:
            failed = [p for p in failed if p in args.prompt_ids]

        print(f"\n[{model_id}] {config['name']} — {len(failed)} prompts to re-run")
        if not failed:
            print("  Nothing to do.")
            continue

        ok = 0
        err = 0
        for pid in failed:
            if pid not in all_prompts:
                print(f"  SKIP {pid}: not in prompt registry")
                continue
            domain, prompt_text = all_prompts[pid]
            record = run_model(model_id, pid, prompt_text, domain,
                               config, api_key, dry_run=args.dry_run)
            if "error" not in record and not args.dry_run:
                save_record(record)
                ok += 1
            elif "error" in record:
                err += 1
            # Small delay to avoid rate limits
            if not args.dry_run:
                time.sleep(2)

        print(f"\n[{model_id}] Done — OK: {ok}, Errors: {err}")

    print("\nRe-run complete. Next: run src/metrics/run_pipeline.py to recompute metrics.")


if __name__ == "__main__":
    main()
