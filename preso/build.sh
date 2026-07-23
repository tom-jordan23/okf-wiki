#!/usr/bin/env bash
# Build decks from Markdown. Wrapper around build_pptx.py that fails helpfully when the
# optional python-pptx dependency (or a named template) is missing.
#
#   ./build.sh                     build every *.md in this directory
#   ./build.sh example-recommendation   build one deck (with or without the .md extension)
#
# A branded template is optional: set PRESO_TEMPLATE=templates/your-brand.pptx to use one.
set -euo pipefail

cd "$(dirname "$0")"

PY="${PYTHON:-python3}"

# --- dependency check (the only third-party dep in the repo) ---------------------------
if ! "$PY" -c "import pptx" >/dev/null 2>&1; then
  cat >&2 <<'MSG'
python-pptx is not installed — it is needed only to build decks.
Install it with:

    pip install -r requirements.txt

(The rest of the repo, including scripts/validate.py, needs no third-party packages.)
MSG
  exit 3
fi

# --- optional branded template ---------------------------------------------------------
TEMPLATE_ARG=()
if [[ -n "${PRESO_TEMPLATE:-}" ]]; then
  if [[ ! -f "$PRESO_TEMPLATE" ]]; then
    echo "error: PRESO_TEMPLATE set but not found: $PRESO_TEMPLATE" >&2
    echo "       drop a branded .pptx/.potx in templates/ (git-ignored) and point here," >&2
    echo "       or unset PRESO_TEMPLATE to build plain slides." >&2
    exit 2
  fi
  TEMPLATE_ARG=(--template "$PRESO_TEMPLATE")
fi

# --- choose decks ----------------------------------------------------------------------
decks=()
if [[ $# -gt 0 ]]; then
  for name in "$@"; do
    [[ "$name" == *.md ]] && decks+=("$name") || decks+=("$name.md")
  done
else
  shopt -s nullglob
  for f in *.md; do
    [[ "$f" == "README.md" ]] && continue
    decks+=("$f")
  done
fi

if [[ ${#decks[@]} -eq 0 ]]; then
  echo "no deck .md files to build in $(pwd)" >&2
  exit 0
fi

for deck in "${decks[@]}"; do
  if [[ ! -f "$deck" ]]; then
    echo "error: no such deck: $deck" >&2
    exit 2
  fi
  "$PY" build_pptx.py "$deck" ${TEMPLATE_ARG[@]+"${TEMPLATE_ARG[@]}"}
done
