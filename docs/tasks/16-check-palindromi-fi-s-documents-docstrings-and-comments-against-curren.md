Steward issue, 2026-10-22 04:23 refill. Goal: learning-play (palindromi.fi is tier 3). Labelled `review` (steward D68). Estimated 45 min.

25 commits have landed on `main` since 2026-10-19, including the 10-19 architecture review's fixes and the Ubuntu 26 runner move. Each issue updated the documents only where it touched them, so statements elsewhere may now be stale or in conflict. palindromi.fi has had an architecture review but never a documentation check. It has few documents, so this check also covers docstrings and comments. The same check has run for kandev-pacer, Hai, Filemill, pi-akaihola, mailjail, kandev-config, skills-akaihola, iskumetri, dallape and syncop.

## What to do

1. Read every tracked Markdown file outside `docs/tasks/`, `docs/reviews/` and `TASKS.md` (`git ls-files '*.md'`), `README.md` and `AGENTS.md` first (`.claude/CLAUDE.md` too), against the code on current `main`: commands, settings and their defaults, file layout, deployment and import steps, how to build, run and test, and what each document says is done or planned.
2. Read the docstrings and comments of the site's scripts and sources (`git ls-files`) for statements the code no longer bears out: parameters, return values, units, defaults, invariants.
3. Fix plain discrepancies and stale statements in text only. Where two places explain the same thing, keep one and link to it. Keep entry points short.
4. Where it's unclear whether the code or the text is wrong, don't guess: list it in `docs/reviews/<run date>-docs-review.md` with the evidence and a proposed answer.
5. That file also lists each change you made, by file, with the code it now matches, and ends with a `## Draft issues` section for anything larger than a text fix. Don't file those issues; the steward decides.

## Constraints and acceptance

- Text only: documents, docstrings and comments. No change to code behaviour or tests. Leave task files, earlier reviews and the dated architecture review as they are.
- No deployment, import against a live service or CI run; this is a source and text check.
- Before merging, run the tests and checks the Rules and `AGENTS.md` (or the README) ask for, and show they pass unchanged.
- Memory: follow your launch prompt's memory rule, and run one heavy command (test suite, browser, build) at a time.
- Handoff: a short outcome and the checks run; detail goes in the review file and this task record.
- Acceptance: the review file is on `main`, every document named in step 1 was read, each change it lists names the code it now matches, and the test results match `main` before the change.

Tracker: [the palindromi.fi tracker](../../TASKS.md).


## Implementation record, 2026-10-22

The [documentation review] inventories all five original in-scope Markdown
files, all 20 Python sources, source/configuration comments, and every corrected
file with its matching code. Added a [development guide] to centralize command
scopes, data contracts and required checks. Tests, configuration and database
content are unchanged. The only executable-source change is the owner-approved
reordering of two existing standard-library imports.

The canonical start move was committed on main as `c82d6fb`, then this worktree
was rebased onto it. Baseline `origin/main` was the cached `edca600`; no fetch,
push, deployment, live import or CI run was attempted. Earlier task files and
reviews are unchanged; this appendix records the required evidence only.

### Verification

| Check | Main baseline | Reviewed candidate |
| --- | --- | --- |
| `uv run --no-sync pytest` | 39 passed | 39 passed, final rerun also passed |
| `uv run --no-sync pytest palindromi_fi_builder/tests/test_syncer.py` | 11 passed | 11 passed |
| `uv run --no-sync graylint --revision origin/main... -L flake8 -L mypy -L pylint ./palindromi_fi_builder` | exit 0 | exit 0, final rerun also passed |
| `uv run --no-sync darker --check --diff --isort --revision origin/main... ./palindromi_fi_builder` | exit 0 | exit 0 after the approved import-order exception |
| `uv run --no-sync make build` | exit 0; compiled JS and rendered | exit 0; all 64 output hashes identical, including 48 HTML pages |
| Executable AST comparison excluding docstrings | baseline recorded | identical for all 11 files after accounting for the exact approved import swap |
| Relative file/heading links | not applicable | 113 checked; 10 private-export targets unavailable, explicitly historical |
| `git diff --check` | clean | passed |

Frozen dependencies use CPython 3.11.16. Setup first failed because the host
sets Python downloads to never; enabling downloads alone still failed because
its Python preference is only-system. The command-local combination
`UV_PYTHON_DOWNLOADS=automatic UV_PYTHON_PREFERENCE=managed` succeeded. Neither
host setting was changed. Subsequent `uv run --no-sync` calls warn about the
host preference but use the verified 3.11.16 environment successfully.

