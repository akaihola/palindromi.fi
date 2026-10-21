# Issue tracking for palindromi.fi

Rules for TASKS.md usage are at the bottom of the file.

## Unverified proposals

- [*] Curate and publish the imported Zoho palindromes with translations and grading.
    - Depends on: [5]

## Ordered backlog

- [2] Rewrite the Zoho converter to order exports by their embedded version.
    - Depends on: [1]

- [5] Import the Zoho palindromes into the database.
    - Depends on: [1], [2], [3], [4]

## Scheduled

## In Progress

- [~] [11] Validate Ubuntu 26 workflows and remove Ubuntu 24.04 pins.
    - Depends on: [10]

      <!-- hai:{"id":"simple-4053a1a4-bd08-458a-8ec2-5e3f7c40f353","createdAt":"2026-10-17T07:39:51.958Z","updatedAt":"2026-10-21T04:42:07.172Z"} -->

- [~] [1] Refresh the Zoho exports before editing the note again.

- [~] [4] Decide the rules for importing Zoho palindromes.

## Completed / Accepted

- [x] [*] Delete the untracked `analyze_zoho_html.py` and
      `extract_zoho_revisions.py` from the repo root. Obsolete: Antti committed
      both scripts in `454fc17` on 2026-10-14 (B2, board clean-up, approved by
      Antti 2026-10-19).
      <!-- hai:{"id":"simple-87dd7661e7632a2b","updatedAt":"2026-10-21T05:29:48.764Z"} -->

- [x] [15] Add a short README and reconcile operating documentation
      <!-- hai:{"id":"simple-e47ca29e-3695-4c65-9673-739113afec90","labels":["steward"],"createdAt":"2026-10-19T11:18:17.859Z","updatedAt":"2026-10-19T14:05:43.503Z"} -->

- [x] [14] Make build rerender after any site input changes
      <!-- hai:{"id":"simple-4bea8bf7-7400-4913-a060-928d90ce4d05","labels":["steward"],"createdAt":"2026-10-19T11:18:17.273Z","updatedAt":"2026-10-19T14:05:43.787Z"} -->

- [x] [13] Review palindromi.fi's architecture and docs, and draft the fixes
      <!-- hai:{"id":"simple-c8564ae1-1f95-42f2-a18a-bd43861ddb6e","labels":["steward"],"createdAt":"2026-10-19T08:13:11.863Z","updatedAt":"2026-10-19T14:05:44.077Z"} -->

- [ ] [12] Gather acceptance evidence for the 4 review-queue items
      <!-- hai:{"id":"simple-a7fd5257-eb4d-44f3-bdd3-a1101c25f55a","labels":["steward"],"createdAt":"2026-10-17T20:09:28.739Z","updatedAt":"2026-10-17T20:21:10.684Z"} -->

