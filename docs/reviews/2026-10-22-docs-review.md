# Documentation review, 2026-10-22

Reviewed canonical local `main` at `c82d6fb` after committing the task's start
move. The cached `origin/main` was `edca600`; no remote freshness check was made.
This is a source and text review. Historical reviews and earlier task records
were left unchanged. Validation and resource measurements are in the
[task record]. No push, deployment, live import or CI run was attempted.

## Coverage

All five Markdown files selected by `git ls-files '*.md'`, excluding the
[task descriptions], [review directory] and [tracker], were read completely:

- **[Quick start]:** setup, build, preview, data layout and command claims.
- **[Agent guidance]:** command defaults, checks, architecture and import claims.
- **[Claude entry point]:** its existing include still resolves to agent guidance;
  no change needed.
- **[Deployment guide]:** checked against all three workflow definitions and the
  latest recorded [Ubuntu 26 validation]. Four jobs pin Ubuntu 26.04; hosted
  deployment remains unverified in that record, not rechecked here.
- **[Zoho import notes]:** current tracker/data claims checked; private export
  counts, versions and dating retained as the October 5 investigation snapshot.
  Private exports were not available for independent reproduction.

All 20 tracked Python sources were read, including docstrings and comments:

- **Builder:** [package metadata], [CLI registration], [database conversion],
  [formatter], [load command], [palindrome validator], [renderer], [HTTP server],
  [Syncer], [typography] and [YAML helpers].
- **Imports and diagnostics:** [adhoc package], [HTML converter],
  [public-note downloader], [HTML analysis] and [revision analysis].
- **Browser source:** [navigation script].
- **Tests:** [render tests], [Syncer tests] and [typography tests], read without
  edits. Their existing assertions remain the before/after baseline.

Also read [Makefile], [project configuration], [Deploy], [Linting], [Formatting],
[flake8 settings], [mypy settings], [darglint settings], [ignore rules],
[page template], [site CSS] and [domain file]. The tracked database YAML has no
comments. Parsed its 47 curated rows and 109 graded INBOX rows for the claims
below. Image contents and third-party assets were outside this text review.

## Changes by file

Each entry names the implementation that the revised text describes.

- **[Quick start]:** retained the Python 3.11 setup/build/preview entry point;
  moved duplicate command/data explanations to the development guide. Build
  wording matches the phony `build` target and JS prerequisite in [Makefile].
- **[Agent guidance]:** reduced to repository rules and links to the canonical
  command/data guide. References match [CLI registration], [project configuration]
  and the workflow commands; publishing ownership remains explicit.
- **[Development guide] (new):** consolidates CLI commands, defaults, source layout
  and checks. Sources: Click decorators in [formatter], [load command] and
  [renderer]; `main()` in [HTTP server]; `read_database()` and
  `calculate_identifier()` in [database conversion]; [Makefile] and all workflows.
  Corrects the old claim that both servers serve generated output only: directory
  selection is explicit, and the package server defaults to the current directory
  on all interfaces. Explains row-order navigation, literal-scalar conversion,
  obsolete-output removal and omitted editorial fields.
- **[Deployment guide]:** links to canonical local checks and removes a completed
  task's publishing prohibition from general operating guidance. Ubuntu 26 status
  is explicitly the recorded October 21 result, matching [Deploy], [Linting],
  [Formatting] and the [Ubuntu 26 validation] record.
- **[Zoho import notes]:** separates current work from the October 5 snapshot;
  removes completed duplicate removal and dependency fixes from the remaining
  plan. Current data claims match [INBOX] and `read_database()`. Script guidance
  matches the HTML converter's filename glob, first `parsed-html` match,
  `seen_palindromes` update and output deletion; the downloader's `parse_block()`;
  and both diagnostic scripts' UTF-8 replacement decoding and inline dependencies.
  Links to the data contract replace duplicate identifier/translation rules.
- **[Database conversion]:** docstrings specify copied fields, omitted editorial
  fields, immediate curated YAML scope, nonempty input, row-order circular links
  and four-byte SHA-256/Base58 identifiers. The navigation comment now describes
  row order rather than implying creation dates are sorted. Matches
  `db_to_site_palindrome()`, `read_database()` and `calculate_identifier()`.
- **[Load command]:** CLI and module docstrings describe derived site YAML to
  stdout, with identifiers/navigation and lost editorial fields. Matches its
  `read_database()` call and `yaml.dump(..., sys.stdout)`.
- **[Formatter]:** removes redundant procedural comments; describes only the text
  fields actually passed to `maybe_preserve_literal()`, immediate-directory scope,
  the default curated directory, width and newline limitations. Matches
  `reformat_yaml_file()`, the Click argument and `target.glob('*.yaml')`.
- **[YAML helpers]:** distinguishes the width-only dumper factory from explicit
  literal conversion; removes unconditional inline-style and `|-` promises.
  Matches `create_yaml_dumper()`, `maybe_preserve_literal()` and the locked
  ruamel.yaml 0.18.16 `preserve_literal()` implementation. The dependency replaces
  CRLF/CR with LF; local probes confirm `|-`, `|` and `|+` for trailing-newline
  variants. Literal block width is not capped at 88 characters.
