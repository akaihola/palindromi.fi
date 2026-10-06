---
depends-on: [6]
---

# Fix the failing Formatting workflow

The `darker` job in `.github/workflows/formatting.yaml` fails in the
`akaihola/darker@1.7.0` step with exit code 4. It failed on `ece255e` (2025-12-06)
and again on `010167c` (run 37419669333, 2026-10-06).

Likely cause, to confirm in the log (the Actions UI, since the `gh` token on atom gets
HTTP 403 for logs):

- Exit code 4 is Darker's `EXIT_CODE_DEPENDENCY`.
- The workflow uses the 1.7.0 action with `version: "@master"`. That action installs
  `darker[color,isort]` from Darker's `master` branch, where Black is now an optional
  `black` extra. Black is therefore missing.
- The 1.7.0 action script imports `pkg_resources`, which recent setuptools no longer
  ships. Expect that to break next.

Pin the action and Darker to one current release, and add the `black` extra if that
release needs it. Darker is not in the `dev` dependency group, so if task 6 moves CI
to `uv sync --frozen`, decide whether to add it there.

`actions/setup-python@v4` has no `python-version`; set it. Like Linting, the job
compares against `origin/main...` and so only checks pull requests.

Done when the workflow passes on a push to `main`, and a misformatted line in a
pull request or a local run of the same command makes it fail.

## Investigation, 2026-10-06

The CLI token in this worktree downloaded the log of
[run 37419669333](https://github.com/akaihola/palindromi.fi/actions/runs/37419669333)
with `gh run view 37419669333 --log-failed`. It confirms the likely cause above.
The 1.7.0 action built `darker-3.0.0` from `master` into a Python 3.12
environment without Black and crashed before checking anything:

```text
ModuleNotFoundError: No module named 'black'
darker.exceptions.DependencyError: Can't find the Black package
##[error]Process completed with exit code 4.
```

Task 6 already implements the fix. The workflow installs the frozen dev group
on Python 3.11 and runs Darker 2.1.1 from `uv.lock` with `uv run --no-sync`.
That release depends on Black directly, so no `black` extra is needed; the lock
resolves Black 26.10.0, isort 7.0.0 and Darkgraylib 1.2.1. The 1.7.0 action
and its `pkg_resources` import are gone from the workflow. `origin/main...` is
preserved, so pushes to main compare against an empty diff.

## Local validation and remaining check, 2026-10-06

`uv sync --frozen --python 3.11` installed the locked dev environment on
CPython 3.11.16. The exact workflow command exited 0 with `main...` as the
revision, which matches a push to main where `origin/main...` is empty:

```bash
uv run --no-sync darker --check --diff --isort --color \
  --revision origin/main... ./palindromi_fi_builder
```

Against the stale `origin/main` at `ece255e` the same command exits 1 and
prints the reformatting of the Zoho converter that task 6 recorded as
pre-existing. In a temporary clone, committing a new
`palindromi_fi_builder/format_failure_probe.py` containing
`def   probe( a,b ):` made the command exit 1 and print the Black diff for
that file. The clone was removed; the probe never entered this repository.

Remote validation remains blocked for the same reason as task 7: local main
already carries unpublished commits, and pushing would publish unrelated work
and trigger deployment. Keep task 8 In Progress until the Formatting workflow
passes on a push to main, then move it to Completed / Accepted with `[ ]`.
