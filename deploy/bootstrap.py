#!/usr/bin/env python3
"""Trust-aware bootstrap for the self-deployable OKF environment (ADR-0005).

An interview, not a config dig. It asks -- and records, dated -- the deployment's TRUST
decisions before generating any config:

  1. Trusted dataset(s): which bundle(s) to serve, VALIDATED before use, and who vouches.
  2. Data-sensitivity / egress posture: -> selects the `no-egress` or `hosted` profile.
  3. Org structure / access: who counts as "leadership", and the access token that gates them.

It then writes deploy/.env (secrets, git-ignored), selects the compose profile + gateway
config, and emits deploy/deployment.manifest.md -- a dated provenance record of the trust
posture, so the deployment's trust decisions are written down, not tribal. Extending the
integrity ethos from notes to the deployment is the whole point.

Stdlib only. Run from the repo root:  python3 deploy/bootstrap.py
"""
from __future__ import annotations

import datetime
import getpass
import os
import secrets
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ENV_PATH = os.path.join(HERE, ".env")
MANIFEST_PATH = os.path.join(HERE, "deployment.manifest.md")
VALIDATE = os.path.join(REPO, "scripts", "validate.py")


# --- small prompt helpers ------------------------------------------------------------

def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        val = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        val = ""
    return val or default


def ask_yes(prompt: str, default_yes: bool = True) -> bool:
    d = "Y/n" if default_yes else "y/N"
    val = ask(f"{prompt} ({d})").lower()
    if not val:
        return default_yes
    return val.startswith("y")


def section(title: str):
    print(f"\n\033[1m== {title} ==\033[0m")


# --- steps ---------------------------------------------------------------------------

def collect_datasets() -> list[dict]:
    section("1. Trusted dataset(s)")
    print("Which knowledge bundle(s) should this deployment serve? Each is validated for OKF")
    print("conformance before use, and we record who vouches for it -- provenance of the corpus.")
    datasets = []
    default_path = os.path.join(REPO, "okf")
    while True:
        loc = ask("Bundle path or git URL", default_path if not datasets else "")
        if not loc:
            break
        is_git = loc.endswith(".git") or loc.startswith(("http://", "https://", "git@"))
        validated = "skipped (git URL -- clone & validate on the host)"
        if not is_git:
            path = os.path.abspath(loc)
            if not os.path.isdir(path):
                print(f"  ! not a directory: {path} -- skipping.")
                continue
            validated = run_validate(path)
        vouches = ask("Who vouches for this dataset's trustworthiness (name/role)")
        datasets.append({"location": loc, "is_git": is_git,
                         "validated": validated, "vouches": vouches or "(unrecorded)"})
        if not ask_yes("Add another dataset?", default_yes=False):
            break
    if not datasets:
        print("No dataset given -- defaulting to the local okf/ bundle.")
        datasets.append({"location": default_path, "is_git": False,
                         "validated": run_validate(default_path), "vouches": "(unrecorded)"})
    return datasets


def run_validate(path: str) -> str:
    if not os.path.isfile(VALIDATE):
        return "skipped (validator not found)"
    try:
        r = subprocess.run([sys.executable, VALIDATE, path],
                           capture_output=True, text=True, timeout=120)
    except Exception as e:  # noqa: BLE001
        return f"error running validator: {e}"
    ok = r.returncode == 0
    print(f"  {'✓' if ok else '✗'} OKF validation "
          f"{'passed' if ok else 'FAILED (exit %d)' % r.returncode} for {path}")
    if not ok:
        sys.stdout.write(r.stdout[-800:])
        if not ask_yes("  Validation failed -- serve this dataset anyway?", default_yes=False):
            print("  (recorded as failed; fix the bundle and re-run to serve it)")
    return "passed" if ok else f"FAILED (exit {r.returncode}) -- overridden by operator"


def collect_posture() -> str:
    section("2. Data sensitivity / egress posture")
    print("Can this project's knowledge be sent to an APPROVED external cloud model,")
    print("or must it NEVER leave this host?")
    print("  1) It must never leave the host        -> no-egress (all inference local)")
    print("  2) An approved cloud model is allowed  -> hosted (bring your own key)")
    choice = ask("Choose 1 or 2", "1")
    return "no-egress" if choice.strip() != "2" else "hosted"


def collect_hosted(env: dict):
    section("Approved cloud provider (hosted profile)")
    print("Edit deploy/gateway/litellm.hosted.yaml to point okf-chat-model / okf-stt-model /")
    print("okf-tts-model at the models your institution approved. Enter the keys they use:")
    if ask_yes("Set an Anthropic API key?", default_yes=True):
        env["ANTHROPIC_API_KEY"] = getpass.getpass("  ANTHROPIC_API_KEY (hidden): ").strip()
    if ask_yes("Set an OpenAI API key (used by the example audio models)?", default_yes=True):
        env["OPENAI_API_KEY"] = getpass.getpass("  OPENAI_API_KEY (hidden): ").strip()


def collect_no_egress(env: dict):
    section("Local models (no-egress profile)")
    env["OKF_WHISPER_MODEL"] = ask("Whisper STT model (tiny|base|small|medium|large-v3)", "base")
    print("After `docker compose --profile no-egress up`, pull the LLM once:")
    print("  docker compose exec ollama ollama pull llama3.1:8b-instruct")
    print("and make sure the model name in litellm.no-egress.yaml matches what you pulled.")


