# docs/

Optional **publish surface** for the knowledge base. It sits *outside* the OKF bundle
(`okf/`), so nothing here is subject to OKF conformance.

This is intentionally empty for now. The `okf/` bundle is kept portable so that, when
you want a published docs site, you can point a static-site generator (MkDocs Material,
Quarto, or Docusaurus) at `okf/` — or curate a reader-facing subset here — without
restructuring the notes.

Choosing and wiring a generator is deferred (see the roadmap in `../CLAUDE.md`). Until
then, the bundle renders fine as Markdown on GitLab/GitHub and in Obsidian.
