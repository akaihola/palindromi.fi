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
