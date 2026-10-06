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

- [*] Replace `pkg_resources.resource_filename` in `render.py` with
  `importlib.resources`. Recent setuptools no longer ships `pkg_resources`.

- [*] Delete `lock.json` and `flake.lock`, left over from the Nix setup removed in
  `eaa78ee`.

## Scheduled

- [6] Fix dependency installs in CI.
  <!-- hai:{"updatedAt":"2026-10-06T16:10:19.339Z"} -->

## In Progress

- [~] [1] Refresh the Zoho exports before editing the note again.

- [~] [4] Decide the rules for importing Zoho palindromes.

- [~] [*] Delete the untracked `analyze_zoho_html.py` and `extract_zoho_revisions.py`
  from the repo root.

## Completed / Accepted

- [ ] [3] Remove the reflowed duplicates that `3daa724` added to `INBOX.yaml`, before
  pushing `main`.
  <!-- hai:{"updatedAt":"2026-10-06T16:06:17.092Z"} -->

- [ ] [*] Investigate the unfinished Zoho import work and record the findings in
  `docs/zoho-import.md`.

- [ ] [*] Ignore `zoho-history/`, `.env` and `.claude/settings.local.json`, and commit
  `uv.lock` with `requires-python = ">=3.11"`.

[1]: docs/tasks/1-refresh-zoho-exports.md
[2]: docs/tasks/2-fix-zoho-converter.md
[3]: docs/tasks/3-remove-inbox-duplicates.md
[4]: docs/tasks/4-zoho-import-rules.md
[5]: docs/tasks/5-import-zoho-palindromes.md
[6]: docs/tasks/6-ci-dependency-installs.md
[*]: TASKS.md

<!-- hai:reserved-numbers:1,2,3,4,5,6 -->

## Rules

Here are the rules for TASKS.md usage:

### TASKS.md maintenance sessions

- In `## Completed / Accepted`, `- [ ] [N] summary` or `- [ ] [*] summary` means
  completed work awaiting user acceptance. `- [x] [N] summary` or `- [x] [*] summary`
  means the user has accepted it. Only user acceptance changes `[ ]` to `[x]`;
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

- When Git applies, rebase the feature branch on `main`, resolve conflicts, merge it,
  and remove the worktree and branch.
- Move the issue to `## Completed / Accepted` with `[ ]`, pending user acceptance, and
  commit when applicable.
- Follow any deployment steps in `docs/deployment.md`.
