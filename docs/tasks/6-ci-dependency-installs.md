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
