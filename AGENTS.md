# Agent guidance

This repository builds palindromi.fi from curated YAML, Jinja templates and
Transcrypt navigation code. Use the [quick start](README.md) for the supported
Python 3.11 setup and complete local build.

- Read the [development guide](docs/development.md) for command scopes, defaults,
  source layout and required local checks. Run the full pytest suite, the
  incremental Graylint and Darker commands, and a complete build before handoff.
- Keep published text exact: it determines identifiers. The
  [data contract](docs/development.md#data-and-rendering) explains navigation,
  omitted editorial fields and the formatter's newline caveat.
- Follow the [deployment guide](docs/deployment.md) and the current task's
  publishing constraints. Antti owns publishing and deployment.
- The [Zoho import notes](docs/zoho-import.md) distinguish current work from
  historical findings. The existing converter's output is unsafe to import.
- Follow the [tracker rules](TASKS.md#rules). Completed task descriptions and
  dated reviews record history, not current implementation instructions.

Python formatting uses Darker with isort, configured in
[pyproject.toml](pyproject.toml). Keep changes within the requested scope;
known full-tree lint findings are not a request to clean up unrelated code.
