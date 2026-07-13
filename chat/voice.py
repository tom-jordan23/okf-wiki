#!/usr/bin/env python3
"""Voice I/O for the leadership chat -- STT and TTS through the SAME gateway (ADR-0004).

ADR-0004 decision 2: speech is not a separate vendor. Speech-to-text and text-to-speech
are ordinary OpenAI-format calls to the same gateway the chat loop already uses --
``POST {base_url}/audio/transcriptions`` and ``POST {base_url}/audio/speech`` -- so audio
inherits the gateway's virtual-key spend tracking, provider abstraction, and (via a
self-hosted route) data-egress posture, exactly like chat. See okf/sources/0002-litellm.md
for the verified endpoint support.

This module adds only the audio transport plus the ``SPOKEN`` / ``PROVENANCE`` channel
split (decision 3). The agentic-navigation loop in ``agent.py`` is untouched: voice is a
transcribe-before / synthesize-after shell around it.

No third-party dependencies -- stdlib ``urllib`` only. Multipart/form-data for the audio
upload is built by hand below.
"""
from __future__ import annotations

import os
import re
import urllib.error
import urllib.request

from gateway import GatewayError

# Audio config lives alongside the chat config, reusing the same base_url / api_key so a
# single gateway serves chat + STT + TTS. Only the model aliases and TTS voice/format are
# voice-specific.
_DEFAULT_TTS_VOICE = "alloy"
_DEFAULT_TTS_FORMAT = "mp3"


class Voice:
    """Audio transport over the gateway's OpenAI-format ``/audio/*`` endpoints."""

    def __init__(self, base_url: str, api_key: str, *, stt_model: str, tts_model: str,
                 tts_voice: str = _DEFAULT_TTS_VOICE, tts_format: str = _DEFAULT_TTS_FORMAT,
                 timeout: float = 120.0):
        if not base_url:
            raise GatewayError("voice base_url is empty -- set OKF_CHAT_BASE_URL")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.stt_model = stt_model
        self.tts_model = tts_model
        self.tts_voice = tts_voice
        self.tts_format = tts_format
        self.timeout = timeout

    def _auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    def transcribe(self, audio: bytes, filename: str = "question.wav") -> str:
        """Speech -> text via POST {base_url}/audio/transcriptions (multipart/form-data)."""
        if not self.stt_model:
            raise GatewayError("no STT model -- set OKF_CHAT_STT_MODEL")
        body, content_type = _multipart(
            fields={"model": self.stt_model, "response_format": "text"},
            file_field="file", filename=filename, file_bytes=audio,
        )
        headers = {"Content-Type": content_type, **self._auth_headers()}
        req = urllib.request.Request(
            f"{self.base_url}/audio/transcriptions", data=body, headers=headers, method="POST"
        )
        raw = self._send(req)
        text = raw.decode("utf-8", errors="replace").strip()
        # response_format=text returns bare text; tolerate a JSON {"text": ...} too.
        if text.startswith("{"):
            import json
            try:
                return (json.loads(text).get("text") or "").strip()
            except json.JSONDecodeError:
                pass
        return text

    def synthesize(self, text: str) -> bytes:
        """Text -> audio bytes via POST {base_url}/audio/speech. Caller writes the file."""
        if not self.tts_model:
            raise GatewayError("no TTS model -- set OKF_CHAT_TTS_MODEL")
        import json
        payload = json.dumps({
            "model": self.tts_model,
            "input": text,
            "voice": self.tts_voice,
            "response_format": self.tts_format,
        }).encode("utf-8")
        headers = {"Content-Type": "application/json", **self._auth_headers()}
        req = urllib.request.Request(
            f"{self.base_url}/audio/speech", data=payload, headers=headers, method="POST"
        )
        return self._send(req)

    def _send(self, req) -> bytes:
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise GatewayError(f"gateway HTTP {e.code}: {body[:500]}") from e
        except urllib.error.URLError as e:
            raise GatewayError(
                f"cannot reach gateway at {self.base_url}: {e.reason}. "
                f"Is the proxy running / is OKF_CHAT_BASE_URL correct?"
            ) from e


