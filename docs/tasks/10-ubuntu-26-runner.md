---
depends-on: [9]
---

# Get CI passing on Ubuntu 26 before `ubuntu-latest` switches on 2026-10-19

All three workflows use `runs-on: ubuntu-latest`. GitHub starts moving that label to
Ubuntu 26 on 2026-10-19 (https://github.com/actions/runner-images/issues/14748).

Things that may break:

- Any job that does not pin Python gets the new image's default Python.
- `make build` runs `transcrypt`, which may not support that Python.
- `actions/setup-python` may not offer Python 3.11 for Ubuntu 26 yet. Deploy pins
  3.11.

Run each workflow once with `runs-on: ubuntu-26.04`. Deploy only runs on pushes to
`main`, so test its `build` job on a branch without the `deploy` job. If something
fails and the fix is not quick, pin `ubuntu-24.04` with a dated comment saying why and
add a follow-up task.

Done when all three workflows pass on Ubuntu 26, or are pinned to `ubuntu-24.04` with
the follow-up task recorded.

## Fallback implementation and validation, 2026-10-17

Dependency task 9 is accepted. All three workflows already use setup-uv with
Python 3.11 and frozen dependencies, so neither the image's default Python nor
setup-python's available versions applies to the current configuration.

Prepared all three workflows with `runs-on: ubuntu-26.04` and branch push
triggers, removing Deploy's deploy job for that test. GitHub rejected
`git push -u origin HEAD` before creating the branch:

```text
refusing to allow a Personal Access Token to create or update workflow
`.github/workflows/deploy.yaml` without `workflow` scope
```

No Ubuntu 26 workflow ran. This is a publishing blocker, not evidence of an
Ubuntu 26 incompatibility. Applied the requested fallback rather than leaving
CI exposed to the label migration: all four jobs now pin `ubuntu-24.04` with
dated comments referencing follow-up [11]. Normal triggers and the Deploy job
are restored. Task 11 records the remaining Ubuntu 26 checks and pin removal.

The last successful production [Deploy run 38931784745](https://github.com/akaihola/palindromi.fi/actions/runs/38931784745)
logs Ubuntu 24.04.5 and `Image: ubuntu-24.04`, confirming this pins the
previously tested image family.

Validation on this host with CPython 3.11.16:

- Frozen production installation passed.
- `uv run --no-sync --no-dev make -B build` passed, forcing Transcrypt 3.9.4
  recompilation and rendering the complete site.
- Frozen dev installation and all 39 pytest tests passed.
- Actionlint v1.7.12 and `git diff --check` passed.
- No Python code or dependency lock changed.

The fallback satisfies the implementation criterion, pending user acceptance.
Publishing and deployment remain blocked by the token's missing workflow
permission. The pins only protect remote CI after these commits are pushed.
No deployment guide exists; a push to main runs the Pages deployment workflow.
