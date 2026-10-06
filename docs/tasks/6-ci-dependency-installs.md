# Fix dependency installs in CI

- `.github/workflows/linting.yaml` installs `-e .[test]`, but `e0c712c` moved the
  test extra into the `dev` dependency group. The linting environment therefore
  lacks pytest and the type stubs.
- `deploy.yaml` runs an unpinned `pip install -e .` on Python 3.11 and ignores
  `uv.lock`. A simulated deploy installed click 8.6.0.dev0, ruamel.yaml 0.19.1 and
  transcrypt 3.9.5 instead of the locked versions. It still built.
- `formatting.yaml` runs darker 1.7.0 without setting `python-version`.
- The latest Linting and Formatting runs on `origin/main` failed. Reading the logs
  needs repo admin access, so check them in the Actions UI first.

Consider `astral-sh/setup-uv` with `uv sync --frozen` in all three workflows.

Darker and graylint compare against `origin/main...`, which is empty on a push to
`main`. They only check changed code in pull requests.

## Implementation and validation, 2026-10-06

All three workflows use `astral-sh/setup-uv@v10.2.0`, uv 0.12.17 and Python
3.11. Linting and Formatting run `uv sync --frozen` and invoke the locked
Graylint and Darker commands with `uv run --no-sync`. Deploy uses
`uv sync --frozen --no-dev` and `uv run --no-sync --no-dev make build`.
Darker 2.1.1 with color/isort extras and Graylint 1.1.1 with color support are
now dev dependencies. This Darker release includes Black as a core dependency.
The lock adds their dependencies and updates pathspec for Black; existing
Click, ruamel.yaml, Transcrypt and other package versions remain unchanged.

Validation on Python 3.11.16:

- Frozen dev and production installs succeeded; `uv lock --check` passed.
- Actionlint passed after excluding its existing checkout@v3 runner warning,
  which task 9 covers. No new workflow errors were reported.
- All 37 pytest tests passed.
- The production-only environment built the complete site with `make build`.
- Isolated Git fixtures confirmed Darker rejects a misformatted changed line
  and Graylint rejects an unused import with flake8 F401. Both exited with 1.
- Comparison against local main passes. Comparison against the older
  origin/main reports existing lint and formatting problems in the Zoho
  converter and a pylint warning in `__main__.py`. These are outside task 6.

The Actions UI was checked for Formatting run 37419669333 and Linting run
37419669373. It confirms exit codes 4 and 1 and missing Python-version
annotations. Both pages require sign-in to view logs, so the detailed failures
could not be confirmed. Tasks 7 and 8 retain responsibility for further CI
failures. The `origin/main...` comparison is preserved and remains empty on
pushes to main.

No `docs/deployment.md` exists. Deployment uses the existing GitHub Pages
workflow triggered by a push to main.
