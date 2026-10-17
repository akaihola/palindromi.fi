# Gather acceptance evidence for the 4 review-queue items

Steward issue, 2026-10-17 (decisions D7, D10 and D37 in
`/home/agent/my-knowledge/agents/steward/decisions.md`). It takes over
palindromi.fi's part of vault [17] and [20]. The vault's tracker is blocked, so
this check runs here, in the repository it checks. The verdicts feed the
steward's next digest, so that Antti can accept or reject these items with less
checking of his own.

## Items

These `- [ ]` items under `## Completed / Accepted`:

- [10] and the `setup-uv` cache-save `[*]`, with Hai timestamps. For [10], the
  evidence includes the GitHub Actions runs (`gh run list -R
  akaihola/palindromi.fi`); [11], the Ubuntu 26 validation branch, still waits
  for Antti's push and is not in scope.
- The Zoho import investigation `[*]` and the `zoho-history/` ignore and
  `uv.lock` `[*]`, legacy bullets.

Items whose Hai metadata has no `updatedAt` (it starts with 1970 in `hai-tasks
read`) are legacy bullets that predate Hai timestamps. Judge them against
today's `main`: find the commits that delivered each one (`git log -S`,
`--grep`, its description under `docs/tasks/`) and check that the behaviour
still exists. An item superseded by later work is "would accept" only when the
later work covers its request; name the issue that superseded it.

## Work

Run the test suite that the README or AGENTS.md documents once on current
`main`, and a targeted test wherever an issue names one. Check criterion 3 with
`git revert --no-commit` of an item's merge commits in a temporary worktree
(`git worktree add --detach "$TMPDIR/revert-check" main`, removed afterwards);
conflicts only in `TASKS.md` and `docs/tasks/` don't count.

For each item, record one line: issue, a one-line outcome, the evidence
(commits, files, test command with pass and fail counts) and a verdict under
`/home/agent/my-knowledge/agents/steward/acceptance-policy.md`:

- **would accept:** all four criteria hold; give the revert command;
- **left to Antti:** name the criterion or the "Always left to Antti" class;
- **not done:** say what is missing.

## Deliverable

A section `## Evidence, YYYY-MM-DD` in this description file, with the lines
grouped by verdict and the counts per verdict at the end.

## Ground rules

- Change no other issue's state or text, and never change `[ ]` to `[x]`: only
  Antti accepts.
- Don't push, deploy or restart services, and don't touch the vault or the
  running pacer.

## Acceptance

- Every listed item has a line with evidence and a verdict.
- Nothing outside this file and the issue's own tracker moves changed.

## Evidence, 2026-10-17

Checked against `main` at `4934313`. `origin/main` is at `c2c6c6f`, and the 16
commits after it are unpushed. They include all of [10] and the `setup-uv` fix.
The newest run in `gh run list -R akaihola/palindromi.fi` is for `c2c6c6f`, on
2026-10-16, so no GitHub run has tested either change.

Test suite on `main`, using the host's default CPython 3.14.7:

- `uv run pytest`: 39 passed, 0 failed.
- `uv run flake8 -j 1 palindromi_fi_builder`: 7 findings, six E501 and one
  W391, in `convert_zoho_html.py`, `format.py`, `test_typography.py` and
  `yaml_utils.py`.
- `uv run mypy .`: 177 errors in 7 files.

None of the four items changes Python code, so the flake8 and mypy findings say
nothing about them. [10] names a forced build as its validation.
`uv run --no-sync --no-dev make -B build` passed on `main` with CPython 3.11.11,
the version CI pins. Transcrypt 3.9.4 compiled and the build wrote 48 HTML files.
On CPython 3.14.7 Transcrypt aborts in `org.transcrypt.__runtime__`. CI is not
affected, but a local build has to use 3.11.

The revert checks ran in a temporary detached worktree of `main`, now removed.
Where a revert conflicted only in `TASKS.md` or `docs/tasks/`, the check kept
`main`'s version of those files.

### Would accept

