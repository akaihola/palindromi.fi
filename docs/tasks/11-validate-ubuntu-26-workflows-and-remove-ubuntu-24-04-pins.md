---
depends-on: [10]
---

# Validate Ubuntu 26 workflows and remove Ubuntu 24.04 pins

Task 10 pinned all four jobs in the three workflows to Ubuntu 24.04 on
2026-10-17 because GitHub rejected the Ubuntu 26 test branch push. The configured
Personal Access Token cannot create or update workflow files without workflow
scope. No Ubuntu 26 job ran, so compatibility remains unverified.

Once workflow publishing is available:

- Run Formatting and Linting once on `ubuntu-26.04`.
- Run Deploy's build job on `ubuntu-26.04` from a branch without its deploy job.
- Keep setup-uv's explicit Python 3.11 and frozen installs. Verify Transcrypt and
  the rendered site build. Fix any Ubuntu 26 failures.
- After all three pass, replace every `ubuntu-24.04` pin with `ubuntu-26.04`,
  remove the dated fallback comments, restore the normal workflow triggers and
  Deploy job, and verify deployment on main.
- Record run URLs and actual runner image versions here.
