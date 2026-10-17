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

## Validation attempt, 2026-10-17

Workflow publishing remains blocked. Prepared local branch
`validate-ubuntu-26-issue-11`, commit `74c38c5`, with all three workflows on
`ubuntu-26.04`, push triggers targeting that branch, and Deploy's deploy job
removed. Explicit Python 3.11, frozen installs and the shared-cache writer
settings are preserved. The candidate passes `git diff --check`.

Publishing the candidate with
`git push origin HEAD:refs/heads/validate-ubuntu-26-issue-11` failed:

```text
refusing to allow a Personal Access Token to create or update workflow
`.github/workflows/deploy.yaml` without `workflow` scope
```

`git ls-remote --heads origin validate-ubuntu-26-issue-11` returned no branch,
and `gh run list --branch validate-ubuntu-26-issue-11` returned no runs.
There are no Ubuntu 26 run URLs or actual runner image versions to record.
Transcrypt and site rendering have not been verified on Ubuntu 26. Local
builds cannot establish hosted-runner compatibility, so they were not repeated.

Issue 11 remains In Progress. The normal workflows retain all four Ubuntu
24.04 pins and fallback comments. No main deployment was triggered. Resume
with credentials permitted to publish workflow files, run the retained
validation branch, then remove the fallback pins only after all three runs
pass. Record each run URL and its Set up job image version, restore the normal
triggers and deploy job, and verify deployment on main before completion.
