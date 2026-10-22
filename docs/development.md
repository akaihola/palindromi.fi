# Development

Use the [quick start] for Python 3.11 setup, the full build and local preview.
Commands below run from the repository root after that frozen install.
Dev dependencies are included by default. A production-only install uses
`uv sync --frozen --python 3.11 --no-dev`; sync again without `--no-dev` for checks.

## Commands and defaults

```bash
uv run --no-sync python -m palindromi_fi_builder render ./database -o ./html
uv run --no-sync python -m palindromi_fi_builder load ./database
uv run --no-sync python -m palindromi_fi_builder format ./database/palindromes
uv run --no-sync python -m palindromi_fi_builder format ./database/INBOX.yaml
uv run --no-sync python -m palindromi_fi_builder.server --bind 127.0.0.1 -d ./html 8000
```

- **Build:** `uv run --no-sync make build` compiles navigation JavaScript when
  its target is missing or older than the [navigation source], then always renders.
  It does not clean first. Direct `render` does not compile JavaScript.
- **Render:** defaults to the [database directory] and [HTML output directory].
  It reads curated rows, copies package static assets and illustrations, and
  removes obsolete output through `Syncer`. Use a dedicated output directory.
- **Load:** defaults to the [database directory] and prints derived site YAML
  to stdout. It is not a lossless database backup; see the data contract below.
- **Format:** defaults to the [curated directory]. A directory argument selects
  only its immediate `*.yaml` files; a file argument must end in `.yaml`.
  Pass the explicit [INBOX] path for drafts. It neither validates nor publishes.
  Only palindrome and translation text fields receive literal-scalar conversion:
  values with LF newlines or more than 50 characters use literal blocks; other
  values are left unchanged by the helper. Chomping (`|-`, `|`, `|+`) depends on trailing
  newlines. The helper normalizes CRLF and CR to LF when conversion is selected,
  so it does not preserve every possible scalar value. Its dumper width is 88,
  not a maximum line length for literal blocks or unbreakable strings.
- **Serve:** the quick start uses Python's standard HTTP server. The package
  server above also assigns HTML MIME type to legacy extensionless files.
  Its defaults are the current directory, all interfaces, and port 8000;
  the example explicitly serves generated output on loopback. Neither server
  rebuilds files.

## Data and rendering

[database.py] reads only immediate `*.yaml` files in the [curated directory],
sorted by filename, then in row order. [INBOX] is unpublished. Input must contain
at least one row. Navigation wraps: `next` points to the preceding row and
`previous` to the following row. The last row becomes the homepage; creation
dates do not sort the site.

`calculate_identifier()` encodes the first four bytes of the exact text's UTF-8
SHA-256 digest in Base58. Whitespace and newlines affect URLs. Preserve published
text, including when formatting it.

`db_to_site_palindrome()` copies text, author, translations and optional
illustrations/creation date, and adds an identifier and navigation container.
Other source fields, including grading and series, are omitted. Keep source
YAML for backups and editorial work. The loader does not validate the schema;
missing required keys fail during conversion, and an empty translation list
fails when the [page template] accesses its first item.

[render.py] writes one `.html` page per identifier and copies the final page to
the homepage. Illustrations come from the [illustration directory]. The
[page template] uses Tufte CSS and [main.css]; [typography.py] emits typographic
quote entities. [palindrome.py] validates by lowercasing and retaining only
`a-z`, digits, `ä` and `ö`, with at least three retained characters; rendering
does not call that validator. [Syncer] preserves unchanged files on their first
write per instance; repeated destinations are a known limitation.

## Tests and incremental checks

```bash
uv run --no-sync pytest
uv run --no-sync pytest palindromi_fi_builder/tests/test_syncer.py
uv run --no-sync graylint --revision origin/main... -L flake8 -L mypy -L pylint ./palindromi_fi_builder
uv run --no-sync darker --check --diff --isort --revision origin/main... ./palindromi_fi_builder
uv run --no-sync make build
```

The focused Syncer command is optional when the full suite has run. The lint
and formatting commands match [Linting] and [Formatting], using the locally
available `origin/main` reference. Full diagnostics with
`uv run --no-sync flake8 --extend-exclude .venv` and `uv run --no-sync mypy .`
have known baseline findings recorded in the [architecture review]. Their
failure does not invalidate the accepted incremental CI fixes. `make lint`
is a legacy entry point requiring undeclared darglint2; architecture draft I
owns its reconciliation. See the [deployment guide] for CI scope.

[quick start]: ../README.md
[database directory]: ../database/
[curated directory]: ../database/palindromes/
[HTML output directory]: ../html/
[INBOX]: ../database/INBOX.yaml
[navigation source]: ../palindromi_fi_builder/static/palindrome.py
[database.py]: ../palindromi_fi_builder/database.py
[render.py]: ../palindromi_fi_builder/render.py
[Syncer]: ../palindromi_fi_builder/syncer.py
[page template]: ../palindromi_fi_builder/templates/palindrome.html
[illustration directory]: ../database/illustrations/
[main.css]: ../palindromi_fi_builder/static/main.css
[typography.py]: ../palindromi_fi_builder/typography.py
[palindrome.py]: ../palindromi_fi_builder/palindrome.py
[Linting]: ../.github/workflows/linting.yaml
[Formatting]: ../.github/workflows/formatting.yaml
[architecture review]: reviews/2026-10-19-architecture-review.md
[deployment guide]: deployment.md
