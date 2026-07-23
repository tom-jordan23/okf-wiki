# preso/ — decks from Markdown

An **optional** presentation tier: build leadership decks from Markdown, deterministically.
It is a sibling to `docs/` (a publish surface), lives **outside** the `okf/` bundle, and
carries no OKF frontmatter. Delete this whole directory if you don't present.

## The contract

1. **The Markdown is the source of record.** One `.md` per deck holds the speaker script
   (BLUF on each slide face; the precise, caveated version in the notes). `build_pptx.py`
   *mirrors* it — it never becomes a second source of truth. Change content in the `.md`
   and re-run the build.
2. **Every slide claim traces back to an `okf/` note.** A deck is a rendering of the
   knowledge base, not new knowledge. If a slide asserts something, the note it rests on
   exists and is linked from the speaker script.
3. **Decks are generated, never hand-edited.** No fact lives only inside a `.pptx`. If you
   tweak a slide in PowerPoint, you've forked the source — put the change in the `.md`.

## Use

```sh
pip install -r preso/requirements.txt     # one third-party dep: python-pptx
cd preso
./build.sh                                # build every *.md in this dir
./build.sh example-recommendation         # build one deck
```

`build.sh` prints an actionable message (and exits cleanly) if `python-pptx` or a branded
template is missing — the rest of the repo stays dependency-free; only deck-building needs
the dep.

## Branded templates (optional)

Drop an org-branded `.pptx`/`.potx` in `preso/templates/` and point the builder at it. Those
files are **git-ignored** (they're often proprietary) — symlink yours in, or commit only a
neutral house template you own. The builder works with no template at all (plain slides).

## Files

```text
preso/
  README.md                    this file
  requirements.txt             python-pptx (the only third-party dep in the repo)
  build.sh                     wrapper: dep/template checks, renders <deck>.md -> <deck>.pptx
  build_pptx.py                the deterministic builder (python-pptx)
  example-recommendation.md    a domain-neutral worked deck (delete with the other examples)
  templates/                   branded .pptx/.potx go here (git-ignored)
```