- **[Palindrome validator]:** describes the actual normalization alphabet and
  three-character minimum in `is_palindrome()`, including its inability to
  distinguish palindrome drafts from complete entries.
- **[Renderer]:** documents curated input, default directories, existing-asset
  copying, final-row homepage and stale-output deletion in `render()`; completes
  the truncated return-path sentence in `render_palindrome_and_illustrations()`.
- **[Syncer]:** replaces an obsolete gsutil comparison claim with historical
  motivation and current Pages deployment. Fixes the package import and variable
  names in the example. Documents single-use destinations, explicit cleanup,
  UTF-8 text and `copytree()`'s absolute file/subdirectory return paths. These
  match `write_bytes()`, `write_text()`, `copytree()` and `remove_deleted()`.
- **[HTML converter]:** docstrings distinguish historical selected content from
  export-time live content, empty-br versus empty-div handling, first-match
  extraction, filename ordering, same-export duplicates and output-file deletion.
  Matches `ContentExtractor`, `extract_from_main_html()` and `main()`; makes no
  claim that the already-owned converter rewrite has landed.
- **[Public-note downloader]:** `parse_block()` now documents the first passing
  prefix, optional remainder and actual `NoPalindromeFound` exception. Its
  exception-class docstring uses the same prefix condition. API wording matches
  the constructed public-notecard URL, without claiming a live-service test.
- **[HTML analysis]:** removes the recommendation to trust the converter and
  points to current import findings. Describes exploratory UTF-8 replacement
  decoding and the 100,000-character script threshold in `extract_script_data()`.
- **[Revision analysis]:** removes verified-version/single-snapshot claims and
  describes the actual marker filters, character offsets and four-element tuples
  in `find_version_content_blocks()`. Notes discarded blank lines in
  `extract_text_from_html()` and the 10,000-character threshold in
  `analyze_script_tags()`. Comments identify heuristics rather than proven versions.
- **[Task record]:** appends this run's evidence and required memory accounting;
  preserves the original requirements. The review itself is this new file.

## Validation and limits

The frozen environment used CPython 3.11.16. The host defaults disable managed
Python downloads and select system interpreters, so setup required command-local
`UV_PYTHON_DOWNLOADS=automatic UV_PYTHON_PREFERENCE=managed`. Neither setting was
changed globally. Both initially failed setup attempts are recorded in the task.

Before edits, `uv run --no-sync pytest` passed 39 tests and the focused Syncer
suite passed 11. Required incremental Graylint, Darker and the complete build
passed. After text edits, both suites, Graylint and the build passed again.
The 64 generated files, including 48 HTML pages, have identical SHA-256 hashes.
Executable ASTs for all 11 edited Python files match baseline after stripping
only docstrings; tests, configuration and database content are unchanged.

Darker currently reports one existing import-order defect in the HTML converter.
Its installed `apply_isort()` uses the first-to-last edited-line range, so edits
to docstrings before and after the imports expose that otherwise untouched block.
The text-only scope forbids the requested two-import swap; an explicit scope
question is pending. Final formatting approval and merge are not yet complete.

An automatic edit hook also reported existing Ruff/ty diagnostics in unchanged
imports, annotations and executable statements. These are outside the repository's
required incremental checks, not new behavior changes; no autofixes were applied.
The full-tree flake8/mypy diagnostics and legacy `make lint` were not repeated;
their existing debt remains recorded in architecture draft I.

Synthetic local probes verified converter blank-line loss, the actual parser
exception/prefix behavior, scalar chomping and carriage-return normalization,
repeated Syncer writes/copies and the nested-break failure below. They used
memory-bounded temporary fixtures; no live service was contacted and no test
file was added or changed.

## Draft issues

These are proposed follow-ups, not filed issues. Existing owners are linked so
the steward can extend their scope instead of creating duplicates.

- **D1 — Preserve formatted scalar values (extend draft H).** The formatter
  maps a quoted scalar `"aba\r\n"` to `"aba\n"` through ruamel's
  `preserve_literal()`. Current curated/INBOX palindrome and translation values
  contain no CR, so no present-data regression was found. The intended policy
  is unclear because exact text determines identifiers while earlier guidance
  promised preservation.

  **Recommendation:** extend [architecture draft H] to preserve scalar bytes in
  memory (or reject unsupported line endings without rewriting), with CR, CRLF,
  LF and trailing-newline round-trip cases. Do not normalize published text
  silently. This review only corrects the description of current behavior.

- **D2 — Finish converter semantics under its existing owner.** Empty-div
  markup yields `aba\naca` instead of `aba\n\naca`; the filename glob rejects
  planned version-suffixed exports and the within-export filter retains repeats.
  Those mechanisms explain the contradictions between prior docstrings and
  import instructions. Private-export counts remain historical evidence.

  **Recommendation:** keep repair in the [converter rewrite], using the
  [export refresh] and [import rules] for ordering and duplicate policy. The
  documentation change does not establish safe import output.

