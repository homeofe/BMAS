#!/usr/bin/env python3
"""
Re-run failed M7 prompts via OpenClaw cron (uses OAuth, not API key).
Runs prompts in parallel batches for speed.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BMAS_DIR = Path(__file__).resolve().parent.parent.parent
RAW_OUTPUTS = BMAS_DIR / "experiments" / "raw-outputs"
PROMPTS_DIR = BMAS_DIR / "experiments" / "prompts"

MODEL_STRING = "google-gemini-cli/gemini-3-pro-preview"
MODEL_ID = "M7"
BATCH_SIZE = 4  # parallel jobs
TIMEOUT_S = 180

ISOLATION_SYSTEM = (
    "You are a knowledgeable expert assistant. "
    "Answer the following question as accurately and completely as possible. "
    "Be precise, factual, and structured. "
    "If you are uncertain about any specific detail, state that explicitly."
)


def openclaw(args):
    r = subprocess.run(["openclaw"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"openclaw {' '.join(args[:3])} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def find_failed_prompts():
    failed = []
    for d in sorted(RAW_OUTPUTS.iterdir()):
        m7 = d / "M7.json"
        if not m7.exists():
            failed.append(d.name)
            continue
        data = json.load(open(m7))
        resp = data.get("response", "")
        if (len(resp) < 100 or
            "rate limit" in resp.lower() or
            "429" in resp or
            "quota" in resp.lower() or
            "resource has been exhausted" in resp.lower()):
            failed.append(d.name)
    return failed


def get_prompt_text(prompt_id):
    """Get prompt text and domain from existing M7.json (or any model file)."""
    prompt_dir = RAW_OUTPUTS / prompt_id
    # Try M7 first (has the original prompt), then any other model
    for mfile in ["M7.json", "M1.json", "M2.json", "M3.json"]:
        p = prompt_dir / mfile
        if p.exists():
            data = json.load(open(p))
            return data["prompt"], data.get("domain", "unknown")
    raise FileNotFoundError(f"Prompt {prompt_id} not found in raw-outputs")


def get_response_from_session(session_id):
    sessions_dir = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
    for f in sessions_dir.glob("*.jsonl"):
        if session_id in f.name:
            lines = f.read_text().strip().split("\n")
            for line in reversed(lines):
                entry = json.loads(line)
                if entry.get("role") == "assistant":
                    content = entry.get("content", "")
                    if isinstance(content, list):
                        return "".join(p.get("text", "") for p in content)
                    return content
    # Try via cron runs
    return ""


def run_batch(prompt_ids):
    """Run a batch of prompts in parallel via cron jobs."""
    jobs = {}

    # Create and trigger all jobs
    for pid in prompt_ids:
        prompt_text, domain = get_prompt_text(pid)
        full_msg = f"{ISOLATION_SYSTEM}\n\n{prompt_text}"
        try:
            raw = openclaw([
                "cron", "add",
                "--name", f"bmas-{pid}-M7-rerun",
                "--session", "isolated",
                "--model", MODEL_STRING,
                "--message", full_msg,
                "--no-deliver",
                "--timeout-seconds", str(TIMEOUT_S),
                "--at", "1m",
                "--delete-after-run",
                "--json",
            ])
            data = json.loads(raw)
            job_id = data["id"]
            openclaw(["cron", "run", job_id, "--timeout", str((TIMEOUT_S + 60) * 1000)])
            jobs[pid] = {"job_id": job_id, "domain": domain, "prompt": prompt_text}
            print(f"  {pid}: triggered ({job_id[:8]})")
        except Exception as e:
            print(f"  {pid}: FAILED to create job: {e}")

    # Wait for all jobs
    results = {}
    deadline = time.time() + TIMEOUT_S + 120
    pending = set(jobs.keys())

    while pending and time.time() < deadline:
        time.sleep(5)
        for pid in list(pending):
            job_id = jobs[pid]["job_id"]
            try:
                raw = openclaw(["cron", "runs", "--id", job_id])
                data = json.loads(raw)
                entries = data.get("entries", [])
                for entry in entries:
                    if entry.get("action") == "finished":
                        session_id = entry.get("sessionId", "")
                        status = entry.get("status", "")
                        if status == "ok" and session_id:
                            resp = get_response_from_session(session_id)
                            if resp and len(resp) > 50:
                                results[pid] = {
                                    "response": resp,
                                    "session_id": session_id,
                                    "usage": entry.get("usage", {}),
                                }
                                print(f"  {pid}: OK ({len(resp)} chars)")
                            else:
                                # Try summary
                                summary = entry.get("summary", "")
                                if summary and len(summary) > 50:
                                    results[pid] = {
                                        "response": summary,
                                        "session_id": session_id,
                                        "usage": entry.get("usage", {}),
                                    }
                                    print(f"  {pid}: OK via summary ({len(summary)} chars)")
                                else:
                                    print(f"  {pid}: EMPTY response")
                        else:
                            print(f"  {pid}: job status={status}")
                        pending.discard(pid)
                        break
            except Exception:
                pass

    for pid in pending:
        print(f"  {pid}: TIMEOUT")

    return results


def save_result(prompt_id, domain, prompt_text, response, usage, session_id):
    out_dir = RAW_OUTPUTS / prompt_id
    out_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "run_id": f"{prompt_id}-M7-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "bmas_version": "1.0",
        "prompt_id": prompt_id,
        "model_id": "M7",
        "model": MODEL_STRING,
        "domain": domain,
        "prompt": prompt_text,
        "response": response,
        "response_tokens": usage.get("output_tokens", 0),
        "input_tokens": usage.get("input_tokens", 0),
        "latency_ms": 0,
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(out_dir / "M7.json", "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)


def main():
    failed = find_failed_prompts()
    print(f"[M7 Re-run via OpenClaw] {len(failed)} failed prompts\n")

    if not failed:
        print("Nothing to re-run!")
        return

    ok_count = 0
    err_count = 0

    for i in range(0, len(failed), BATCH_SIZE):
        batch = failed[i:i + BATCH_SIZE]
        print(f"\nBatch {i // BATCH_SIZE + 1} ({len(batch)} prompts):")
        results = run_batch(batch)

        for pid in batch:
            if pid in results:
                prompt_text, domain = get_prompt_text(pid)
                r = results[pid]
                save_result(pid, domain, prompt_text, r["response"], r["usage"], r["session_id"])
                ok_count += 1
            else:
                err_count += 1

    print(f"\n[M7] Done - OK: {ok_count}, Errors: {err_count}")
    if ok_count > 0:
        print("Next: run src/metrics/run_pipeline.py to recompute metrics.")


if __name__ == "__main__":
    main()
