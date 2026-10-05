# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static site generator for palindromi.fi, a Finnish palindrome collection website. It processes palindromes stored in YAML files and renders them as HTML pages with illustrations and translations.

## Commands

### Setup
```bash
uv sync                             # Install all dependencies (includes dev by default)
uv sync --no-dev                    # Install only production dependencies
```

### CLI Commands
```bash
uv run python -m palindromi_fi_builder render ./database -o ./html  # Render site to HTML
uv run python -m palindromi_fi_builder load ./database              # Dump database as YAML to stdout
uv run python -m palindromi_fi_builder.server -d ./html             # Serve rendered site (port 8000)
```

### Testing and Linting
```bash
uv run pytest                                    # Run all tests
uv run pytest palindromi_fi_builder/tests/test_syncer.py  # Run single test file
uv run flake8                                    # Lint
uv run mypy .                                    # Type check
```

Dev dependencies (pytest, flake8, mypy, pylint, type stubs) are installed by default with `uv sync`.

## Architecture

### Data Flow
1. **Database** (`database/palindromes/*.yaml`): YAML files containing palindromes with text, author, translations, illustrations, and creation dates
2. **database.py**: Reads YAML files, converts `DbPalindrome` to `SitePalindrome` format, generates Base58-encoded identifiers from SHA256 hash of text
3. **render.py**: Uses Jinja2 templates to generate HTML pages, manages static assets
4. **syncer.py**: Handles incremental file updates (only writes changed files to preserve timestamps for `gsutil rsync`)

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
uv run python -m palindromi_fi_builder.adhoc.convert_zoho_html
```

Processes all `YYYY-MM-DD.html` files in the local, git-ignored `zoho-history/` directory and writes a `YYYY-MM-DD.txt` per export containing only entries not seen in earlier files.

Known broken: it orders exports by filename (several filenames are wrong) and reads exports saved from the phone app as a single entry. Don't trust its output. See `docs/zoho-import.md` for the export format, the findings and the import plan.

#### Zoho Notebook API downloader (`adhoc/zoho_notebook.py`)
2023 script that fetches a publicly shared Zoho note through the notecard API and converts its blocks to `DbPalindrome` dicts.

## Code Style

- Uses Darker for incremental Black formatting (configured in pyproject.toml)
- Finnish palindrome validation includes ä and ö characters (see `palindrome.py`)
- Typography filter converts quotes to HTML entities for proper typographic rendering
