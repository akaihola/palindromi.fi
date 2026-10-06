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