- [ ] [*] Solve
  `Post Run astral-sh/setup-uv@v10.2.0 Failed to save: Unable to reserve cache with key setup-uv-2-x86_64-unknown-linux-gnu-ubuntu-24.04-3.11-607d7b8ed2ba5be0b3bfc7e58c92addb1438c976c37a6086996897ab76979748, another job may be creating this cache.`
  seen in in
  [build for MR #79](https://github.com/akaihola/palindromi.fi/actions/runs/38931186757/job/117075274768)
      <!-- hai:{"id":"simple-a04a202b0d896f17","updatedAt":"2026-10-17T07:42:15.804Z"} -->

- [x] [10] Get CI passing on Ubuntu 26 before `ubuntu-latest` switches on 2026-10-19.
    - Depends on: [9]

      <!-- hai:{"updatedAt":"2026-10-18T09:50:49.354Z"} -->

- [x] [9] Move the workflows to action versions that run on Node.js 24.
    - Depends on: [6], [7], [8]

  <!-- hai:{"updatedAt":"2026-10-17T07:09:32.992Z"} -->

- [x] [*] Fix the unintended `<nnnnn>.bin` download when tapping the page. A page tap
      must display the next palindrome and must not download a file.
      <!-- hai:{"id":"simple-2b77e5d9f1b0c0a9","updatedAt":"2026-10-15T20:36:52.107Z"} -->

- [x] [8] Fix the failing Formatting workflow.
    - Depends on: [6]

      <!-- hai:{"updatedAt":"2026-10-07T04:15:04.064Z"} -->

- [x] [7] Fix the failing Linting workflow.
    - Depends on: [6]

      <!-- hai:{"updatedAt":"2026-10-07T04:11:55.742Z"} -->

- [x] [*] Replace `pkg_resources.resource_filename` in `render.py` with
      `importlib.resources`. Recent setuptools no longer ships `pkg_resources`.
      <!-- hai:{"id":"simple-68788e48c58089d7","updatedAt":"2026-10-07T04:08:32.633Z"} -->

- [x] [*] Delete `lock.json` and `flake.lock`, left over from the Nix setup removed in
      `eaa78ee`.
      <!-- hai:{"id":"simple-cedf4f66511832e1","updatedAt":"2026-10-07T04:09:00.483Z"} -->

- [x] [6] Fix dependency installs in CI.
      <!-- hai:{"updatedAt":"2026-10-07T04:03:00.426Z"} -->

- [x] [3] Remove the reflowed duplicates that `3daa724` added to `INBOX.yaml`, before
      pushing `main`.
  <!-- hai:{"updatedAt":"2026-10-17T07:09:34.015Z"} -->

- [ ] [*] Investigate the unfinished Zoho import work and record the findings in
      `docs/zoho-import.md`.

- [x] [*] Ignore `zoho-history/`, `.env` and `.claude/settings.local.json`, and commit
      `uv.lock` with `requires-python = ">=3.11"`.
      <!-- hai:{"id":"simple-537e971dbd4914ab","updatedAt":"2026-10-21T05:29:51.074Z"} -->

[1]: docs/tasks/1-refresh-zoho-exports.md
[2]: docs/tasks/2-fix-zoho-converter.md
[3]: docs/tasks/3-remove-inbox-duplicates.md
[4]: docs/tasks/4-zoho-import-rules.md
[5]: docs/tasks/5-import-zoho-palindromes.md
[6]: docs/tasks/6-ci-dependency-installs.md
[7]: docs/tasks/7-fix-linting-workflow.md
[8]: docs/tasks/8-fix-formatting-workflow.md
[9]: docs/tasks/9-node24-actions.md
[10]: docs/tasks/10-ubuntu-26-runner.md
[*]: TASKS.md

<!-- hai:reserved-numbers:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -->

[11]: docs/tasks/11-validate-ubuntu-26-workflows-and-remove-ubuntu-24-04-pins.md

[12]: docs/tasks/12-gather-acceptance-evidence-for-the-4-review-queue-items.md

[13]: docs/tasks/13-review-palindromi-fi-s-architecture-and-docs-and-draft-the-fixes.md

[14]: docs/tasks/14-make-build-rerender-after-any-site-input-changes.md

[15]: docs/tasks/15-add-a-short-readme-and-reconcile-operating-documentation.md

## Rules

Here are the rules for TASKS.md usage:

### TASKS.md maintenance sessions

- In `## Completed / Accepted`, `- [ ] [N] summary` or `- [ ] [*] summary` means
  completed work awaiting user acceptance. `- [x] [N] summary` or `- [x] [*] summary`
  means the user has accepted it. Only user acceptance, or the steward's under its acceptance policy, changes `[ ]` to `[x]`;
  completion, tests and deployment do not.
- Move newly completed issues into `## Completed / Accepted` with `[ ]`.
- During the next maintenance run, remove only `[x]` issues from this section, plus
  their unused description files and reference-style links. Keep `[ ]` issues and any
  files or links still referenced by another issue.
- Each issue must retain either
    - a numbered reference-style link (e.g. `[1]`) to a description file, or
    - `[*]` to indicate no description file is needed for a simple task.
- `[~]` marks an issue that is actively in progress. When the issue is complete, move it
  to `## Completed / Accepted` with `[ ]`, pending user acceptance.
- Link references are listed between `## Completed / Accepted` and `## Rules`.
- Keep summaries concise. Move detailed requirements, rationale, examples and acceptance
  criteria into `docs/tasks/N-issue-description.md`; preserve simple tasks inline. Reuse
  an existing description for the same issue.
- For a new description, use the first unused number, checking both this file and
  description filenames in available Git history. Do not reuse numbers of accepted
  issues.
- Preserve Hai metadata comments during manual edits, including the reserved-number
  ledger that prevents identifier reuse after cleanup without Git history.
- The section records work status; the checkbox in `## Completed / Accepted` records
  user acceptance. Completed descriptions retain historical requirements, paths and
  validation results; they are not current implementation instructions. Date later
  corrections and distinguish regressions from earlier work.
- Any completed tasks which haven't yet been moved from `## In Progress` to
  `## Completed / Accepted` should be moved there.
- Any in progress tasks which haven't yet been moved from `## Ordered backlog` or
  `## Scheduled` to `## In Progress` should be moved there.
- Ensure there are no duplicate sections, and that they are in the correct order:
  `## Unverified proposals` -> `## Ordered backlog` -> `## Scheduled` ->
  `## In Progress` -> `## Completed / Accepted` -> `## Rules`.

### Modifying issues

- Ensure dependencies between issues are correctly updated.
- State dependencies using
    - indented `- Depends on: [N]` bullets in TASKS.md, and
    - YAML frontmatter in description files.
- Ensure backlog order respects dependencies.
- When you move an issue, preserve its identifier, text and line wrapping. Change only
  the status checkbox when completion or user acceptance requires it. This keeps moves
  identifiable in Git and reduces avoidable conflicts.

### Workflow for new issue completion

Git operations below apply only when this directory is a Git repository. Without Git,
use the working files, skip branch/commit/rebase/merge steps, and preserve the same
scheduling, implementation, validation, and acceptance transitions. Do not initialize a
repository just to satisfy these rules.

Below, `<filename>@<branch>` means operate on the file in the specified branch.

1. Choose issue and schedule work

- Pick the first issue in `TASKS.md@main` with no dependency on uncompleted work.
- Move it from `## Ordered backlog` to `## Scheduled` in `TASKS.md@main`, and commit
  when the Git workflow applies.

2. Work on the issue

- Move the issue to `## In Progress` in `TASKS.md@<worktree-branch>`, mark it `[~]`, and
  ensure no copy is left in the backlog or scheduled section.
- Create or update, review and refine `docs/tasks/N-issue-description.md` if the plan
  needs more than a concise bullet. Link a new description with a new `[N]`.
- Reword the summary if needed. Commit the description and tracker when applicable.
- Implement, test, review, and refine the work in the feature worktree when available.

3. Merge and deploy

- When Git applies, rebase the feature branch on `main`, resolve conflicts, and merge it.
- Keep the worktree and branch after merging. Remove them only when the user
  explicitly requests it.
- Move the issue to `## Completed / Accepted` with `[ ]`, pending user acceptance, and
  commit when applicable.
- Follow any deployment steps in `docs/deployment.md`.
