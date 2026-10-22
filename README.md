# palindromi.fi

A static Finnish palindrome collection with English translations and illustrations.

Install uv, GNU Make and Python 3.11 for the site build. The current Transcrypt
build is known not to work on Python 3.14. Run from the repository root:

```bash
uv sync --frozen --python 3.11
uv run --no-sync make build
uv run --no-sync python -m http.server --bind 127.0.0.1 --directory html 8000
```

Open <http://127.0.0.1:8000/>. Re-run `uv run --no-sync make build` after editing
content. Make compiles navigation JavaScript as needed and always renders the site.

See the [development guide] for data layout, command scopes and local checks,
the [Zoho import notes] for the unfinished import, and the [tracker] for work
status. Completed task descriptions record history, not current instructions.

Pushing `main` triggers GitHub Pages deployment. Publishing and deployment belong
to Antti; a local build does not require either. See the [deployment guide].

[development guide]: docs/development.md
[Zoho import notes]: docs/zoho-import.md
[tracker]: TASKS.md
[deployment guide]: docs/deployment.md
