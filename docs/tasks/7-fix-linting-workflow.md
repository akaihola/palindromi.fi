---
depends-on: [6]
---

# Fix the failing Linting workflow

The `graylint` job in `.github/workflows/linting.yaml` fails in the
`akaihola/graylint@action-extra-packages` step with exit code 1. It failed on
`ece255e` (2025-12-06) and again on `010167c` (run 37419669373, 2026-10-06), so the
Zoho commits did not cause it.

- Read the log first. The `gh` token on atom gets HTTP 403 for run logs, so open the
  run in the Actions UI.
- Task 6 may fix part of this. It covers the `-e .[test]` extra that `e0c712c` moved
  into the `dev` dependency group.
- `actions/setup-python@v4` has no `python-version`, so the job runs on whatever Python
  the runner image ships.
- The action comes from graylint's `action-extra-packages` branch, not a release. Pin
  a release if one has the `extra_packages` input.
- `revision: "origin/main..."` is empty on a push to `main`, so the job only checks
  pull requests. Keep that unless there is a reason to lint all of `main`.

Done when the workflow passes on a push to `main`, and a deliberate flake8 error in
a pull request or a local run of the same command makes it fail.

## Investigation, 2026-10-06

The Actions UI for [run 37419669373](https://github.com/akaihola/palindromi.fi/actions/runs/37419669373)
requires sign-in to view logs. Unlike the token on atom, the CLI token in this
worktree can download them with `gh run view 37419669373 --log-failed`.
The action installed Graylint 0.0.1 from `action-extra-packages` with
Darkgraylib 2.4.1, then crashed before linting:

```text
ImportError: cannot import name 'shlex_join' from 'darkgraylib.git'
```

The log also confirms Python 3.12 and warnings that neither Graylint's `color`
extra nor the project's `test` extra exists in those installations. The 2025
run 19992127293 logs are unavailable, returning HTTP 410.

Task 6 already implements the fix. The workflow installs the frozen dev group
on Python 3.11 and runs Graylint 1.1.1 with Darkgraylib 1.2.1 from `uv.lock`.
The [v1.1.1 action](https://github.com/akaihola/graylint/blob/v1.1.1/action.yml)
has no `extra_packages` input. Keep the locked CLI rather than restoring the
branch action. No additional workflow change is needed. Preserve
`origin/main...` so pushes to main compare against an empty diff.

A fresh `uv sync --frozen --python 3.11` installed the locked dev environment
on CPython 3.11.16, and `uv lock --check` passed. This host requires
`UV_PYTHON_DOWNLOADS=automatic UV_PYTHON_PREFERENCE=managed` to select managed
Python; GitHub's setup-uv step selects Python 3.11 explicitly.

## Local validation and remaining check, 2026-10-06

In a temporary clone of local main, the exact workflow command passed with
HEAD equal to `origin/main`, exiting 0:

```bash
uv run --no-sync graylint --color --revision origin/main... \
  -L flake8 -L mypy -L pylint ./palindromi_fi_builder
```

Committing a new `palindromi_fi_builder/lint_failure_probe.py` containing
`import os` in that clone made the same command exit 1 with flake8 F401 and
pylint W0611. The temporary clone was removed; the probe never entered this
repository. `git diff --check` also passed.

Remote validation remains blocked. Local main already contained 28 unpublished
commits at the start of this task. Pushing main would publish unrelated work
and trigger deployment. No push was made without approval for that expanded
scope. Keep task 7 In Progress until the Linting workflow passes on a push to
main, then move it to Completed / Accepted with `[ ]`. No deployment guide
exists; the GitHub Pages workflow deploys automatically on pushes to main.
