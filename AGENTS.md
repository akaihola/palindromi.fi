# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static site generator for palindromi.fi, a Finnish palindrome collection website. It processes palindromes stored in YAML files and renders them as HTML pages with illustrations and translations.

## Commands

Use the [README](README.md) for the supported Python 3.11 setup and complete
`uv run --no-sync make build` path. Direct rendering does not compile navigation
JavaScript. Transcrypt is known to fail on Python 3.14.

### Command scopes

Run these from the repository root after `uv sync --frozen --python 3.11`:

```bash
uv run --no-sync make build
uv run --no-sync python -m palindromi_fi_builder render ./database -o ./html
uv run --no-sync python -m palindromi_fi_builder load ./database
uv run --no-sync python -m palindromi_fi_builder format ./database/palindromes
uv run --no-sync python -m palindromi_fi_builder format ./database/INBOX.yaml
uv run --no-sync python -m palindromi_fi_builder.server --bind 127.0.0.1 -d ./html 8000
```

- `make build` compiles JavaScript as needed and always renders the curated site.
- `render` and `load` read only `database/palindromes/*.yaml`, in sorted filename
  and row order. Neither reads the unpublished `database/INBOX.yaml`.
- `render` is useful after compilation, but use Make for a complete build.
- `load` emits derived site YAML with identifiers and navigation. It drops fields
  such as grading and series, so it is not a lossless database backup.
- `format` rewrites the given file or the directory's immediate `*.yaml` files.
  Its default is the curated `./database/palindromes` directory. Give the explicit
  INBOX path to format drafts. It preserves scalar values; block chomping depends
  on trailing newlines. It does not validate or publish entries.
- Both local server commands serve generated output only. The README uses
  Python's standard HTTP server; the package server also supports legacy
  extensionless HTML pages.

### Tests and lint

Dev dependencies are included by default. A production-only install uses
`uv sync --frozen --python 3.11 --no-dev`; sync again without `--no-dev` for checks.

```bash
uv run --no-sync pytest
uv run --no-sync pytest palindromi_fi_builder/tests/test_syncer.py
uv run --no-sync graylint --revision origin/main... -L flake8 -L mypy -L pylint ./palindromi_fi_builder
uv run --no-sync darker --check --diff --isort --revision origin/main... ./palindromi_fi_builder
```

These lint and formatting commands match incremental CI. Full diagnostics with
`uv run --no-sync flake8 --extend-exclude .venv` and `uv run --no-sync mypy .` have known baseline
findings, recorded in the architecture review. Their failure does not invalidate
the accepted incremental CI fixes. `make lint` is a legacy entry point requiring
undeclared darglint2; review draft I owns its reconciliation.

See [deployment](docs/deployment.md) for Antti's publishing workflow.

## Architecture

### Data Flow
1. **Database** (`database/palindromes/*.yaml`): YAML files containing palindromes with text, author, translations, illustrations, and creation dates
2. **database.py**: Reads YAML files, converts `DbPalindrome` to `SitePalindrome` format, generates Base58 identifiers from the first four bytes of the exact UTF-8 text's SHA-256 digest
3. **render.py**: Uses Jinja2 templates to generate HTML pages, manages static assets
4. **syncer.py**: Handles incremental file updates (only writes changed files to preserve timestamps; historically used with `gsutil rsync`, now deployed through GitHub Pages artifacts)

### Key Types (database.py)
- `DbPalindrome`: Database format with text, author, translations, illustrations, created date
- `SitePalindrome`: Extends DbPalindrome with `identifier` (for URLs) and `links` (prev/next navigation)

### Static Files
- `templates/palindrome.html`: Jinja2 template using Tufte CSS
- `static/palindrome.py`: Transpiled to JavaScript via Transcrypt for keyboard navigation
- `static/main.css`: Custom styles

### Ad-hoc Import Scripts
`adhoc/` contains one-time importers for data sources.

#### Zoho Notebook Converter (`adhoc/convert_zoho_html.py`)
Extracts palindrome content from Zoho Notebook HTML exports. Each export contains a `parsed-html` attribute with entity-encoded HTML content. The script decodes and converts this to plaintext, preserving blank lines between palindromes while collapsing consecutive empty lines from nested HTML tags.

Usage:
```bash
uv run --no-sync python -m palindromi_fi_builder.adhoc.convert_zoho_html
```

Processes all `YYYY-MM-DD.html` files in the local, git-ignored `zoho-history/` directory and writes a `YYYY-MM-DD.txt` per export containing only entries not seen in earlier files.

Known broken: it orders exports by filename (several filenames are wrong) and reads exports saved from the phone app as a single entry. Don't trust its output. See `docs/zoho-import.md` for the export format, the findings and the import plan.

#### Zoho Notebook API downloader (`adhoc/zoho_notebook.py`)
2023 script that fetches a publicly shared Zoho note through the notecard API and converts its blocks to `DbPalindrome` dicts.

## Code Style

- Uses Darker for incremental Black formatting (configured in pyproject.toml)
- Finnish palindrome validation includes ä and ö characters (see `palindrome.py`)
- Typography filter converts quotes to HTML entities for proper typographic rendering