def from_env() -> Voice:
    """Build a Voice from the same env as the chat gateway, plus audio-specific vars.

    Reuses OKF_CHAT_BASE_URL / OKF_CHAT_API_KEY (one gateway for chat + audio), and adds:
      OKF_CHAT_STT_MODEL, OKF_CHAT_TTS_MODEL, OKF_CHAT_TTS_VOICE, OKF_CHAT_TTS_FORMAT.
    """
    base_url = os.environ.get("OKF_CHAT_BASE_URL", "")
    if not base_url and (os.environ.get("OKF_CHAT_GATEWAY") or "internal") == "internal":
        base_url = "http://localhost:4000"
    return Voice(
        base_url=base_url,
        api_key=os.environ.get("OKF_CHAT_API_KEY", ""),
        stt_model=os.environ.get("OKF_CHAT_STT_MODEL", ""),
        tts_model=os.environ.get("OKF_CHAT_TTS_MODEL", ""),
        tts_voice=os.environ.get("OKF_CHAT_TTS_VOICE", _DEFAULT_TTS_VOICE),
        tts_format=os.environ.get("OKF_CHAT_TTS_FORMAT", _DEFAULT_TTS_FORMAT),
    )


# --- multipart/form-data (stdlib, no `requests`) -------------------------------------

def _multipart(fields: dict, file_field: str, filename: str, file_bytes: bytes):
    """Encode a multipart/form-data body. Returns (body_bytes, content_type_header)."""
    # A fixed boundary is fine: we control the payload and it does not appear in the data.
    boundary = "----okf-voice-boundary-7MA4YWxkTrZu0gW"
    crlf = b"\r\n"
    parts = []
    for name, value in fields.items():
        parts += [
            f"--{boundary}".encode(),
            f'Content-Disposition: form-data; name="{name}"'.encode(),
            b"", str(value).encode("utf-8"),
        ]
    parts += [
        f"--{boundary}".encode(),
        f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"'.encode(),
        b"Content-Type: application/octet-stream",
        b"", file_bytes,
        f"--{boundary}--".encode(), b"",
    ]
    body = crlf.join(parts)
    return body, f"multipart/form-data; boundary={boundary}"


# --- SPOKEN / PROVENANCE channel split (ADR-0004 decision 3) --------------------------

_SPOKEN_RX = re.compile(r"SPOKEN:\s*(.*?)(?:\n\s*PROVENANCE:|\Z)", re.IGNORECASE | re.DOTALL)
_PROV_RX = re.compile(r"PROVENANCE:\s*(.*)\Z", re.IGNORECASE | re.DOTALL)
# A path-like token ending in .md -- the same shape run_poc.py checks, used here to catch
# a raw citation leaking into the SPOKEN (heard) channel, which decision 3 forbids.
_MD_PATH_RX = re.compile(r"(?<![\w/])((?:[\w.-]+/)*[\w.-]+\.md)")


def split_channels(answer_text: str) -> tuple[str, str]:
    """Split a voice-mode answer into (spoken, provenance).

    Falls back gracefully if the model omitted the headings: with no SPOKEN heading the
    whole text is treated as spoken (and will fail the leak check if it contains paths),
    which is the honest, visible failure we want -- not a silent pass.
    """
    text = answer_text or ""
    sm = _SPOKEN_RX.search(text)
    pm = _PROV_RX.search(text)
    spoken = sm.group(1).strip() if sm else text.strip()
    provenance = pm.group(1).strip() if pm else ""
    return spoken, provenance


def leaked_paths(spoken: str) -> list[str]:
    """Return any bundle path tokens that leaked into the spoken (heard) channel."""
    seen = []
    for m in _MD_PATH_RX.findall(spoken or ""):
        if m not in seen:
            seen.append(m)
    return seen
