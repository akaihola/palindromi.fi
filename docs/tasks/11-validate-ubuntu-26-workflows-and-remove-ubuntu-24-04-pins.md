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

## Validation retry, 2026-10-19

Rebased the validation candidate onto current main, `edca600`, and prepared
`validate-ubuntu-26-issue-11-retry` at `444e623`. The branch targets Ubuntu 26
for Formatting, Linting and Deploy's build job, omits the deploy job, and
preserves Python 3.11 and frozen installs. `git diff --check main` passed.

Both the configured Git credential helper and an explicit retry using
`gh auth git-credential` were rejected by GitHub with the same error:

```text
refusing to allow a Personal Access Token to create or update workflow
`.github/workflows/deploy.yaml` without `workflow` scope
```

No remote validation branch or Actions runs were created. Ubuntu 26 runner
image versions, Transcrypt, site rendering and deployment remain unverified.
Issue 11 stays In Progress and all four Ubuntu 24.04 pins remain. The token
used for publishing still needs workflow permission before validation can resume.

## Manual publishing succeeded, 2026-10-19

Antti manually pushed `validate-ubuntu-26-issue-11-retry` at `444e623`.
The remote branch is confirmed. Workflow publishing is no longer blocking
this validation candidate. GitHub created these runs:

- [Formatting](https://github.com/akaihola/palindromi.fi/actions/runs/39279782382)
- [Linting](https://github.com/akaihola/palindromi.fi/actions/runs/39279782024)
- [Deploy, build only](https://github.com/akaihola/palindromi.fi/actions/runs/39279782145)

As of 15:43 UTC, all three runs remain queued with no executed steps or
assigned runner image versions. Earlier Ubuntu 24.04 main jobs are also
queued without assigned runners. This is pending validation, not evidence
of Ubuntu 26 compatibility or failure. Keep issue 11 In Progress and retain
the normal workflows' Ubuntu 24.04 pins until the three validation runs pass.
Then restore normal triggers and the deploy job on Ubuntu 26 and verify main
deployment before completing the issue.

## Partial validation results, 2026-10-19

[Linting](https://github.com/akaihola/palindromi.fi/actions/runs/39279782024)
and [Formatting](https://github.com/akaihola/palindromi.fi/actions/runs/39279782382)
completed successfully on commit `444e623`. Both Set up job logs report
Ubuntu 26.04.1, image `ubuntu-26.04`, image version `20261012.163.1`.
The runner image provisioner reports version `20261012.601`.

At 16:12 UTC the build-only Deploy run remains queued. Transcrypt, rendered
site output and main deployment are still pending validation. Keep all four
normal Ubuntu 24.04 pins and issue 11 In Progress until the remaining required
validation succeeds.

## Monitoring cutoff, 2026-10-19

At 16:16 UTC the [build-only Deploy run](https://github.com/akaihola/palindromi.fi/actions/runs/39279782145)
remains queued, beyond the requested 16:15 UTC monitoring cutoff. The temporary
two-minute monitoring schedule has been disabled. The existing run was left
intact; no duplicate run was started. Linting and Formatting passed, but
Transcrypt and site rendering on Ubuntu 26 remain unverified until this build
finishes. No normal runner pins were changed and no main deployment was
verified. Issue 11 remains In Progress. Resume by inspecting the existing build
run, then continue the remaining validation and rollout requirements.

## Validation passed and rollout prepared, 2026-10-21

The existing [build-only Deploy run][ubuntu26-build] is now confirmed successful,
alongside [Formatting][ubuntu26-format] and [Linting][ubuntu26-lint], all at
commit `444e623`. No run was retried. All three used Ubuntu 26.04.1, image
`ubuntu-26.04`, image version `20261012.163.1`. The build reports runner
`2.337.0` and image provisioner `20261012.601`.

The build log confirms CPython 3.11.16 and Transcrypt 3.9.4:
`transcrypt -b -m -n` completed with `Ready`, followed by the site renderer.
The Pages artifact upload succeeded, artifact ID `12202377027`, 534510 bytes.
This verifies compilation, rendering and artifact production on Ubuntu 26.

The [Deploy workflow][deploy-workflow], [Formatting workflow][format-workflow]
and [Linting workflow][lint-workflow] now use Ubuntu 26.04 for all four jobs.
Removed the dated fallback comments. Normal main/PR triggers, the deploy job,
Python 3.11, frozen installs, cache settings and concurrency are preserved.
Updated the [deployment instructions][deployment-guide].

Local validation with Python 3.11.16 passed all 39 tests and the complete
`uv run --no-sync make build`, including Transcrypt compilation. Parsed YAML
comparison against main verified that runner labels are the only semantic
workflow changes. Generated index HTML and navigation JavaScript exist.
`git diff --check` passed. Commands ran sequentially under the requested
memory/swap limits.

Publishing belongs to Antti; no push was attempted. The rollout is prepared
for local merge to main. After Antti pushes main, verify the new Deploy run,
record its URL and both jobs' actual image versions, and only then move this
issue to Completed / Accepted with an unchecked acceptance box.
Issue 11 remains In Progress because main deployment on Ubuntu 26 is still
an unmet completion requirement.

[ubuntu26-build]: https://github.com/akaihola/palindromi.fi/actions/runs/39279782145
[ubuntu26-format]: https://github.com/akaihola/palindromi.fi/actions/runs/39279782382
[ubuntu26-lint]: https://github.com/akaihola/palindromi.fi/actions/runs/39279782024
[deploy-workflow]: ../../.github/workflows/deploy.yaml
[format-workflow]: ../../.github/workflows/formatting.yaml
[lint-workflow]: ../../.github/workflows/linting.yaml
[deployment-guide]: ../deployment.md