- `[*]` Zoho import investigation. Legacy, no Hai timestamps. Outcome: the
  findings are in `docs/zoho-import.md`. It covers the export format, the
  misnamed exports, what v1142 contains and the database constraints, and its
  plan points to tasks 1 to 5. `AGENTS.md` marks the converter as broken and
  links the doc. Evidence: `2674fca` adds the doc and edits `AGENTS.md`.
  `7a2574f` moves the plan into `TASKS.md` and `docs/tasks/1` to `6`. Both are
  on `origin/main`. The 129-line doc and `AGENTS.md:64` are still on `main`, and
  the doc contains no email address or Zoho user id. No later issue superseded
  it. Open tasks 1, 2, 4 and 5 build on it. It cites local artifacts in
  `zoho-history/investigation-2026-10-05/`, which is git-ignored and absent on
  this host, so I did not check them. Revert: `git revert --no-commit 7a2574f
  2674fca`, then at the conflict stop `git checkout HEAD -- TASKS.md docs/tasks
  && git revert --continue`. It conflicts only in `TASKS.md` and
  `docs/tasks/{2,3,6}`. Reverting `2674fca` alone conflicts in
  `docs/zoho-import.md`, because `7a2574f` rewrote its Plan section.

### Left to Antti

- [10], Hai `updatedAt` 2026-10-17T07:40:14.640Z. Outcome: no Ubuntu 26 run
  happened. GitHub rejected the test branch push because the token lacks
  `workflow` scope. As a fallback, all four jobs are pinned to `ubuntu-24.04`
  with dated comments, and follow-up [11] is recorded. Evidence: the net change
  of `0a67cbd` and `7508892` replaces `ubuntu-latest` with `ubuntu-24.04` plus a
  comment in each job and leaves triggers and the deploy job as they were.
  `ff15226` records the outcome in `docs/tasks/10-ubuntu-26-runner.md` and adds
  [11]. The worker validated locally with frozen installs, a forced build, 39
  tests and actionlint. The forced build above passes on 3.11. The last Deploy
  run, 38931784745, logged `Image: ubuntu-24.04`, so the pin keeps the image CI
  last passed on. Revert is clean: `git revert --no-commit 7508892 0a67cbd`
  puts `ubuntu-latest` back in all four jobs. Adding the tracker commits
  `ff15226` and `6676a2d` conflicts only in `TASKS.md` and `docs/tasks/11-…`.
  Why left: "Always left to Antti", because the worker reported publishing
  blocked and remote CI unverified, and the pins only work after a public push
  with a token that has `workflow` scope. `origin/main` still runs on
  `ubuntu-latest`, so that push has to land before 2026-10-19 for the pins to
  matter. The description allows the fallback "if something fails"; here the
  push failed, not a workflow. Whether that counts is also Antti's call.
- `[*]` `setup-uv` cache-save warning, Hai `updatedAt`
  2026-10-17T07:42:15.804Z. Outcome: Deploy is now the only workflow that saves
  the shared uv cache, with `save-cache: "true"`. Its `pages` concurrency group,
  with `cancel-in-progress: false`, runs one Deploy at a time. Formatting and
  Linting set `save-cache: "false"` and only restore the cache. Evidence:
  `faf263c` adds 6 lines across the three workflows. The run logs for push
  `0aee125` confirm the cause. All three workflows used the same cache key.
  Formatting run 38931186754 saved it, and Deploy run 38931186757, the cited
  job, and Linting run 38931186772 both logged "Failed to save: Unable to
  reserve cache". `save-cache` is a setup-uv v10.2.0 input, default `auto`, in
  its `action.yml`. As the commit message says, Formatting and Linting now
  download their dev-only packages on every run. Revert is clean: `git revert
  --no-commit faf263c`. Why left: "Always left to Antti", because `faf263c`
  reports remote CI and Pages deployment as unverified. The change is unpushed
  behind the same token scope, so no run has shown the warning gone.
- `[*]` `zoho-history/` ignore and `uv.lock`. Legacy, no Hai timestamps.
  Outcome: delivered, and still in effect on `main`. Evidence: `c50c37c` adds
  `.gitignore` lines 7 to 9, and `git check-ignore -v` matches
  `zoho-history/…`, `.env` and `.claude/settings.local.json`. `80844e0` adds
  `requires-python = ">=3.11"`, which is in `pyproject.toml:11` and `uv.lock:3`.
  `uv.lock` is tracked and `uv lock --check` passes. Both commits are on
  `origin/main`. Criteria 1, 2 and 4 hold. Why left: criterion 3. `git revert
  --no-commit c50c37c` is clean, but `git revert --no-commit 80844e0` hits a
  modify/delete conflict in `uv.lock`. Accepted [6] (`b066d0b`) and the accepted
  `pkg_resources` item (`1b7c879`) re-locked it, and all three workflows run
  `uv sync --frozen` against it. Undoing the `uv.lock` half would break accepted
  work.

### Not done

None.

### Counts

- Would accept: 1
- Left to Antti: 3
- Not done: 0