The first link-check attempt rejected the unavailable private-export directory
because the checker recognized descendants but not the directory itself. Fixed
that temporary checker; the complete rerun passed. Automatic Ruff/ty edit hooks
also reported pre-existing code diagnostics; the executable-AST comparison
confirms those imports, annotations and statements are unchanged. No autofixes
were applied. Existing full-tree flake8/mypy debt and legacy `make lint` were not
rerun; they are outside the required incremental checks.

Synthetic local probes confirmed literal chomping, CRLF-to-LF scalar mutation,
phone-export blank-line loss, the parser's first-prefix rule and exception,
Syncer repeated-write/copy limitations, and nested-break failure in the legacy
API helper. Current curated and INBOX text/translation values contain no CR.
See the review's draft issues for proposed follow-ups; none were filed.

### Approved scope exception, 2026-10-22

The required Darker check initially requested a swap of
`from html.parser import HTMLParser` and `from pathlib import Path` in the
[HTML converter]. Darker's installed `apply_isort()` considers the span from
the first to last edited line, so docstring edits on both sides exposed the
existing unsorted import block. No suppression or configuration change was made.

The owner answered “Allow the import-order-only exception.” Swapped exactly
those two existing standard-library imports; the converter otherwise matches
the reviewed candidate in `6e39ded` byte for byte. Reran the full suite (39
passed), focused Syncer suite (11 passed), required Graylint and Darker commands,
and complete build: all passed. After allowing only that swap, the executable
AST comparison still matches baseline, and all 64 generated file hashes remain
identical. All required checks now match the main baseline's successful results.

The review's formatting draft was removed because it is resolved. The five
remaining draft issues are steward-owned follow-ups; none were filed. The
implementation is ready for local merge and the specified unchecked Hai
completion transition; their outcome will be recorded below.

### Guarded command memory record

Commands ran one at a time with a 120-second timeout unless noted (setup:
300 seconds; Graylint and build: 180 seconds). Admission waited up to ten
minutes for 2048 MiB available, with a 1536 MiB fallback; runtime limits were
1024 MiB available and at most 512 MiB swap growth. No command needed to wait,
use the fallback, or stop for memory. Measurements are MiB; elapsed and wait
are seconds. Output is deliberately excluded from this memory record.

