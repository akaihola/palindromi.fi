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
