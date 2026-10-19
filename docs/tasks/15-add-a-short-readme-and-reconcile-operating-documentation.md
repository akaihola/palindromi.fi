Steward issue, 2026-10-19. Goal: learning-play; palindromi.fi is tier 3.

From draft C of `docs/reviews/2026-10-19-architecture-review.md` (the review in palindromi.fi [13]), which ranks it among the first to do. The draft follows as the reviewer wrote it; read the review's other sections only if this one points there.

## Draft

Estimate: 1 agent hour. High onboarding benefit. No open duplicate; preserve
completed task descriptions as historical evidence. Task [11] owns runner
migration, and tasks [1], [2], [4], [5] own pending import decisions.

Evidence: There is no tracked README. `AGENTS.md:14-24` recommends unqualified
uv setup and direct rendering. `pyproject.toml:11` permits every Python >=3.11,
but the working build uses 3.11 at `.github/workflows/deploy.yaml:27` and the
recorded Transcrypt 3.14 failure is in
`docs/tasks/12-gather-acceptance-evidence-for-the-4-review-queue-items.md:68-81`.
Direct render succeeded in this review but produced no
`static/__target__/palindrome.js`, which the template imports at
`palindromi_fi_builder/templates/palindrome.html:8`. Only Make compiles it at
`Makefile:11-16`. The exact text hash is truncated to four bytes at
`palindromi_fi_builder/database.py:107-112`.

Work: Add the short README drafted below, update AGENTS.md to point to the build
path, and reconcile the discrepancy inventory in this report. Explain which
commands operate on curated data versus drafts, and document that `load` emits
site data rather than a lossless database backup. Correct the project Home URL
at `pyproject.toml:34-35` to this repository. Keep historical task outcomes and
add dated corrections rather than rewriting their original requirements.

Acceptance: A fresh checkout follows the README on Python 3.11 and produces
HTML, navigation JavaScript and illustrations. All current commands match CLI
help. Deployment instructions identify the main-push trigger and Antti's
ownership. The discrepancy inventory has a documented resolution for each item.

What changes: The first build works and readers can distinguish current
instructions from investigation history.

Proposed README content, to be added only by the future issue:

```markdown
# palindromi.fi

A static Finnish palindrome collection with English translations and illustrations.

Use uv and Python 3.11 for the site build. The current Transcrypt build is known
not to work on Python 3.14.

    uv sync --frozen --python 3.11
    uv run --no-sync make build
    uv run --no-sync python -m http.server --bind 127.0.0.1 --directory html 8000

Open http://127.0.0.1:8000/. Re-run make build after editing content.

    uv run --no-sync pytest

Published entries live in database/palindromes/*.yaml. Filename and row order
set navigation; the last entry is the homepage. database/INBOX.yaml is unpublished.
Exact text, including newlines, determines existing page identifiers. Do not
normalize published text casually.

The builder loads YAML in database.py, renders Jinja templates in render.py,
and updates output through syncer.py. Make compiles keyboard navigation from
static/palindrome.py. The load subcommand dumps derived site data, not a backup.

See docs/zoho-import.md for the unfinished import and TASKS.md for work status.
The current Zoho converter output is unsafe to import.

Pushing main triggers GitHub Pages deployment. Publishing and deployment belong
to Antti; a local build does not require either.
```

The sentence about rerunning Make assumes draft A has landed. If C lands first,
use `uv run --no-sync make -B build` until A is complete.

## Steward's constraints

- Don't push or deploy; the site publishes from GitHub.

## Done when

The draft's acceptance holds, lint and tests pass, and the change is merged to `main` as the Rules describe. No push or deploy.

## Implementation and validation, 2026-10-19

Added the short README and the deployment guide referenced by tracker rules.
AGENTS now points to the complete Make build, explains curated versus draft
command scopes and derived `load` output, and documents incremental CI checks.
Corrected the project Home URL. Added dated dispositions for all 17 review
inventory items and corrections to import and completed CI notes, preserving
original requirements, outcomes and acceptance states. Task 14 already landed,
so the README uses `make build` without `-B`.

Validation with CPython 3.11.16 and frozen dependencies:

- A fresh temporary copy of tracked sources plus these documentation changes,
  without an environment or compiled assets, passed the README's sync and build.
  This host configures uv to use only system interpreters, so the clean-copy
  check set `UV_PYTHON_PREFERENCE=managed` to discover its installed Python 3.11.
  No repository setup configuration was changed.
- Output contained 48 HTML pages, navigation JavaScript and five illustrations.
  Every local HTML link and asset reference resolved. The exact README server
  command returned HTTP 200 for the homepage, JavaScript and an illustration.
- All 39 pytest tests passed. Incremental Graylint with flake8, mypy and pylint,
  and Darker's formatting check passed against `origin/main...`.
- CLI help confirmed render, load, format and both HTTP servers' arguments.
  INBOX count was verified as 109 rows, all graded.
- `git diff --check` passed. No Python implementation or dependency lock changed.

Full-tree flake8 with `.venv` excluded still reports 28 existing findings: seven
inside the package and 21 in the two tracked root investigation scripts. The
review's seven-finding count covered the package. An unqualified invocation also
scans the local virtualenv because the existing exclude setting replaces default
exclusions; that run was stopped. These are baseline findings outside this docs
change, not a failure of the passing incremental lint check. Full mypy was not
repeated; the review records its existing baseline errors. Draft I and the
existing script-cleanup issue retain ownership.

No push or deployment was performed. Completion requires a local merge to main
and the tracker move to Completed / Accepted with `[ ]`, pending acceptance.