| Run | Command | Outcome | Wait | Available start → final | Swap start / growth / peak growth | Elapsed | Completion |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| setup | `uv sync --frozen --python 3.11` | started at once | 0.0 | 2447.9 → 2437.7 | 2320.8 / +0.0 / 0.0 | 0.5 | exit 2 |
| setup-managed | `env UV_PYTHON_DOWNLOADS=automatic uv sync --frozen --python 3.11` | started at once | 0.0 | 2418.5 → 2417.8 | 2320.8 / +0.0 / 0.0 | 0.5 | exit 2 |
| setup-managed-preference | `env UV_PYTHON_DOWNLOADS=automatic UV_PYTHON_PREFERENCE=managed uv sync --frozen --python 3.11` | started at once | 0.0 | 2406.9 → 2519.2 | 2320.5 / +0.0 / 0.0 | 3.5 | exit 0 |
| baseline-tests | `uv run --no-sync pytest` | started at once | 0.0 | 2532.4 → 2507.0 | 2320.5 / +0.0 / 0.0 | 1.5 | exit 0 |
| baseline-syncer | `uv run --no-sync pytest palindromi_fi_builder/tests/test_syncer.py` | started at once | 0.0 | 2507.5 → 2489.3 | 2320.5 / +0.0 / 0.0 | 0.5 | exit 0 |
| baseline-graylint | `uv run --no-sync graylint --revision origin/main... -L flake8 -L mypy -L pylint ./palindromi_fi_builder` | started at once | 0.0 | 2489.2 → 2486.7 | 2320.5 / +0.7 / 1.0 | 47.6 | exit 0 |
| baseline-darker | `uv run --no-sync darker --check --diff --isort --revision origin/main... ./palindromi_fi_builder` | started at once | 0.0 | 2486.7 → 2482.3 | 2321.2 / +0.0 / 0.0 | 0.5 | exit 0 |
| baseline-build | `uv run --no-sync make build` | started at once | 0.0 | 2480.7 → 2475.3 | 2321.2 / +0.0 / 0.0 | 1.0 | exit 0 |
| baseline-probes | `.venv/bin/python /tmp/palindromi-docs-review-20261022/probes.py` | started at once | 0.0 | 2643.6 → 2621.1 | 2320.7 / +0.0 / 0.0 | 1.0 | exit 0 |
| post-tests | `uv run --no-sync pytest` | started at once | 0.0 | 2553.7 → 2522.3 | 2293.4 / +0.0 / 0.0 | 1.0 | exit 0 |
| post-syncer | `uv run --no-sync pytest palindromi_fi_builder/tests/test_syncer.py` | started at once | 0.0 | 2522.4 → 2505.4 | 2293.4 / +0.0 / 0.0 | 0.5 | exit 0 |
| post-graylint | `uv run --no-sync graylint --revision origin/main... -L flake8 -L mypy -L pylint ./palindromi_fi_builder` | started at once | 0.0 | 2505.4 → 2632.6 | 2293.4 / +1.8 / 1.8 | 27.6 | exit 0 |
| post-darker | `uv run --no-sync darker --check --diff --isort --revision origin/main... ./palindromi_fi_builder` | started at once | 0.0 | 2641.2 → 2623.3 | 2295.2 / +0.0 / 0.0 | 1.5 | exit 1 |
| post-build | `uv run --no-sync make build` | started at once | 0.0 | 2618.0 → 2609.5 | 2295.2 / +0.0 / 0.0 | 0.5 | exit 0 |
| post-equivalence | `.venv/bin/python /tmp/palindromi-docs-review-20261022/verify.py` | started at once | 0.0 | 2612.7 → 2612.3 | 2295.2 / +0.0 / 0.0 | 0.5 | exit 0 |
| followup-probes | `.venv/bin/python /tmp/palindromi-docs-review-20261022/followup-probes.py` | started at once | 0.0 | 2631.4 → 2627.0 | 2294.4 / +0.0 / 0.0 | 1.0 | exit 0 |
| document-links | `python3 /tmp/palindromi-docs-review-20261022/check-docs.py` | started at once | 0.0 | 2181.7 → 2195.7 | 2298.9 / +0.0 / 0.0 | 0.5 | exit 1 |
| final-tests | `uv run --no-sync pytest` | started at once | 0.0 | 2161.5 → 2142.5 | 2298.9 / +1.5 / 1.5 | 2.5 | exit 0 |
| final-graylint | `uv run --no-sync graylint --revision origin/main... -L flake8 -L mypy -L pylint ./palindromi_fi_builder` | started at once | 0.0 | 2138.9 → 2137.9 | 2300.4 / +16.5 / 16.5 | 57.2 | exit 0 |
| final-equivalence | `.venv/bin/python /tmp/palindromi-docs-review-20261022/verify.py` | started at once | 0.0 | 2137.3 → 2137.0 | 2316.9 / -0.2 / 0.0 | 1.0 | exit 0 |
| document-links-final | `python3 /tmp/palindromi-docs-review-20261022/check-docs.py` | started at once | 0.0 | 2200.8 → 2200.7 | 2316.6 / +0.0 / 0.0 | 0.5 | exit 0 |
| approved-tests | `uv run --no-sync pytest` | started at once | 0.0 | 2338.2 → 2326.5 | 2409.6 / +0.0 / 0.0 | 1.0 | exit 0 |
| approved-syncer | `uv run --no-sync pytest palindromi_fi_builder/tests/test_syncer.py` | started at once | 0.0 | 2324.6 → 2240.2 | 2409.6 / +0.0 / 0.0 | 1.0 | exit 0 |
| approved-graylint | `uv run --no-sync graylint --revision origin/main... -L flake8 -L mypy -L pylint ./palindromi_fi_builder` | started at once | 0.0 | 2244.2 → 2457.8 | 2409.6 / +36.0 / 36.2 | 35.1 | exit 0 |
| approved-darker | `uv run --no-sync darker --check --diff --isort --revision origin/main... ./palindromi_fi_builder` | started at once | 0.0 | 2462.0 → 2353.3 | 2445.6 / -0.2 / 0.0 | 1.5 | exit 0 |
| approved-build | `uv run --no-sync make build` | started at once | 0.0 | 2355.0 → 2336.9 | 2445.3 / +0.0 / 0.0 | 1.0 | exit 0 |
| approved-equivalence | `.venv/bin/python /tmp/palindromi-docs-review-20261022/verify.py` | started at once | 0.0 | 2343.0 → 2362.9 | 2445.3 / +0.0 / 0.0 | 0.5 | exit 0 |
| approved-document-links | `python3 /tmp/palindromi-docs-review-20261022/check-docs.py` | started at once | 0.0 | 2639.3 → 2715.5 | 2541.4 / +2.8 / 2.8 | 0.5 | exit 0 |

[documentation review]: ../reviews/2026-10-22-docs-review.md
[development guide]: ../development.md
[HTML converter]: ../../palindromi_fi_builder/adhoc/convert_zoho_html.py
