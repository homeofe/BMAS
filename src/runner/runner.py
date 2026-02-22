"""
BMAS Runner - Blind Multi-Agent Synthesis prompt runner.

Sends identical prompts to multiple models in strict isolation via OpenClaw.
Each model runs in a separate isolated cron session - no cross-contamination.

Usage:
    # Dry run (validate config, no API calls)
    python runner.py --prompt-id A01 --domain technical --dry-run

    # Run one prompt against all 5 models
    python runner.py --prompt-id A01 --domain technical \
        --prompt "What is the CVSS 3.1 base score for CVE-2024-21762?"

    # Run one prompt against specific models
    python runner.py --prompt-id A01 --domain technical \
        --prompt "..." --models M1 M3

    # Run full pilot (A01, A05, B01, B05, C01)
    python runner.py --pilot

    # Run all 30 prompts
    python runner.py --all
"""

import argparse
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------

MODELS = {
    # --- Original 5 models ---
    "M1":  {"id": "M1",  "name": "claude-sonnet-4-6",       "model_string": "anthropic/claude-sonnet-4-6"},
    "M2":  {"id": "M2",  "name": "claude-opus-4-6",         "model_string": "anthropic/claude-opus-4-6"},
    "M3":  {"id": "M3",  "name": "gpt-5.3-codex",           "model_string": "openai-codex/gpt-5.3-codex"},
    "M4":  {"id": "M4",  "name": "gemini-2.5-pro",          "model_string": "google-gemini-cli/gemini-2.5-pro"},
    "M5":  {"id": "M5",  "name": "sonar-pro",               "model_string": "perplexity/sonar-pro"},
    # --- Extended model set (all configured models) ---
    "M6":  {"id": "M6",  "name": "sonar-deep-research",     "model_string": "perplexity/sonar-deep-research",     "timeout_override": 300},
    "M7":  {"id": "M7",  "name": "gemini-3-pro-preview",   "model_string": "google-gemini-cli/gemini-3-pro-preview"},
    "M8":  {"id": "M8",  "name": "gemini-3-flash-preview", "model_string": "google-gemini-cli/gemini-3-flash-preview"},
    "M9":  {"id": "M9",  "name": "gemini-2.5-flash",        "model_string": "google-gemini-cli/gemini-2.5-flash"},
    "M10": {"id": "M10", "name": "gpt-5.2",                 "model_string": "openai-codex/gpt-5.2"},
    "M11": {"id": "M11", "name": "gpt-5.1",                 "model_string": "openai-codex/gpt-5.1"},
    "M12": {"id": "M12", "name": "claude-sonnet-4-5",       "model_string": "anthropic/claude-sonnet-4-5"},
}

ALL_MODEL_IDS = list(MODELS.keys())

# ---------------------------------------------------------------------------
# Isolation prompt - neutral, no hints about other models or study
# ---------------------------------------------------------------------------

