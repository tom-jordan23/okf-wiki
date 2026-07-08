#!/usr/bin/env python3
"""Provider-agnostic gateway client for the leadership-chat POC.

ADR-0003 decision 3: the app talks only to a **gateway's OpenAI-format API**, never a
provider SDK. That gateway is an *interface*, not a specific instance -- it can be:

- **internal**  : a LiteLLM proxy we self-host (see ``gateways/internal.litellm.yaml``),
                  the interim option while the platform team's service is in progress; or
- **external**  : the platform team's shared LiteLLM + MCP AI gateway (or any other
                  OpenAI-compatible endpoint).

Both speak the same ``POST {base_url}/chat/completions`` contract, so switching between
them is *configuration, not code* -- exactly the portability ADR-0003 asks for. This
client is identical for either; only ``base_url`` / ``api_key`` / ``model`` change.

Configuration is read from the environment (keeps secrets out of the repo -- see the
hardened .gitignore). A ``.env``-style file per profile can be loaded via ``--env-file``.

No third-party dependencies -- stdlib ``urllib`` only.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

# Profile -> the env var prefix and its documented defaults. Both profiles use the SAME
# variable names with a profile prefix, so a deployment sets exactly one profile's vars.
_PROFILES = {
    "internal": {
        # Sensible default for a locally-run LiteLLM proxy (`litellm --config ...`).
        "default_base_url": "http://localhost:4000",
    },
    "external": {
        # No default endpoint -- the platform team's gateway URL must be provided.
        "default_base_url": "",
    },
}


class GatewayError(RuntimeError):
    pass


class Gateway:
    """A thin OpenAI-format chat/completions caller."""

    def __init__(self, base_url: str, api_key: str, model: str, *, timeout: float = 120.0):
        if not base_url:
            raise GatewayError("gateway base_url is empty -- set OKF_CHAT_BASE_URL")
        if not model:
            raise GatewayError("gateway model is empty -- set OKF_CHAT_MODEL")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def chat(self, messages: list, tools: list | None = None,
             tool_choice: str = "auto") -> dict:
        """One chat/completions round-trip. Returns the parsed JSON response.

        Raises GatewayError on transport/HTTP errors so the caller can report cleanly.
        """
        payload = {"model": self.model, "messages": messages}
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions", data=data, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise GatewayError(f"gateway HTTP {e.code}: {body[:500]}") from e
        except urllib.error.URLError as e:
            raise GatewayError(
                f"cannot reach gateway at {self.base_url}: {e.reason}. "
                f"Is the proxy running / is OKF_CHAT_BASE_URL correct?"
            ) from e


def load_env_file(path: str) -> None:
    """Load simple KEY=VALUE lines into os.environ (does not overwrite existing vars).

    Minimal .env reader: ignores blanks and #comments, strips optional surrounding
    quotes. No third-party dotenv dependency.
    """
    if not path or not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            os.environ.setdefault(key, val)


def from_env(profile: str | None = None) -> Gateway:
    """Build a Gateway from environment variables.

    Precedence for each of base_url / api_key / model:
      1. OKF_CHAT_BASE_URL / OKF_CHAT_API_KEY / OKF_CHAT_MODEL   (explicit, wins)
      2. the selected profile's documented default (base_url only)

    ``profile`` comes from the arg, else OKF_CHAT_GATEWAY, else 'internal'.
    """
    profile = (profile or os.environ.get("OKF_CHAT_GATEWAY") or "internal").lower()
    if profile not in _PROFILES:
        raise GatewayError(
            f"unknown gateway profile {profile!r}; expected one of {sorted(_PROFILES)}"
        )
    base_url = os.environ.get("OKF_CHAT_BASE_URL") or _PROFILES[profile]["default_base_url"]
    api_key = os.environ.get("OKF_CHAT_API_KEY", "")
    model = os.environ.get("OKF_CHAT_MODEL", "")
    return Gateway(base_url=base_url, api_key=api_key, model=model)


if __name__ == "__main__":
    # Print the resolved config (never the key) for the current environment.
    prof = os.environ.get("OKF_CHAT_GATEWAY", "internal")
    try:
        gw = from_env(prof)
        print(f"profile={prof}  base_url={gw.base_url}  model={gw.model}  "
              f"api_key={'set' if gw.api_key else 'MISSING'}")
    except GatewayError as e:
        print(f"config error: {e}")
