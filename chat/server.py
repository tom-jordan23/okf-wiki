#!/usr/bin/env python3
"""Thin web + voice service over the OKF bundle (ADR-0003/0004 phase 2, ADR-0005).

A minimal HTTP server that makes the *proven* agentic-navigation loop servable in a
browser: text chat, push-to-talk voice, and the `PROVENANCE` channel shown on screen next
to the spoken answer. It reuses ``agent.py`` / ``navigator.py`` / ``gateway.py`` /
``voice.py`` **unchanged** -- the server is transport only. It holds no provider SDK and no
model keys; like the rest of the app it talks *only* to the gateway (ADR-0003 decision 3).

Endpoints:
  GET  /                     -> the single-page UI (chat + push-to-talk)
  GET  /api/health           -> {ok, voice_enabled, model}
  POST /api/ask   {question} -> {spoken, provenance, citations, files_read}
  POST /api/transcribe  (raw audio body) -> {text}      [voice profile only]
  POST /api/speak {text}     -> audio bytes             [voice profile only]

Auth: if OKF_CHAT_ACCESS_TOKEN is set, every /api/* call must send
``Authorization: Bearer <token>``. This is the deployment access floor (who counts as
"leadership", ADR-0003 open question); TLS + SSO are ADR-0005 phase 2. If the token is
unset the server runs open and says so loudly at startup -- fine for a laptop, not for a
real audience.

Stdlib only (``http.server``); no third-party dependencies.
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import agent
import voice as voice_mod
from gateway import GatewayError, from_env as gateway_from_env
from navigator import Navigator
from run_voice_poc import voice_system_prompt
from run_poc import check_citations, extract_citations

HERE = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(HERE, "web")
_MAX_BODY = 25 * 1024 * 1024  # 25 MB cap (audio uploads); refuse anything larger.


class App:
    """Process-wide singletons: the read-only bundle, the gateway, optional voice."""

    def __init__(self):
        bundle = os.environ.get("OKF_BUNDLE") or os.path.join(HERE, os.pardir, "okf")
        self.nav = Navigator(bundle)
        self.system_prompt = voice_system_prompt()  # always two-channel: works for text too
        self.gateway = gateway_from_env()
        self.access_token = os.environ.get("OKF_CHAT_ACCESS_TOKEN", "")
        self.max_turns = int(os.environ.get("OKF_CHAT_MAX_TURNS", "12"))
        # Voice is optional: only enabled if both audio model aliases are configured.
        self.voice = None
        v = voice_mod.from_env()
        if v.stt_model and v.tts_model:
            self.voice = v

    def ask(self, question: str) -> dict:
        result = agent.answer(question, gateway=self.gateway, navigator=self.nav,
                              system_prompt=self.system_prompt, max_turns=self.max_turns)
        spoken, provenance = voice_mod.split_channels(result["final_text"])
        resolved, fabricated = check_citations(self.nav, extract_citations(provenance))
        return {
            "spoken": spoken,
            "provenance": provenance,
            "citations": resolved,
            "citations_fabricated": fabricated,   # surfaced so the UI can flag, never hide
            "files_read": result["files_read"],
        }


class Handler(BaseHTTPRequestHandler):
    server_version = "okf-chat/0.1"
    app: App = None  # set on the server instance below

    # --- helpers ---------------------------------------------------------------------

    def _send_json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, data: bytes, content_type: str, code=200):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _authed(self) -> bool:
        token = self.app.access_token
        if not token:
            return True  # open mode (startup warned about it)
        got = self.headers.get("Authorization", "")
        return got == f"Bearer {token}"

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length") or 0)
        if length > _MAX_BODY:
            return b""
        return self.rfile.read(length) if length else b""

    def log_message(self, fmt, *args):  # quieter, single-line logs
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    # --- routes ----------------------------------------------------------------------

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._serve_file(os.path.join(WEB_DIR, "index.html"), "text/html; charset=utf-8")
        if self.path == "/api/health":
            return self._send_json({
                "ok": True,
                "voice_enabled": self.app.voice is not None,
                "model": self.app.gateway.model,
                "auth_required": bool(self.app.access_token),
            })
        return self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        if not self.path.startswith("/api/"):
            return self._send_json({"error": "not found"}, 404)
        if not self._authed():
            return self._send_json({"error": "unauthorized"}, 401)
        try:
            if self.path == "/api/ask":
                return self._route_ask()
            if self.path == "/api/transcribe":
                return self._route_transcribe()
            if self.path == "/api/speak":
                return self._route_speak()
        except GatewayError as e:
            return self._send_json({"error": f"gateway: {e}"}, 502)
        except Exception as e:  # never leak a stack to the client; log it
            self.log_message("error handling %s: %s", self.path, e)
            return self._send_json({"error": "internal error"}, 500)
        return self._send_json({"error": "not found"}, 404)

    def _route_ask(self):
        payload = json.loads(self._read_body() or b"{}")
        question = (payload.get("question") or "").strip()
        if not question:
            return self._send_json({"error": "empty question"}, 400)
        return self._send_json(self.app.ask(question))

    def _route_transcribe(self):
        if self.app.voice is None:
            return self._send_json({"error": "voice not enabled on this deployment"}, 501)
        audio = self._read_body()
        if not audio:
            return self._send_json({"error": "empty or oversized audio"}, 400)
        filename = self.headers.get("X-Audio-Filename", "question.webm")
        return self._send_json({"text": self.app.voice.transcribe(audio, filename=filename)})

    def _route_speak(self):
        if self.app.voice is None:
            return self._send_json({"error": "voice not enabled on this deployment"}, 501)
        payload = json.loads(self._read_body() or b"{}")
        text = (payload.get("text") or "").strip()
        if not text:
            return self._send_json({"error": "empty text"}, 400)
        audio = self.app.voice.synthesize(text)
        return self._send_bytes(audio, _audio_mime(self.app.voice.tts_format))

    def _serve_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                self._send_bytes(f.read(), content_type)
        except FileNotFoundError:
            self._send_json({"error": "ui not found"}, 404)


def _audio_mime(fmt: str) -> str:
    return {"mp3": "audio/mpeg", "opus": "audio/opus", "aac": "audio/aac",
            "flac": "audio/flac", "wav": "audio/wav", "pcm": "audio/pcm"}.get(fmt, "audio/mpeg")


def main() -> int:
    host = os.environ.get("OKF_CHAT_HOST", "0.0.0.0")
    port = int(os.environ.get("OKF_CHAT_PORT", "8080"))
    try:
        app = App()
    except (NotADirectoryError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except GatewayError as e:
        print(f"gateway config error: {e}\n"
              f"Set OKF_CHAT_BASE_URL / OKF_CHAT_MODEL (see deploy/.env.example).",
              file=sys.stderr)
        return 2

    Handler.app = app
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"okf-chat serving on http://{host}:{port}  "
          f"(model={app.gateway.model}, voice={'on' if app.voice else 'off'})")
    if not app.access_token:
        print("WARNING: OKF_CHAT_ACCESS_TOKEN is unset -- the server is OPEN to anyone who "
              "can reach it. Set a token before exposing this beyond localhost.",
              file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