ISOLATION_SYSTEM_PREFIX = (
    "You are a knowledgeable expert assistant. "
    "Answer the following question as accurately and completely as possible. "
    "Be precise, factual, and structured. "
    "If you are uncertain about any specific detail, state that explicitly."
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
BMAS_DIR     = Path(__file__).resolve().parent.parent.parent
RAW_OUTPUTS  = BMAS_DIR / "experiments" / "raw-outputs"
PROMPTS_DIR  = BMAS_DIR / "experiments" / "prompts"


# ---------------------------------------------------------------------------
# OpenClaw cron runner
# ---------------------------------------------------------------------------

def _openclaw(args: list[str], capture: bool = True) -> str:
    """Run openclaw CLI command, return stdout."""
    result = subprocess.run(
        ["openclaw"] + args,
        capture_output=capture,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"openclaw {' '.join(args[:3])} failed: {result.stderr.strip()}"
        )
    return result.stdout.strip() if capture else ""


def _create_isolated_job(
    prompt_id: str,
    model_id: str,
    prompt_text: str,
    timeout_seconds: int = 120,
) -> str:
    """Create an isolated cron job for one model. Returns job id."""
    model = MODELS[model_id]
    # Per-model timeout override (e.g. sonar-deep-research needs more time)
    effective_timeout = model.get("timeout_override", timeout_seconds)
    # Prepend isolation system prefix to the prompt
    full_message = f"{ISOLATION_SYSTEM_PREFIX}\n\n{prompt_text}"

    raw = _openclaw([
        "cron", "add",
        "--name",    f"bmas-{prompt_id}-{model_id}",
        "--session", "isolated",
        "--model",   model["model_string"],
        "--message", full_message,
        "--no-deliver",
        "--timeout-seconds", str(effective_timeout),
        "--at",      "2m",
        "--delete-after-run",
        "--json",
    ])
    data = json.loads(raw)
    return data["id"]


def _trigger_job(job_id: str, timeout_ms: int = 180_000) -> None:
    """Force-run a cron job immediately."""
    _openclaw(["cron", "run", job_id, "--timeout", str(timeout_ms)])


def _wait_for_job(job_id: str, poll_interval: float = 3.0, max_wait: float = 180.0) -> dict:
    """
    Poll cron runs until the job finishes. Returns the run entry dict.
    Raises RuntimeError on timeout or job failure.
    """
    deadline = time.time() + max_wait
    while time.time() < deadline:
        raw = _openclaw(["cron", "runs", "--id", job_id])
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            time.sleep(poll_interval)
            continue

        entries = data.get("entries", [])
        for entry in entries:
            if entry.get("action") == "finished":
                if entry.get("status") == "ok":
                    return entry
                else:
                    raise RuntimeError(
                        f"Job {job_id} failed with status: {entry.get('status')}"
                    )
        time.sleep(poll_interval)

    raise TimeoutError(f"Job {job_id} did not finish within {max_wait}s")


def _get_full_response_from_session(session_id: str) -> str:
    """
    Read the full assistant text response from the session JSONL file.
    Falls back to summary if session file not found.
    """
    session_file = SESSIONS_DIR / f"{session_id}.jsonl"
    if not session_file.exists():
        return ""

    texts = []
    with open(session_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            if event.get("type") == "message":
                msg = event.get("message", {})
                if msg.get("role") == "assistant":
                    content = msg.get("content", [])
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                texts.append(block["text"])
                    elif isinstance(content, str):
                        texts.append(content)

    return "\n".join(texts)


# ---------------------------------------------------------------------------
# Core run function
# ---------------------------------------------------------------------------

def run_prompt_blind(
    prompt_id: str,
    prompt_text: str,
    domain: str,
    model_ids: list[str],
    output_dir: Path,
    dry_run: bool = False,
    timeout_seconds: int = 120,
) -> list[dict]:
    """
    Run a single prompt against all specified models in isolation.
    Saves one JSON file per model: output_dir/<prompt_id>/<model_id>.json
    Returns list of run records.
    """
    print(f"\n[BMAS] Prompt {prompt_id} ({domain}) x {len(model_ids)} models")
    results = []

    for model_id in model_ids:
        model = MODELS[model_id]
        print(f"  -> {model_id} ({model['name']})... ", end="", flush=True)
        start = time.time()

        if dry_run:
            record = {
                "run_id":          f"{prompt_id}-{model_id}-dry",
                "bmas_version":    "1.0",
                "prompt_id":       prompt_id,
                "model_id":        model_id,
                "model":           model["model_string"],
                "domain":          domain,
                "prompt":          prompt_text,
                "response":        "[DRY RUN]",
                "response_tokens": 0,
                "latency_ms":      0,
                "timestamp":       datetime.now(timezone.utc).isoformat(),
            }
            _save_record(output_dir, record)
            results.append(record)
            print("DRY RUN")
            continue

        try:
            effective_timeout = model.get("timeout_override", timeout_seconds)
            job_id = _create_isolated_job(prompt_id, model_id, prompt_text, timeout_seconds)
            _trigger_job(job_id, timeout_ms=(effective_timeout + 60) * 1000)
            run_entry = _wait_for_job(job_id, max_wait=float(effective_timeout) + 60)

            session_id = run_entry.get("sessionId", "")
            response = _get_full_response_from_session(session_id)

            # Fall back to summary if session file not accessible
            if not response:
                response = run_entry.get("summary", "")

            usage = run_entry.get("usage", {})
            latency = int((time.time() - start) * 1000)

            record = {
                "run_id":          f"{prompt_id}-{model_id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "bmas_version":    "1.0",
                "prompt_id":       prompt_id,
                "model_id":        model_id,
                "model":           model["model_string"],
                "domain":          domain,
                "prompt":          prompt_text,
                "response":        response,
                "response_tokens": usage.get("output_tokens", 0),
                "input_tokens":    usage.get("input_tokens", 0),
                "latency_ms":      latency,
                "job_id":          job_id,
                "session_id":      session_id,
                "timestamp":       datetime.now(timezone.utc).isoformat(),
            }
            _save_record(output_dir, record)
            results.append(record)
            print(f"OK ({record['response_tokens']} tokens, {latency}ms)")

        except (RuntimeError, TimeoutError) as e:
            print(f"FAILED: {e}")
            results.append({
                "run_id":      f"{prompt_id}-{model_id}-error",
                "prompt_id":   prompt_id,
                "model_id":    model_id,
                "error":       str(e),
                "timestamp":   datetime.now(timezone.utc).isoformat(),
            })

    return results


def _save_record(output_dir: Path, record: dict) -> Path:
    prompt_dir = output_dir / record["prompt_id"]
    prompt_dir.mkdir(parents=True, exist_ok=True)
    out_path = prompt_dir / f"{record['model_id']}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    return out_path


# ---------------------------------------------------------------------------
# Prompt loader
# ---------------------------------------------------------------------------

DOMAIN_A_PROMPTS = {
    "A01": ("technical", "What is the CVSS 3.1 base score for CVE-2024-21762 (Fortinet FortiOS out-of-bounds write vulnerability)? State the score, the vector string, and explain the rationale for each base metric component (AV, AC, PR, UI, S, C, I, A)."),

    "A02": ("technical", "Compare ML-KEM-768 and ML-DSA-65 (FIPS 203 and FIPS 204) on the following dimensions: (1) primary use case, (2) key sizes in bytes, (3) signature/ciphertext size, (4) security level in bits. Present results in a structured format."),
    "A03": ("technical", "For TLS 1.3, list all standardized cipher suites defined in RFC 8446. For each, state: the AEAD algorithm, the hash function, and the key exchange group(s) it is compatible with. Which of these is recommended for post-quantum readiness and why?"),
    "A04": ("technical", "SHA-3-256 and BLAKE3 are both modern cryptographic hash functions. Compare them on: (1) standardization status, (2) output size, (3) construction (sponge vs. Merkle-Damgard variant), (4) performance on modern CPUs, (5) known weaknesses or attack surface. Which is preferred for a new high-security application and why?"),
    "A05": ("technical", "Describe the complete OpenID for Verifiable Presentations (OID4VP) protocol flow for a cross-device presentation scenario. Include: all involved parties, the role of the presentation_definition, how the response_uri is used, and what SD-JWT VC format looks like at the protocol level."),
    "A06": ("technical", "According to the EU eIDAS 2.0 regulation (Regulation 2024/1183), what are the mandatory components of an EU Digital Identity Wallet (EUDIW)? List the required technical functions and the assurance level requirements."),
    "A07": ("technical", "Explain the Learning With Errors (LWE) problem and how it underpins the security of ML-KEM. What is the assumed computational hardness, and what class of attacker (classical vs. quantum) is it secure against?"),
    "A08": ("technical", "CVSS v4.0 was released in November 2023. What are the three most significant structural changes compared to CVSS v3.1? For each change, explain the motivation and the practical impact on vulnerability scoring."),
    "A09": ("technical", "In the SD-JWT format (IETF RFC 9901), how does a holder selectively disclose claims to a verifier without revealing the full credential? Describe the cryptographic mechanism, including the role of salts, the disclosure objects, and the _sd array."),
    "A10": ("technical", "According to BSI Technical Guideline TR-03116 Part 4 (eCard-API), what are the currently approved symmetric encryption algorithms and minimum key lengths for protecting sensitive personal data in German government systems?"),
    # --- Extended prompt set (v2 expansion) ---
    "A11": ("technical", "Explain the DNSSEC validation chain from root to leaf. What is the role of the DNSKEY, RRSIG, DS, and NSEC/NSEC3 record types? Describe a zone-signing walk-through and identify the two most critical points of failure in a DNSSEC deployment."),
    "A12": ("technical", "Describe the Kubernetes RBAC model: how do Roles, ClusterRoles, RoleBindings, and ClusterRoleBindings interact? List the top 5 RBAC misconfigurations that lead to privilege escalation, and explain the attack path for each."),
    "A13": ("technical", "Describe the OAuth 2.0 Authorization Code Flow with PKCE (Proof Key for Code Exchange). What problem does PKCE solve compared to the original Authorization Code Flow? What are the exact cryptographic operations involved, and what attacks does it prevent?"),
    "A14": ("technical", "Explain the FIDO2/WebAuthn credential creation and authentication ceremonies step by step. What cryptographic primitives are used? How does the authenticator attest to its identity, and what is the role of the AAGUID and attestation certificate?"),
    "A15": ("technical", "Compare Fully Homomorphic Encryption (FHE) and Partially Homomorphic Encryption (PHE). What operations does each support? Name two production-ready FHE libraries and one real-world use case where FHE is currently deployed. What are the primary performance constraints preventing wider adoption?"),
}

DOMAIN_B_PROMPTS = {
    "B01": ("regulatory", "Under GDPR Article 17(3), under which conditions can a controller refuse a data subject's request for erasure? List all valid legal bases defined in the article and provide a one-sentence explanation for each."),
    "B02": ("regulatory", "What distinguishes TISAX Assessment Level 3 (AL3) from AL2? What additional controls or assessment requirements apply at AL3, and for what type of information is AL3 relevant?"),
    "B03": ("regulatory", "The BSI Cloud Computing Compliance Criteria Catalogue (C5) defines a set of requirements for cloud service providers. Which of the 17 C5 domains is specifically concerned with encryption and key management, and what are the core requirements in that domain?"),
    "B04": ("regulatory", "ISO 27001:2022 introduced significant changes compared to ISO 27001:2013. What are the three most impactful changes to Annex A controls? For each, describe what was changed and the practical compliance implication."),
    "B05": ("regulatory", "Under GDPR Article 33, when must a personal data breach be notified to the supervisory authority? What is the exact time limit, when does the clock start, and under what conditions is notification not required?"),
    "B06": ("regulatory", "What are the three most significant legal and technical changes that eIDAS 2.0 (Regulation 2024/1183) introduces compared to the original eIDAS regulation (Regulation 910/2014)?"),
    "B07": ("regulatory", "Under GDPR, what distinguishes a data controller from a data processor? Can a single entity be both simultaneously for the same data? Cite the relevant GDPR articles."),
    "B08": ("regulatory", "The NIS2 Directive (EU) 2022/2555 defines 'essential entities' and 'important entities.' What criteria determine whether an organization falls into each category? List the sectors explicitly named in Annexes I and II."),
    "B09": ("regulatory", "Under GDPR Article 35, when is a Data Protection Impact Assessment (DPIA) mandatory? List all conditions that trigger the DPIA requirement and cite any relevant EDPB guidance on high-risk processing."),
    "B10": ("regulatory", "Compare SOC 2 Type II and ISO 27001 on the following dimensions: (1) issuing body, (2) what is certified, (3) audit frequency, (4) public availability of the report, (5) geographic adoption. Which is more appropriate for a European cloud service provider targeting enterprise customers in the EU and US?"),
    # --- Extended prompt set (v2 expansion) ---
    "B11": ("regulatory", "DORA (Digital Operational Resilience Act, EU 2022/2554) applies to financial entities from January 2025. What are the five ICT risk management pillars defined in DORA? For each pillar, state the core obligation and name one specific technical or organizational control required."),
    "B12": ("regulatory", "The EU AI Act (Regulation 2024/1689) defines four risk categories for AI systems. List all four, provide two examples of AI applications that fall into each category, and explain the compliance obligations for 'high-risk' systems specifically."),
    "B13": ("regulatory", "PCI DSS v4.0 was released in March 2022 with a transition deadline of March 2024. What are the three most significant changes compared to PCI DSS v3.2.1? For each, describe the change and its practical impact on a cardholder data environment."),
    "B14": ("regulatory", "An EU-based company processes health data for US clients under both GDPR and HIPAA. What are the three most critical structural differences between GDPR and HIPAA that affect this company's data processing agreements, breach notification timelines, and patient rights obligations?"),
    "B15": ("regulatory", "The EU Cyber Resilience Act (CRA, proposed 2022, final 2024) introduces mandatory cybersecurity requirements for products with digital elements. What are the essential cybersecurity requirements manufacturers must meet? What are the reporting obligations for actively exploited vulnerabilities, and what are the market access consequences for non-compliance?"),
}

DOMAIN_C_PROMPTS = {
    "C01": ("strategic", "For a zero-trust architecture handling cross-border EU government identity verification, should the orchestration layer be implemented as an event-driven microservice mesh or a stateless API gateway chain? The system processes ~10,000 identity verifications per day across 5 EU member states, with GDPR and eIDAS 2.0 compliance requirements. Justify your recommendation."),
    "C02": ("strategic", "An enterprise with a 10-year IT infrastructure lifespan is planning a post-quantum cryptography migration. Given that NIST finalized ML-KEM (FIPS 203) and ML-DSA (FIPS 204) in 2024, what should the migration priority order be across these systems: (1) TLS termination, (2) code signing, (3) data-at-rest encryption, (4) email encryption, (5) VPN tunnels? Justify each priority decision."),
    "C03": ("strategic", "An organization with 200 employees, one IT administrator, and a budget of 80,000 EUR/year for security tooling is evaluating whether to deploy an open-source SIEM (e.g., Wazuh, OpenSearch) or a commercial cloud SIEM (e.g., Microsoft Sentinel, Elastic SIEM). What is your recommendation? Consider: operational overhead, detection quality, compliance reporting, and total cost of ownership."),
    "C04": ("strategic", "A team of 4 engineers is building a regulatory compliance data platform that must meet GDPR and ISO 27001 requirements. The platform needs to store, process, and report on personal data for 500 enterprise clients. Should they start with a microservice architecture or a well-structured monolith? What are the top 3 risks of each approach in this specific regulatory context?"),
    "C05": ("strategic", "During a security incident, your threat intelligence indicates an attacker has established persistence in your network but has not yet exfiltrated data. You have two options: (A) immediately isolate affected systems, risking operational disruption and alerting the attacker; or (B) monitor silently to gather full attack chain intelligence, accepting the risk of ongoing access. Which approach do you recommend and under what conditions would you switch strategies?"),
    "C06": ("strategic", "Should a Security Operations Center (SOC) with 5 analysts use AI/LLM-based tools for alert triage and first-line investigation? List the top 3 benefits and top 3 risks. Given those, what is your overall recommendation and what governance controls are mandatory before deployment?"),
    "C07": ("strategic", "An IT leader has 200,000 EUR to invest in security for a mid-sized company. Option A: achieve ISO 27001 certification (estimated cost: 150,000 EUR including consultant + audit). Option B: invest the full amount in technical security controls (EDR, SIEM, PAM, vulnerability management). From a risk reduction perspective, which investment produces better outcomes in years 1-3? Justify with reasoning."),
    "C08": ("strategic", "You are designing an identity federation for 5 European government agencies that need to accept each other's credentials. The options are: (A) centralized identity broker, (B) peer-to-peer federation using SAML/OIDC trust anchors, or (C) self-sovereign identity with verifiable credentials (eIDAS 2.0 EUDIW). Each agency has 50,000 citizens. Which architecture do you recommend and why? What are the top failure modes of your chosen approach?"),
    "C09": ("strategic", "An organization runs annual phishing simulations and security awareness training. The CISO argues this is ineffective and wants to redirect the budget (40,000 EUR/year) to technical controls (email filtering, browser isolation). The HR director argues training is a compliance requirement and builds culture. Who is right? Present both arguments and give your verdict with reasoning."),
    "C10": ("strategic", "Can open-source LLMs (e.g., Llama 3, Mistral) be deployed in a GDPR-compliant environment for processing personal data, assuming the model runs fully on-premises with no external API calls? What are the three key compliance requirements that must be addressed, and what is the most critical technical control needed?"),
    # --- Extended prompt set (v2 expansion) ---
    "C11": ("strategic", "A mid-sized European company is evaluating whether to migrate its remaining on-premises workloads to an EU-based sovereign cloud (e.g., OVHcloud, IONOS, T-Systems) or to a hyperscaler with EU data residency guarantees (e.g., AWS EU Sovereign Cloud, Microsoft EU Data Boundary). What are the top 3 decision criteria that should determine the choice, and what is the single biggest risk of each option?"),
    "C12": ("strategic", "Should a security program be primarily risk-based or compliance-based? A CISO argues that chasing certifications (ISO 27001, TISAX) consumes resources without reducing actual risk. A CFO argues that certifications are required to win enterprise contracts. Present both sides and give your verdict: how should a mature security organization balance the two approaches?"),
    "C13": ("strategic", "An organization with 50,000 endpoints and a 3-person patch management team receives 200 CVEs per month. They cannot patch everything immediately. Design a prioritization framework that goes beyond raw CVSS scores. What are the top 5 factors to consider, and how should they be weighted relative to each other?"),
    "C14": ("strategic", "A 5,000-person organization is deciding between a centralized security team (one CISO, central SOC, central GRC) vs. a federated model (embedded security leads in each business unit, light central coordination). What are the top 3 advantages and disadvantages of each model? Which structure is more appropriate for a regulated industry (e.g., financial services), and why?"),
    "C15": ("strategic", "A SOC manager needs to measure the effectiveness of their security operations center. Propose the 5 most meaningful KPIs, explaining what each measures, why it matters, and what a 'good' vs. 'bad' benchmark looks like. Avoid vanity metrics (e.g., total alerts processed) and focus on metrics that reflect actual risk reduction and operational quality."),
}

ALL_PROMPTS: dict[str, tuple[str, str]] = {
    **DOMAIN_A_PROMPTS,
    **DOMAIN_B_PROMPTS,
    **DOMAIN_C_PROMPTS,
}

PILOT_PROMPTS = ["A01", "A05", "B01", "B05", "C01"]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="BMAS Blind Multi-Agent Prompt Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--pilot",    action="store_true", help="Run pilot set (A01, A05, B01, B05, C01)")
    mode.add_argument("--all",      action="store_true", help="Run all 30 prompts")
    mode.add_argument("--prompt-id", help="Single prompt ID (e.g. A01, B05)")

    parser.add_argument("--prompt",    help="Prompt text (required with --prompt-id)")
    parser.add_argument("--domain",    choices=["technical", "regulatory", "strategic"],
                        help="Domain (required with --prompt-id)")
    parser.add_argument("--models",    nargs="+", default=ALL_MODEL_IDS,
                        help="Model IDs (default: all M1-M5)")
    parser.add_argument("--output-dir", default=str(RAW_OUTPUTS))
    parser.add_argument("--timeout",   type=int, default=120,
                        help="Per-model timeout in seconds (default: 120)")
    parser.add_argument("--dry-run",      action="store_true",
                        help="Validate config without making API calls")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip prompt/model pairs that already have a saved JSON result")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build list of (prompt_id, domain, prompt_text) to run
    runs: list[tuple[str, str, str]] = []

    if args.pilot:
        for pid in PILOT_PROMPTS:
            domain, text = ALL_PROMPTS[pid]
            runs.append((pid, domain, text))
    elif args.all:
        for pid, (domain, text) in ALL_PROMPTS.items():
            runs.append((pid, domain, text))
    elif args.prompt_id:
        if args.prompt and args.domain:
            runs.append((args.prompt_id, args.domain, args.prompt))
        elif args.prompt_id in ALL_PROMPTS:
            domain, text = ALL_PROMPTS[args.prompt_id]
            runs.append((args.prompt_id, domain, text))
        else:
            parser.error(f"Unknown prompt ID '{args.prompt_id}' and no --prompt/--domain provided")
    else:
        parser.print_help()
        return

    print(f"[BMAS] Runner starting")
    print(f"  Prompts   : {len(runs)}")
    print(f"  Models    : {args.models}")
    print(f"  Dry run   : {args.dry_run}")
    print(f"  Output    : {output_dir}")
    print(f"  Timeout   : {args.timeout}s per model")
    print()

    total_ok = 0
    total_err = 0

    for prompt_id, domain, prompt_text in runs:
        # Apply --skip-existing filter per model
        model_ids_to_run = args.models
        if args.skip_existing:
            model_ids_to_run = [
                mid for mid in args.models
                if not (output_dir / prompt_id / f"{mid}.json").exists()
            ]
            skipped = set(args.models) - set(model_ids_to_run)
            if skipped:
                print(f"  [skip] {prompt_id}: {', '.join(sorted(skipped))} already done")
            if not model_ids_to_run:
                total_ok += len(skipped)
                continue

        records = run_prompt_blind(
            prompt_id=prompt_id,
            prompt_text=prompt_text,
            domain=domain,
            model_ids=model_ids_to_run,
            output_dir=output_dir,
            dry_run=args.dry_run,
            timeout_seconds=args.timeout,
        )
        for r in records:
            if "error" in r:
                total_err += 1
            else:
                total_ok += 1

    print(f"\n[BMAS] Done. OK: {total_ok}  Errors: {total_err}")


if __name__ == "__main__":
    main()
