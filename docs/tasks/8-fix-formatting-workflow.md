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
