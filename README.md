# palindromi.fi

A static Finnish palindrome collection with English translations and illustrations.

Install uv, GNU Make and Python 3.11 for the site build. The current Transcrypt
build is known not to work on Python 3.14. Run from the repository root:

```bash
uv sync --frozen --python 3.11
uv run --no-sync make build
uv run --no-sync python -m http.server --bind 127.0.0.1 --directory html 8000
```

Open http://127.0.0.1:8000/. Re-run `uv run --no-sync make build` after editing
content. Make compiles navigation JavaScript and renders HTML and illustrations.

```bash
uv run --no-sync pytest
```

Published entries live in `database/palindromes/*.yaml`. Filename and row order
set navigation; the last entry is the homepage. `database/INBOX.yaml` is unpublished.
Exact text, including newlines, determines page identifiers: Base58 of the first
four bytes of its UTF-8 SHA-256 digest. Do not normalize published text casually.

The builder loads YAML in `database.py`, renders Jinja templates in `render.py`,
and updates output through `syncer.py`. Make compiles keyboard navigation from
`static/palindrome.py`. The `load` subcommand dumps derived site data, including
identifiers and navigation, and omits fields such as grading and series. It is
not a lossless database backup. See [AGENTS.md](AGENTS.md) for command scopes and
incremental lint checks.

See [docs/zoho-import.md](docs/zoho-import.md) for the unfinished import and
[TASKS.md](TASKS.md) for work status. The current Zoho converter output is unsafe
to import. Completed task descriptions record history, not current instructions.

Pushing `main` triggers GitHub Pages deployment. Publishing and deployment belong
to Antti; a local build does not require either. See
[docs/deployment.md](docs/deployment.md) for the operating details.