def collect_voice() -> bool:
    section("Voice")
    return ask_yes("Enable voice (speech in / spoken answers)?", default_yes=True)


def collect_access(env: dict) -> dict:
    section("3. Org structure / access")
    print("Who counts as 'leadership' -- i.e. who is this assistant for? (recorded as the")
    print("access boundary; SSO/TLS are a later hardening step.)")
    audience = ask("Intended audience / access boundary", "project leadership")
    if ask_yes("Generate an access token to gate the assistant? (strongly recommended)", True):
        token = secrets.token_urlsafe(24)
        env["OKF_CHAT_ACCESS_TOKEN"] = token
        print(f"  access token: {token}\n  (also saved in deploy/.env -- share it only with the audience above)")
    else:
        print("  ! No token -- the assistant will be OPEN to anyone who can reach the port.")
    return {"audience": audience, "token_set": bool(env.get("OKF_CHAT_ACCESS_TOKEN"))}


# --- writing -------------------------------------------------------------------------

def write_env(env: dict):
    lines = ["# deploy/.env -- generated by deploy/bootstrap.py. DO NOT COMMIT (secrets).",
             f"# generated {datetime.date.today().isoformat()}", ""]
    for k, v in env.items():
        lines.append(f"{k}={v}")
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(ENV_PATH, 0o600)
    print(f"\nwrote {ENV_PATH} (mode 600)")


def write_manifest(datasets, profile, voice_on, access, env):
    today = datetime.date.today().isoformat()
    ds_lines = []
    for d in datasets:
        ds_lines.append(f"- **{d['location']}**"
                        f"{' (git)' if d['is_git'] else ''} — validation: {d['validated']}; "
                        f"vouched by: {d['vouches']}")
    body = f"""# Deployment provenance manifest

> Generated by `deploy/bootstrap.py` on {today}. This records the **trust decisions** behind
> this deployment (ADR-0005). It is deployment provenance, not a bundle note; it may hold
> org-specific detail and is git-ignored by default. Keep it with the deployment.

## Trusted datasets

{chr(10).join(ds_lines)}

## Egress posture

- **Profile:** `{profile}` — {"all inference local; nothing leaves the host" if profile == "no-egress" else "gateway fronts an approved cloud model (data egresses to the vendor)"}.
- **Gateway config:** `deploy/gateway/{env['OKF_GATEWAY_CONFIG']}`.

## Access boundary

- **Intended audience:** {access['audience']}.
- **Access token set:** {"yes" if access['token_set'] else "NO — deployment is open"}.
- Hardening still owed (ADR-0005 phase 2): TLS termination and SSO/OIDC.

## Voice

- **Enabled:** {"yes" if voice_on else "no"}.

## Integrity note

The chosen model still has to clear the integrity bar (ADR-0003 phase-4 eval): a private but
weak model that launders `draft` support into confident fact is not acceptable. Privacy does
not substitute for the integrity behaviours.
"""
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"wrote {MANIFEST_PATH}")


def main() -> int:
    print("OKF knowledge assistant -- deployment bootstrap (ADR-0005)")
    print("Answers are recorded as deployment provenance. Ctrl-C to abort.\n")

    datasets = collect_datasets()
    profile = collect_posture()
    voice_on = collect_voice()

    key = "sk-" + secrets.token_urlsafe(18)
    env = {
        "OKF_COMPOSE_PROFILE": profile,
        "OKF_GATEWAY_CONFIG": "litellm.no-egress.yaml" if profile == "no-egress" else "litellm.hosted.yaml",
        "OKF_CHAT_PORT": ask("Port to serve on", "8080"),
        "OKF_CHAT_MODEL": "okf-chat-model",
        "OKF_CHAT_STT_MODEL": "okf-stt-model" if voice_on else "",
        "OKF_CHAT_TTS_MODEL": "okf-tts-model" if voice_on else "",
        "OKF_CHAT_TTS_VOICE": "alloy",
        "OKF_CHAT_TTS_FORMAT": "mp3",
        "OKF_CHAT_API_KEY": key,   # app -> gateway
        "MASTER_KEY": key,         # gateway master key (same value locally)
        "ANTHROPIC_API_KEY": "",
        "OPENAI_API_KEY": "",
        "OKF_WHISPER_MODEL": "base",
        "OKF_CHAT_ACCESS_TOKEN": "",
    }

    if profile == "hosted":
        collect_hosted(env)
    else:
        collect_no_egress(env)

    access = collect_access(env)

    write_env(env)
    write_manifest(datasets, profile, voice_on, access, env)

    section("Next steps")
    if profile == "no-egress":
        print("  cd deploy && docker compose --profile no-egress up --build")
        print("  # then pull the LLM:  docker compose exec ollama ollama pull llama3.1:8b-instruct")
    else:
        print("  # confirm deploy/gateway/litellm.hosted.yaml points at your approved models, then:")
        print("  cd deploy && docker compose up --build")
    port = env["OKF_CHAT_PORT"]
    print(f"  open http://localhost:{port}")
    if env.get("OKF_CHAT_ACCESS_TOKEN"):
        print("  paste the access token above into the token field.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\naborted -- nothing written.")
        raise SystemExit(130)
