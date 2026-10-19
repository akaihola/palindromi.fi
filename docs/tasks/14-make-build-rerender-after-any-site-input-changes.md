Steward issue, 2026-10-19. Goal: learning-play; palindromi.fi is tier 3.

From draft A of `docs/reviews/2026-10-19-architecture-review.md` (the review in palindromi.fi [13]), which ranks it among the first to do. The draft follows as the reviewer wrote it; read the review's other sections only if this one points there.

## Draft

Estimate: 0.75 agent hour. High benefit, tiny implementation. No open overlap.

Evidence: `Makefile:9-21` makes index.html depend on compiled JavaScript, the
*directory* containing templates and top-level Python files. Existing template
contents, database YAML, illustration bytes, static CSS and CNAME are absent
from that dependency set. In a temporary clean copy, `make build` succeeded;
after touching each of a published YAML file, main.css and palindrome.html,
`make -n build` said `Nothing to be done for 'build'.` The default `all` target
also cleans everything at `Makefile:3-7`, defeating timestamp preservation.

Work: Make `build` always invoke the incremental renderer after ensuring the
JavaScript exists. Declare command targets phony. Keep `clean` explicit and
avoid maintaining an expanding list of content prerequisites. Do not change
Syncer's unchanged-file behavior.

Acceptance: In a temporary output tree, build twice and retain unchanged page
mtimes; edit YAML, CSS, an illustration and an existing template and see each
change in the next build. Adding or deleting a published entry removes obsolete
pages and updates navigation. Plain `make` does not silently force a clean.

What changes: Contributors can trust local builds after content edits.

## Steward's constraints

- Don't push or deploy; the site publishes from GitHub.

## Done when

The draft's acceptance holds, lint and tests pass, and the change is merged to `main` as the Rules describe. No push or deploy.

## Result, 2026-10-19

`build` now depends only on the compiled JavaScript and always runs
`python -m palindromi_fi_builder render`; Syncer keeps unchanged files untouched.
`all` builds without cleaning. `all`, `build`, `clean` and `lint` are phony. The
Transcrypt rule still rebuilds only when `static/palindrome.py` changes.

Validation in a throwaway copy of the worktree with a CPython 3.11.15 venv, using
`uv run --no-sync --no-dev make`:

- Plain `make -n` lists the render and no `rm`. A first plain `make` wrote 64
  files (48 top-level pages). A second plain `make` and a `make build` changed
  no file's mtime or content.
- Editing a translation in `02-additional.yaml` changed one page. Appending to
  `main.css` changed only `static/main.css`. Appending bytes to `neito.jpg`
  changed only its `static/*.jpg` copy. Adding a comment to `palindrome.html`
  changed all 48 pages and nothing else. No unchanged file was rewritten.
- Appending a new entry to `99-illustrated.yaml` added its page and updated
  `index.html` and the pages of its two neighbours, both of which link to it.
  Removing the entry deleted the page and restored those three files to their
  earlier content, with no remaining links to it.
- The old Makefile, run against the same copy, printed "Nothing to be done for
  'build'" after touching the YAML, CSS, template and illustration. The new one
  renders.
- `make clean` still empties `html/` and removes `static/__target__`.
- `uv run pytest`: 39 passed. `graylint --revision main... -L flake8 -L mypy -L
  pylint ./palindromi_fi_builder` (the CI lint gate) exits 0. No Python file
  changed, so whole-tree flake8 and mypy failures are the same as on `main`.
