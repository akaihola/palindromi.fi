# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static site generator for palindromi.fi, a Finnish palindrome collection website. It processes palindromes stored in YAML files and renders them as HTML pages with illustrations and translations.

## Commands

### Development Environment (Nix)
```bash
nix develop              # Enter development shell
nix run '.#default.lock' # Initialize project after cloning
```

### CLI Commands
```bash
python -m palindromi_fi_builder render ./database -o ./html  # Render site to HTML
python -m palindromi_fi_builder load ./database              # Dump database as YAML to stdout
python -m palindromi_fi_builder.server -d ./html             # Serve rendered site (port 8000)
```

### Testing and Linting
```bash
pytest                                    # Run all tests
pytest palindromi_fi_builder/tests/test_syncer.py  # Run single test file
flake8                                    # Lint
mypy                                      # Type check
```

Install test dependencies: `pip install -e ".[test]"`

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
`adhoc/` contains one-time importers for Flowdock and Zoho Notebook exports.

## Code Style

- Uses Darker for incremental Black formatting (configured in pyproject.toml)
- Finnish palindrome validation includes ä and ö characters (see `palindrome.py`)
- Typography filter converts quotes to HTML entities for proper typographic rendering
