# Self-deployable OKF knowledge assistant (ADR-0005)

One command brings up the **dataset**, the **gateway**, and the **chat + voice** app as a
single environment. Two egress profiles, chosen by an interactive bootstrap that records
what the deployment trusts. See
[ADR-0005](../okf/decisions/0005-self-deployable-environment.md) and the
[deploy runbook](../okf/runbooks/deploy-self-hosted.md).

## Quick start

```sh
python3 deploy/bootstrap.py         # interview: trusted datasets, egress posture, access
cd deploy
docker compose up --build           # hosted profile (approved cloud model, BYO key)
#   ...or, for the fully-local profile:
docker compose --profile no-egress up --build
open http://localhost:8080
```

The bootstrap writes `deploy/.env` (secrets, git-ignored) and
`deploy/deployment.manifest.md` (a dated record of the trust posture).

## The two profiles

| | **hosted** | **no-egress** |
|---|---|---|
| LLM / STT / TTS | approved **cloud** endpoints, BYO key | **local**: Ollama + self-hosted Whisper + Kokoro |
| Data leaves host? | yes (to the vendor) | **no** — nothing leaves |
| Footprint | small, fast | large (weights, hardware) |
| Gateway config | `gateway/litellm.hosted.yaml` | `gateway/litellm.no-egress.yaml` |
| Command | `docker compose up` | `docker compose --profile no-egress up` |

The app only ever talks to the **gateway** (ADR-0003) — it holds no keys and no provider
SDK — so choosing a profile is a config swap, never a code change.

## Services

- **app** — the stdlib web/voice server (`chat/server.py`); serves the UI and proxies the
  loop. Mounts the bundle **read-only** (`../okf` → `/data/okf`); refresh with `git pull`.
- **gateway** — [LiteLLM](https://github.com/BerriAI/litellm) (`ghcr.io/berriai/litellm`,
  pin a release). The one place model choice, keys, and spend live.
- **ollama / whisper / kokoro** *(no-egress only)* — local OpenAI-format LLM / STT / TTS.
  Confirm the STT/TTS image ports against each image's docs and match them in
  `docker-compose.yml` + `gateway/litellm.no-egress.yaml`.

## Notes

- **Access:** the bootstrap sets `OKF_CHAT_ACCESS_TOKEN`; the app requires it on every API
  call. TLS + SSO are ADR-0005 phase 2 — put this behind a reverse proxy before exposing it.
- **Secrets:** live only in `deploy/.env` (mode 600, git-ignored). Never commit them.
- **No app dependencies:** the image is stdlib-only Python — nothing to `pip install`.
- Try the app logic without Docker first: `python3 chat/run_voice_poc.py --dry-run`.
