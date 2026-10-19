# Review palindromi.fi's architecture and docs, and draft the fixes

Steward issue, 2026-10-19 (spare quota, steward decisions D48 and D53:
whole-repository architecture review). Goal: learning-play; palindromi.fi is
tier 3. `main` took 63 commits since 2026-09-19 and has never had a
whole-repository review; the repository has no README.

## Work

1. Read `docs/`, `Makefile`, `pyproject.toml`, `.github/workflows/`, then
   `palindromi_fi_builder/` and `database/`.
2. Apply the `honey` principles with `honey-review` (speculative
   generality, hand-rolled stdlib, single-caller abstractions, dead code,
   narration) and `codebase-design` for deep modules: where a seam would
   make the builder smaller to change and easier to test.
3. Check `docs/` and the workflows against the code: list every statement
   or step the code contradicts.
4. Write `docs/reviews/2026-10-19-architecture-review.md`: findings ranked
   by benefit per hour, each with file and line evidence and a drafted
   issue (title, work, acceptance, about an agent hour each). Draft a short
   README as one of them. Mark drafts that overlap open issues in
   `TASKS.md` instead of duplicating them.

## Ground rules

- Read-only apart from the report and this issue's tracker moves. Don't
  file the drafts; the steward files them.
- No push and no deploy: `main` is ahead of GitHub on purpose, and pushing
  runs the Pages deploy, which is Antti's.

## Acceptance

- Every finding cites code on `main` and says what changes if it is fixed.
- The report names the three drafts it would do first, and why.