- **D3 — Resolve Syncer's single-use contract (draft J).** Two identical writes
  to a new destination return `True, True`; a repeated copy of a nested tree
  raises `KeyError` because `old_files.remove()` sees a directory twice. This
  conflicts with the former unconditional unchanged-file guarantee.

  **Recommendation:** retain [architecture draft J]'s idempotent-write proposal;
  keep the documented limitation until that behavior and its tests change.

- **D4 — Decide the legacy diagnostic-script contract.** The revision helper
  advertises `list[tuple[int, str]]` but appends four values. Both root diagnostics
  decode exports with UTF-8 replacement, while the recorded investigation found
  Windows-1252. Their marker matches cannot establish distinct version counts.

  **Recommendation:** if retained for the import work, align the annotation with
  the four-field result and use the export encoding before trusting diagnostics.
  Otherwise mark the unused helpers as historical and avoid using their output
  as importer evidence. Annotation/decoding changes exceed this text-only review.

- **D5 — Bound or fix legacy nested-break parsing.** In the [public-note downloader],
  `br_to_newline()` selects parents with direct breaks, collects all descendant
  breaks, then removes them as direct children. The synthetic input
  `<root><div>a<br/><div>b<br/></div></div></root>` raises
  `ValueError: list.remove(x): x not in list`. It is unclear whether callers are
  meant to guarantee flat markup; no live API contract was checked.

  **Recommendation:** document and validate a flat-input boundary if this legacy
  downloader remains limited, or traverse actual parents with nested fixtures if
  it is reused. Do not use it as the historical-export importer. Multi-line
  palindrome/translation choices remain with the [import rules].

- **D6 — Reconcile formatting with text-only edits.** Required Darker exposes an
  existing import-order defect when converter documentation spans its imports.
  The candidate is otherwise text-only and the executable AST is unchanged.

  **Recommendation:** permit the isolated standard-library import reorder, then
  rerun required checks, or retain this as a merge blocker under strict text-only
  scope. No formatter suppression or configuration change has been introduced.

[task record]: ../tasks/16-check-palindromi-fi-s-documents-docstrings-and-comments-against-curren.md
[task descriptions]: ../tasks/
[review directory]: ./
[tracker]: ../../TASKS.md
[Quick start]: ../../README.md
[Agent guidance]: ../../AGENTS.md
[Claude entry point]: ../../.claude/CLAUDE.md
[Deployment guide]: ../deployment.md
[Development guide]: ../development.md
[Zoho import notes]: ../zoho-import.md
[Ubuntu 26 validation]: ../tasks/11-validate-ubuntu-26-workflows-and-remove-ubuntu-24-04-pins.md
[package metadata]: ../../palindromi_fi_builder/__init__.py
[CLI registration]: ../../palindromi_fi_builder/__main__.py
[database conversion]: ../../palindromi_fi_builder/database.py
[formatter]: ../../palindromi_fi_builder/format.py
[load command]: ../../palindromi_fi_builder/load.py
[palindrome validator]: ../../palindromi_fi_builder/palindrome.py
[renderer]: ../../palindromi_fi_builder/render.py
[HTTP server]: ../../palindromi_fi_builder/server.py
[Syncer]: ../../palindromi_fi_builder/syncer.py
[typography]: ../../palindromi_fi_builder/typography.py
[YAML helpers]: ../../palindromi_fi_builder/yaml_utils.py
[adhoc package]: ../../palindromi_fi_builder/adhoc/__init__.py
[HTML converter]: ../../palindromi_fi_builder/adhoc/convert_zoho_html.py
[public-note downloader]: ../../palindromi_fi_builder/adhoc/zoho_notebook.py
[HTML analysis]: ../../analyze_zoho_html.py
[revision analysis]: ../../extract_zoho_revisions.py
[navigation script]: ../../palindromi_fi_builder/static/palindrome.py
[render tests]: ../../palindromi_fi_builder/tests/test_render.py
[Syncer tests]: ../../palindromi_fi_builder/tests/test_syncer.py
[typography tests]: ../../palindromi_fi_builder/tests/test_typography.py
[Makefile]: ../../Makefile
[project configuration]: ../../pyproject.toml
[Deploy]: ../../.github/workflows/deploy.yaml
[Linting]: ../../.github/workflows/linting.yaml
[Formatting]: ../../.github/workflows/formatting.yaml
[flake8 settings]: ../../.flake8
[mypy settings]: ../../mypy.ini
[darglint settings]: ../../.darglint2
[ignore rules]: ../../.gitignore
[page template]: ../../palindromi_fi_builder/templates/palindrome.html
[site CSS]: ../../palindromi_fi_builder/static/main.css
[domain file]: ../../palindromi_fi_builder/static/CNAME
[INBOX]: ../../database/INBOX.yaml
[architecture draft H]: 2026-10-19-architecture-review.md#h-make-the-yaml-formatters-literal-policy-real-and-testable
[architecture draft J]: 2026-10-19-architecture-review.md#j-make-syncer-writes-idempotent-within-one-run
[converter rewrite]: ../tasks/2-fix-zoho-converter.md
[export refresh]: ../tasks/1-refresh-zoho-exports.md
[import rules]: ../tasks/4-zoho-import-rules.md
