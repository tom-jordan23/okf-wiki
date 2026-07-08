#!/usr/bin/env python3
"""Read-only navigation tools scoped to an OKF bundle checkout.

This is the *bundle-navigation capability* from ADR-0003 decision 6, packaged as a
standalone module so it can later be exposed as an MCP server (or called directly from
the phase-1 POC loop) without being welded into any app. It exposes exactly three
read-only tools -- ``read_file``, ``list_dir``, ``grep`` -- every one of them confined
to a single root directory (the ``okf/`` checkout). Nothing here writes.

Design constraints it honors:
- **Read-only.** No tool mutates the filesystem.
- **Scoped.** Every path argument is resolved and rejected if it escapes the root, so
  the model cannot read outside the bundle (no ``../../etc/passwd``, no symlink escape).
- **Provider-agnostic.** ``tool_specs()`` emits OpenAI-format function schemas, which is
  the shape LiteLLM (internal or the platform gateway) proxies to any approved model.

No third-party dependencies -- stdlib only, same as ``scripts/validate.py``.
"""
from __future__ import annotations

import json
import os
import re

# Hard caps so a single tool call can never flood the context window.
_MAX_FILE_BYTES = 120_000
_MAX_GREP_MATCHES = 200
_MAX_GREP_FILE_BYTES = 2_000_000


class Navigator:
    """Read-only file tools confined to ``root`` (an OKF bundle checkout)."""

    def __init__(self, root: str):
        # realpath so symlinks in the checkout are resolved up front; every access is
        # then checked against this canonical root.
        self.root = os.path.realpath(root)
        if not os.path.isdir(self.root):
            raise NotADirectoryError(f"bundle root is not a directory: {root}")

    # --- path safety -----------------------------------------------------------------

    def _resolve(self, rel: str) -> str:
        """Resolve ``rel`` under the root, rejecting any escape.

        Raises ValueError if the resulting path is outside the bundle root.
        """
        rel = (rel or ".").strip()
        # Reject absolute inputs outright; everything is relative to the bundle root.
        if os.path.isabs(rel):
            raise ValueError(f"path must be relative to the bundle root: {rel!r}")
        resolved = os.path.realpath(os.path.join(self.root, rel))
        if resolved != self.root and not resolved.startswith(self.root + os.sep):
            raise ValueError(f"path escapes the bundle root: {rel!r}")
        return resolved

    def _rel(self, absolute: str) -> str:
        """Path relative to the root, using forward slashes, for stable citations."""
        rel = os.path.relpath(absolute, self.root)
        return rel.replace(os.sep, "/")

    # --- tools -----------------------------------------------------------------------

    def read_file(self, path: str) -> str:
        target = self._resolve(path)
        if not os.path.isfile(target):
            return f"error: not a file: {path}"
        with open(target, "rb") as f:
            raw = f.read(_MAX_FILE_BYTES + 1)
        text = raw[:_MAX_FILE_BYTES].decode("utf-8", errors="replace")
        if len(raw) > _MAX_FILE_BYTES:
            text += f"\n\n[... truncated at {_MAX_FILE_BYTES} bytes ...]"
        return text

    def list_dir(self, path: str = ".") -> str:
        target = self._resolve(path)
        if not os.path.isdir(target):
            return f"error: not a directory: {path}"
        entries = []
        for name in sorted(os.listdir(target)):
            if name.startswith("."):
                continue
            full = os.path.join(target, name)
            kind = "dir " if os.path.isdir(full) else "file"
            entries.append(f"{kind}  {self._rel(full)}")
        listing = "\n".join(entries) if entries else "(empty)"
        return f"{self._rel(target)}/\n{listing}"

    def grep(self, pattern: str, path: str = ".") -> str:
        try:
            rx = re.compile(pattern)
        except re.error as e:
            return f"error: invalid regex {pattern!r}: {e}"
        base = self._resolve(path)
        targets = []
        if os.path.isfile(base):
            targets = [base]
        else:
            for dirpath, dirnames, filenames in os.walk(base):
                dirnames[:] = [d for d in dirnames if not d.startswith(".")]
                for fn in sorted(filenames):
                    if fn.endswith(".md"):
                        targets.append(os.path.join(dirpath, fn))
        matches = []
        for tp in sorted(targets):
            if os.path.getsize(tp) > _MAX_GREP_FILE_BYTES:
                continue
            with open(tp, encoding="utf-8", errors="replace") as f:
                for lineno, line in enumerate(f, 1):
                    if rx.search(line):
                        matches.append(f"{self._rel(tp)}:{lineno}: {line.rstrip()}")
                        if len(matches) >= _MAX_GREP_MATCHES:
                            matches.append(f"[... stopped at {_MAX_GREP_MATCHES} matches ...]")
                            return "\n".join(matches)
        return "\n".join(matches) if matches else f"(no matches for {pattern!r})"

    # --- dispatch + schema -----------------------------------------------------------

    def dispatch(self, name: str, arguments: dict) -> str:
        """Execute a tool call by name. Never raises -- errors are returned as text so
        the model can recover (e.g. retry with a valid path) inside the loop."""
        try:
            if name == "read_file":
                return self.read_file(arguments["path"])
            if name == "list_dir":
                return self.list_dir(arguments.get("path", "."))
            if name == "grep":
                return self.grep(arguments["pattern"], arguments.get("path", "."))
            return f"error: unknown tool {name!r}"
        except KeyError as e:
            return f"error: missing required argument {e} for tool {name!r}"
        except ValueError as e:
            return f"error: {e}"
        except Exception as e:  # defensive: keep the loop alive
            return f"error: {type(e).__name__}: {e}"

    def tool_specs(self) -> list:
        """OpenAI-format function-tool schemas for the chat/completions ``tools`` field."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "list_dir",
                    "description": (
                        "List files and subdirectories inside the OKF bundle. Start at the "
                        "root (path='.') and read index.md files to navigate progressively."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Bundle-relative directory (default '.').",
                            }
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": (
                        "Read one note's full text, including its YAML frontmatter "
                        "(type, status, sources, review_by, ...). Cite the note by this "
                        "bundle-relative path."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Bundle-relative file path, e.g. 'concepts/okf-frontmatter-schema.md'.",
                            }
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "grep",
                    "description": (
                        "Regex-search across .md files in the bundle. Returns matching "
                        "'path:line: text' rows. Use to locate which note discusses a term."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": "Python regular expression.",
                            },
                            "path": {
                                "type": "string",
                                "description": "Bundle-relative directory to search under (default '.').",
                            },
                        },
                        "required": ["pattern"],
                    },
                },
            },
        ]


if __name__ == "__main__":
    # Tiny smoke test: navigate the sibling okf/ bundle.
    here = os.path.dirname(os.path.abspath(__file__))
    nav = Navigator(os.path.join(here, os.pardir, "okf"))
    print(nav.list_dir("."))
    print("\n--- grep 'OKF requires' ---")
    print(nav.grep(r"OKF.*requires"))
    print("\n--- path-escape rejected? ---")
    print(nav.dispatch("read_file", {"path": "../CLAUDE.md"}))
    print(json.dumps(nav.tool_specs()[0], indent=2)[:200])
