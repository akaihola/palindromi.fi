# Architecture and documentation review, 2026-10-19

Reviewed local `main` at `a509ce29bfd2f27fbc50d0ad3db747ee764f9f54`.
Its application, database, workflow and documentation files match the starting
worktree at `1561c4d985e6240385ac45c7e8cb5af6666dd19f`; only TASKS.md differs.
All file and line references below refer to that main snapshot, not GitHub's
older main. No proposed fix was implemented or filed.

## What I would do first

1. Draft A, make local builds reflect every input. A successful command currently
   leaves edited content unpublished locally. The fix is small and easy to prove.
2. Draft B, run tests and a site build before merge. This protects the complete
   publishing path, including data-only changes that Python linters cannot check.
3. Draft C, add the README below and correct current operating guidance. It gives
   the next contributor a working build command and makes deployment ownership
   explicit. It also prevents repeatedly rediscovering the Python constraint.

These are ranked by expected benefit per agent hour, not by maximum possible
impact. Draft D is next because validation becomes more valuable as the Zoho
import grows. Estimates include focused tests and review; none includes remote
publishing, deployment, or waiting for editorial decisions.

## Architecture worth keeping

This is a small pipeline, not a framework candidate. Three published YAML files
supply 47 entries. The 109 INBOX entries are intentionally separate. The loader
sorts filenames and preserves row order, converts rows to site dictionaries,
then makes circular links. The last row becomes the homepage. Dates do not sort
the site. See `palindromi_fi_builder/database.py:75-97` and
`palindromi_fi_builder/render.py:59-76`.

Rendering copies package static assets, gives illustrations identifier-based
names, writes one page per identifier and copies the last page to index.html.
Syncer compares bytes, preserves unchanged timestamps and removes obsolete
output. Keep that useful behavior even though deployment now uploads a complete
Pages artifact, rather than running gsutil. See
`palindromi_fi_builder/render.py:64-110`,
`palindromi_fi_builder/syncer.py:56-125`, and
`.github/workflows/deploy.yaml:30-50`.

The useful deep-module boundary is the published-database loader: hide YAML
shape checks, source locations, identifier uniqueness and navigation construction
behind its existing small interface. The useful rendering boundary is a configured
page renderer that owns its template and typography rules. Click should only
translate options and errors; filesystem synchronization should remain separate.
Neither boundary needs a plugin system, repository class, generic storage layer,
or new configuration model. Split functions where it makes fixtures smaller,
not merely to move lines between files.

Honey and honey-review were applied to the whole snapshot. The named
`codebase-design` skill was not installed in the supplied catalog or local skill
search; the deep-module criteria explicitly given in this issue were applied
directly. This is a manual repository review, not a claim to have run that skill.

## Ranked issue drafts

Each letter is a report-local draft identifier, not a new tracker issue.

### A. Make build rerender after any site input changes

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

### B. Test and build the site on pull requests without deploying

Estimate: 1 agent hour. High benefit across all future changes. Touches the same
workflow files as open task [11], but is a separate behavior change; coordinate
with [11] and retain its Ubuntu pins until its own validation succeeds.

Evidence: `.github/workflows/linting.yaml:26-31` runs only Graylint;
`.github/workflows/formatting.yaml:26-31` runs only Darker. No workflow runs
pytest. `.github/workflows/deploy.yaml:3-6,30-50` builds only after a main push
and immediately makes the artifact eligible for deployment. The two existing
render tests check copied CSS and HTML navigation, not compiled JavaScript
availability, at `palindromi_fi_builder/tests/test_render.py:10-67`.

Work: Add a nondeploying PR check using frozen dependencies and Python 3.11,
running pytest and a clean `make build`. Check that generated navigation targets,
illustrations and the imported JavaScript exist. Share the existing build
command rather than writing a second Python build implementation. Preserve the
single shared-cache writer arrangement.

Acceptance: A malformed published row and a missing static script fail the PR
check; a normal PR passes pytest and build. No Pages permissions or deploy step
are attached to the PR job. Local equivalents pass before publishing; remote
validation remains a later authorized action.

What changes: Data and build regressions are caught before the main push that
triggers production deployment.

### C. Add a short README and reconcile operating documentation

Estimate: 1 agent hour. High onboarding benefit. No open duplicate; preserve
completed task descriptions as historical evidence. Task [11] owns runner
migration, and tasks [1], [2], [4], [5] own pending import decisions.

Evidence: There is no tracked README. `AGENTS.md:14-24` recommends unqualified
uv setup and direct rendering. `pyproject.toml:11` permits every Python >=3.11,
but the working build uses 3.11 at `.github/workflows/deploy.yaml:27` and the
recorded Transcrypt 3.14 failure is in
`docs/tasks/12-gather-acceptance-evidence-for-the-4-review-queue-items.md:68-81`.
Direct render succeeded in this review but produced no
`static/__target__/palindrome.js`, which the template imports at
`palindromi_fi_builder/templates/palindrome.html:8`. Only Make compiles it at
`Makefile:11-16`. The exact text hash is truncated to four bytes at
`palindromi_fi_builder/database.py:107-112`.

Work: Add the short README drafted below, update AGENTS.md to point to the build
path, and reconcile the discrepancy inventory in this report. Explain which
commands operate on curated data versus drafts, and document that `load` emits
site data rather than a lossless database backup. Correct the project Home URL
at `pyproject.toml:34-35` to this repository. Keep historical task outcomes and
add dated corrections rather than rewriting their original requirements.

Acceptance: A fresh checkout follows the README on Python 3.11 and produces
HTML, navigation JavaScript and illustrations. All current commands match CLI
help. Deployment instructions identify the main-push trigger and Antti's
ownership. The discrepancy inventory has a documented resolution for each item.

What changes: The first build works and readers can distinguish current
instructions from investigation history.

Proposed README content, to be added only by the future issue:

```markdown
# palindromi.fi

A static Finnish palindrome collection with English translations and illustrations.

Use uv and Python 3.11 for the site build. The current Transcrypt build is known
not to work on Python 3.14.

    uv sync --frozen --python 3.11
    uv run --no-sync make build
    uv run --no-sync python -m http.server --bind 127.0.0.1 --directory html 8000

Open http://127.0.0.1:8000/. Re-run make build after editing content.

    uv run --no-sync pytest

Published entries live in database/palindromes/*.yaml. Filename and row order
set navigation; the last entry is the homepage. database/INBOX.yaml is unpublished.
Exact text, including newlines, determines existing page identifiers. Do not
normalize published text casually.

The builder loads YAML in database.py, renders Jinja templates in render.py,
and updates output through syncer.py. Make compiles keyboard navigation from
static/palindrome.py. The load subcommand dumps derived site data, not a backup.

See docs/zoho-import.md for the unfinished import and TASKS.md for work status.
The current Zoho converter output is unsafe to import.

Pushing main triggers GitHub Pages deployment. Publishing and deployment belong
to Antti; a local build does not require either.
```

The sentence about rerunning Make assumes draft A has landed. If C lands first,
use `uv run --no-sync make -B build` until A is complete.

### D. Validate published rows before constructing the site

Estimate: 1 agent hour. High diagnostic benefit; keep the first patch narrow.
Partial overlap with [4] and [5] on data rules, so do not decide import policy here.

Evidence: `palindromi_fi_builder/database.py:82-96` casts unchecked YAML and
indexes row zero even for an empty database. Missing required keys fail inside
conversion at `database.py:61-71`; empty translations fail in the template at
`templates/palindrome.html:23`. Identifiers contain only 32 hash bits at
`database.py:107-112`, but uniqueness is not checked before pages are overwritten
at `render.py:98-110`. Current data has 47 distinct identifiers, so no existing
collision was found. The illustration in
`database/palindromes/99-illustrated.yaml:45-46` lacks keys declared required at
`database.py:14-19`; its unquoted date at line 47 loads as `datetime.date`, although
`created` is typed as str at `database.py:37`.

Work: Validate the published subset at the loader boundary, reporting source
file and row for missing text, author, translation and illustration files.
Reject an empty collection and duplicate output identifiers explicitly. Model
optional illustration fields and accepted date values honestly. Keep identifiers
and text byte-for-byte compatible. Do not introduce Pydantic or a generic schema
framework. Broader INBOX validation belongs with [4]/[5].

Acceptance: Small fixtures cover empty input, malformed rows, missing images,
empty translations, duplicate identifiers and the existing optional illustration
metadata. Errors name the source row and occur before output writes. The real
47-entry database keeps its identifiers and navigation.

What changes: Invalid curated content produces actionable errors instead of late
tracebacks or silent page replacement.

### E. Escape rendered content while preserving typographic quotes

Estimate: 1 agent hour. Medium benefit now, higher once imported text is published.
No open duplicate; curation after [5] should use this boundary.

Evidence: `palindromi_fi_builder/render.py:31-38` constructs Jinja without
autoescaping. `templates/palindrome.html:16-23` places text in an attribute and
in blockquotes. A temporary row containing `<b>HTML</b>` renders an actual HTML
tag. `typography.py:24-26,36` returns entity strings, so merely switching on
autoescape would double-escape its output.

Work: Enable HTML autoescaping and make typography transform escaped text safely,
or return Unicode punctuation instead of HTML entities. Handle text attributes
without marking raw source content safe. Reuse one configured environment and
template for a render run, behind a small rendering interface; currently both
are recreated for each of 47 pages at `render.py:31-33`.

Acceptance: Text containing `<script>`, ampersands and attribute quotes stays
literal, while existing typographic quotes and apostrophes display correctly.
Repeated rendering uses the same configuration and yields stable bytes. Keep
page rendering independently testable without Click or filesystem fixtures.

What changes: Content cannot become unintended HTML, and template policy has
one owner. This is a reproduced content boundary defect, not evidence that
current curated rows contain an attack.

### F. Give navigation and illustrated pages accessible text

Estimate: 1 agent hour. Medium benefit to keyboard and screen-reader users.
No open overlap.

Evidence: `templates/palindrome.html:2,16-23,28-31` omits page language, image alt
text and meaningful navigation labels. `static/main.css:52-55` removes the text
from display when it is drawn in an image; `main.css:76-79` removes focus outlines.
The script focuses the next link but attaches its handler only to that link at
`static/palindrome.py:1-13`, so keyboard behavior changes when focus moves.

Work: Label both navigation links, retain visible keyboard focus, supply useful
image alternatives and document language choices. Keep illustrated palindrome
text available to assistive technology when visually hidden. Bind keyboard
navigation consistently and prevent default space scrolling where appropriate.
Do not redesign the page or remove its large tap targets.

Acceptance: Both links have accessible names and visible focus, text-in-image
pages expose the palindrome, and arrow/space navigation works after tabbing to
either link. Check generated HTML and perform a local keyboard walkthrough.

What changes: The existing visual design remains usable without relying on the
image or the initially focused link.

### G. Separate raw database records from derived site navigation

Estimate: 1 agent hour. Medium benefit before the import work; partial overlap
with [5], which explicitly proposes reusing YAML tools for importing.

Evidence: `load.py:21-23` calls `read_database`, which returns SitePalindrome
rather than raw rows. `database.py:61-71` copies a whitelist and drops fields
such as grading and series present at
`database/palindromes/02-additional.yaml:142-148`. `read_database` also calculates
navigation at `database.py:88-96`. Thus `load` is not a lossless export, and this
loader cannot directly serve an INBOX importer with incomplete translations.

Work: Keep raw row reading and published-site preparation as two explicit
functions in database.py. Preserve editorial fields in the raw path. Keep the
existing `load` output compatible or add an explicit raw option with documented
semantics; do not silently replace its output format. Let [5] reuse the raw
boundary when it is implemented.

Acceptance: A raw round-trip retains grading, series, language, unknown import
metadata and exact text. Site preparation still returns the same 47 identifiers,
circular links and homepage order. INBOX rows are not forced through published
translation requirements. CLI help states which representation it emits.

What changes: Import and formatting code can reuse YAML reading without depending
on website navigation or losing editorial fields.

### H. Make the YAML formatter's literal policy real and testable

Estimate: 0.75 agent hour. Modest benefit; coordinate with [5]'s round-trip criterion.

Evidence: `yaml_utils.py:13-21` and `format.py:55-58` promise long strings use
literal blocks. In the pinned ruamel version, a 51-character one-line string
already does produce `|-`, so this review found no long-string bug.
However, `create_yaml_dumper` claims to preserve long/multiline scalars at
`yaml_utils.py:28-30` but only sets width at lines 35-37. Callers must explicitly
apply `maybe_preserve_literal`, as format does at `format.py:28-38`. A trailing
newline correctly gives `|`, not the universally promised `|-`. There are no
formatter or yaml_utils tests in the current three test modules.

Work: State the distinction between dumper configuration and text-field
conversion; test the actual formatter's round-trip behavior and scalar policy.
Preserve trailing newlines because they determine identifiers. Consolidate
serialization through existing `yaml_dump` only if that removes duplication;
otherwise remove the unused helper as in the Honey list below.

Acceptance: Short, long, multiline, trailing-newline, empty and quoted text
round-trips without changing Python strings or dropping extra fields. A second
format pass writes nothing. Documentation describes YAML chomping accurately.

What changes: Future importers have a tested serialization contract rather than
inferring it from misleading factory documentation.

### I. Align local lint entry points and trim proven leftovers

Estimate: 1 agent hour. Modest benefit; no new issue for the entire lint backlog.
Converter typing work overlaps [2] and stays there.

Evidence: `Makefile:23-24` invokes `darglint2`, absent from
`pyproject.toml:23-32` and the installed frozen environment, while CI uses
Graylint at `.github/workflows/linting.yaml:28-31`. The full documented checks
currently report seven flake8 findings and 177 mypy errors. `mypy.ini:48-49`
retains a pkg_resources override although render now imports importlib.resources
at `render.py:3`. `pyproject.toml:14,30` installs BeautifulSoup and its stubs,
but no package Python module imports either bs4 or BeautifulSoup.

Work: Make local lint invoke the locked CI command and remove the stale darglint2
invocation. Trim the specific leftovers below, correcting stale examples and
comments in the same patch. Remove unused BeautifulSoup dependencies only after
checking the tracked root investigation scripts too. Do not claim a fully clean
mypy baseline or suppress its errors globally. Leave converter repair to [2].

Acceptance: The frozen environment runs the local lint command without missing
executables. Its scope and revision match the documented CI policy. Remaining
full-check failures are recorded accurately, and pytest still passes. Dependency
removal, if justified, updates the lock without unrelated upgrades.

What changes: Local checks stop depending on an undeclared executable and the
repository contains fewer obsolete helpers and comments.

### J. Make Syncer writes idempotent within one run

Estimate: 0.75 agent hour. Low current benefit, useful only if rendering starts
reusing destinations. No current production caller was found to copy one static
tree twice, so this is last, not a prerequisite for the earlier fixes.

Evidence: `syncer.py:66-72` compares bytes only while the destination is in
old_files, then removes it. Two writes of identical new bytes through one
Syncer both return True in a temporary fixture. `syncer.py:109-112` also calls
`old_files.remove` for an existing directory on every copytree traversal,
which can raise KeyError on a repeated traversal.

Work: Compare existing destination bytes consistently and use set operations
that tolerate repeated registration. Retain deletion tracking and directory
handling. Do not replace the class with shutil.copytree, which does not provide
its timestamp-preserving contract.

Acceptance: Writing the same destination twice leaves its second-write mtime
unchanged and returns False. Copying a nested tree twice succeeds. Existing
update, removal and unchanged-file tests still pass.

What changes: The synchronization interface becomes safe to reuse during a
single build without hidden call-order requirements.

## Documentation and workflow discrepancy inventory

This is the full set found by reading all tracked docs, AGENTS.md, Makefile,
project metadata and the three workflows against the reviewed code. Historical
requirements and dated observations are distinguished from current instructions;
they must not be silently rewritten as though the earlier work never happened.
Private Zoho snapshots and external service claims were not independently checked.

1. **Setup permits an unsupported build interpreter.** `AGENTS.md:14-15` and
   `pyproject.toml:11` leave Python unconstrained above 3.11. CI explicitly uses
   3.11, and the existing 3.14 build failure is recorded in task 12 at lines 68-81.
   This review reproduced the successful 3.11 build, not the historical 3.14
   failure. Document the narrower build support in C; dependency metadata need
   not imply the pure Python helpers all fail on newer interpreters.
2. **The documented render command omits JavaScript compilation.**
   `AGENTS.md:20` renders pages that import a nonexistent script on a clean
   checkout, because `render.py:64-67` only copies existing static assets.
   `Makefile:11-16` is the compiler step. Confirmed with direct render into a
   temporary directory. Resolve in C and guard it in B.
3. **The incremental build target does not track the actual inputs.**
   `Makefile:18-21` ignores content inputs while the renderer's own docstring at
   `render.py:51` promises rendering all palindromes without touching unchanged
   files. The promise holds when render runs; Make can skip it. Resolve in A.
4. **The load command's description is incomplete.** `AGENTS.md:21` and
   `load.py:15` describe a database dump. The actual output contains identifiers
   and navigation and drops grading/series through `database.py:61-71`.
   Explain the derived representation in C; draft G offers a raw boundary.
5. **gsutil is historical, not the current deploy mechanism.** `AGENTS.md:41`
   and `syncer.py:3-5` describe gsutil as the motivation. Current deploy uploads
   an artifact and uses deploy-pages at `.github/workflows/deploy.yaml:34-50`.
   Keep the timestamp guarantee, describe its historical motivation accurately.
   The Syncer example also uses `syncr` then `sync` at `syncer.py:22-26`, and
   imports a top-level module instead of the package at line 20. Resolve in I.
6. **Current full checks do not pass.** `AGENTS.md:29-32` gives valid full-check
   commands, but seven flake8 findings and 177 mypy errors remain. This is a
   scope difference from incremental CI, not proof that the accepted linting
   fix failed. Record that distinction in C/I. `Makefile:24` additionally asks
   for undeclared darglint2. The frozen CI command does not use it.
7. **Dumper and chomping claims are too broad.** `yaml_utils.py:28-30` promises
   conversion the factory does not configure, and `yaml_utils.py:13-14` plus
   `format.py:55-58` universally say `|-` even though a trailing newline produces
   `|`. Scalar values are preserved correctly in the probes. Resolve in H.
8. **Import counts and duplicate claims are stale outside their dated context.**
   `docs/zoho-import.md:117-119` says INBOX has 37 duplicate groups introduced by
   3daa724. Task 3's outcome at `docs/tasks/3-remove-inbox-duplicates.md:25-41`
   records their removal in bcc051c, which is on main. INBOX now has 109 rows,
   all graded. `docs/tasks/4-zoho-import-rules.md:6-7` still says 151 curated
   INBOX entries. Correct the current counts or date them in C; do not reopen [3].
9. **The unpushed-commit warning describes an old snapshot.**
   `docs/zoho-import.md:22-23,117-119` says the last seven commits, including
   3daa724, are unpushed. Locally cached origin/main already contains 3daa724.
   This dated October 5 observation cannot describe today's branch. Preserve it
   as history or add a dated correction; main is still intentionally ahead, so
   do not infer permission to push. C owns the clarification.
10. **New export naming and the old converter disagree.**
    `docs/tasks/1-refresh-zoho-exports.md:16-17` instructs saving
    YYYY-MM-DD-vNNNN.html. `adhoc/convert_zoho_html.py:115` accepts only the old
    date-only names. Task 1 explicitly relies on task 2's future converter, so
    retain that dependency rather than claiming the current converter supports
    new names. This belongs to existing [2], not a new issue.
11. **Converter behavior contradicts its broad markup description.**
    `adhoc/convert_zoho_html.py:28-33` says it handles both variants, but its
    start-tag handler at lines 41-50 does not preserve an empty div as a blank
    separator. The synthetic phone markup yielded `aba\ncdc`, one block.
    `docs/zoho-import.md:18-21,38-45` and AGENTS.md's known-broken warning are
    accurate. Existing [2] owns the fix, including filename ordering and metadata
    extraction. Do not file a parallel converter rewrite.
12. **The root-script cleanup describes tracked files as untracked.**
    TASKS.md's active simple issue names analyze_zoho_html.py and
    extract_zoho_revisions.py as untracked, but both are tracked in this main
    snapshot. Their advice also predates the converter warning, for example
    `analyze_zoho_html.py:14-17` recommends the converter for actual extraction.
    Amend the existing cleanup issue's premise when its owner resumes it; do not
    file another deletion draft. The scripts import BeautifulSoup at lines 24
    and 25 respectively, so its dependency is not globally dead yet.
13. **Old CI task premises are superseded, not new defects.** Task 6 lines 3-11
    describe pip installs, missing test extras and old Darker; task 7 lines 12-21
    describes the branch Graylint action and setup-python; task 8 lines 15-26
    describes the old Darker action and absent dev dependency; task 9 lines 12-14
    lists older actions. The current workflows use frozen uv installs, explicit
    3.11, checkout v7, and CLI Graylint/Darker. Their later implementation sections
    mostly explain this. Add historical labels only where needed under C.
14. **Some completed task descriptions still contain old stop instructions.**
    `docs/tasks/7-fix-linting-workflow.md:69-74` and
    `docs/tasks/8-fix-formatting-workflow.md:70-73` still say keep them In Progress
    until remote success. TASKS.md has accepted both, and task 9 lines 64-82
    records later successful remote runs. Task 9's own lines 60-62 are explicitly
    superseded by that completion section. Preserve the history and cross-link
    the later evidence in C; do not change accepted tracker states.
15. **Ubuntu migration is still intentionally unfinished.** Task 10 lines 7-15
    describe ubuntu-latest and setup-python, but its dated fallback section at
    lines 25-61 explains why all four current jobs use Ubuntu 24.04 and Python
    3.11. Task [11] explicitly tracks remote validation. This is an already-owned
    gap, not evidence to remove pins now. No migration draft is proposed.
16. **Repository metadata points elsewhere.** `pyproject.toml:35` points to
    akaihola/palindromi_fi_builder, while the tracked workflow evidence and issue
    identify akaihola/palindromi.fi. Resolve the project Home URL in C.
17. **The tracker names a nonexistent deployment guide.** TASKS.md's completion
    rules say follow docs/deployment.md; no such tracked file exists. Multiple
    completed tasks correctly say no guide exists. C should point the rule to
    the README's deploy section or add a short guide. Neither should authorize
    this review to push or deploy.

No other contradiction was found in the current workflow commands themselves:
frozen installs, explicit Python, cache writer comments and artifact directory
match the code. Their coverage gaps are B. The empty main-push incremental diff
is intentional in accepted tasks 6-8, not an accidental regression to "fix".
The lack of a PR build and tests remains significant despite that policy.

## Honey delete-list

These are candidate cuts, not changes made during this review. Counts exclude
surrounding blank lines and include replacement lines where relevant.

1. `palindromi_fi_builder/yaml_utils.py:40-50`: cut unused yaml_dump if H does not
   adopt it; no tracked caller exists. Saves 11 lines.
2. `palindromi_fi_builder/format.py:28,30,34,40,45,72,84`: cut seven comments that
   narrate the following operation; they add no policy. Saves 7 lines.
3. `palindromi_fi_builder/syncer.py:34-40`: cut mkdirp and use
   Path.mkdir(parents=True, exist_ok=True) at its two callers, lines 71 and 114.
   Saves 7 lines. This is a thin stdlib wrapper, not a useful deep module.
4. `palindromi_fi_builder/static/main.css:33-35,45-46`: cut two empty selectors.
   Saves 5 lines without removing visual behavior.
5. `mypy.ini:48-49`: cut the pkg_resources exception left after the accepted
   importlib.resources migration. Saves 2 lines.

Total: 32 lines across five findings. Imports made unused by these cuts can be
removed too. Do not count speculative removal of tests, input checks, requests,
or BeautifulSoup as savings. The generic Syncer test helpers support meaningful
shared assertions and are not a priority just because they use classes.

## Already-owned work and deferred observations

- [1], [2], [4], [5] own refreshing private exports, converter fidelity, import
  policy and import execution. The converter's first-match regex, permissive
  unknown-tag handling, repeated block parsing, per-file broad exception catch
  and date sorting all belong in [2]'s existing rewrite. Avoid cosmetic cleanup
  there before its semantics change.
- [11] owns Ubuntu 26 validation and pin removal. This review neither tests
  hosted runners nor proposes another migration ticket.
- The active simple cleanup issue owns the two root scripts. Once they are
  deleted, I can remove BeautifulSoup and its stubs if no remaining consumer
  needs them. Requests remains used by the public-note downloader at
  `adhoc/zoho_notebook.py:44`.
- `server.py:9-11` overrides extensionless MIME types and mutates the base
  handler's map. Generated pages now have .html via `render.py:17,108`, so the
  stdlib server is sufficient for new pages. The README uses it; removing the
  old command is low benefit without deciding legacy URL compatibility.
- `palindrome.py:13` ignores å while tasks 2-5 describe comparison keys including
  å. These are currently separate operations. Decide and test a shared policy
  under [4]/[5] before reusing is_palindrome as a normalization contract. No
  published text should be normalized to implement this.
- `static/CNAME:1` is copied under html/static by `render.py:64-67`, not to the
  output root. The temporary build confirms that placement. Repository Pages
  settings may already own the custom domain; no live failure is established.
  Clarify ownership with the deployment documentation before moving it.
- The public-note downloader does not call raise_for_status before XML parsing
  at `adhoc/zoho_notebook.py:44-49`. Add a focused diagnostic if [1] needs this
  optional fetch path. The default refresh path is saving exports manually.

## Validation and limits

Read all tracked docs and workflow files, the Makefile and pyproject.toml before
reviewing every package Python file, template, static source and test. Parsed all
published YAML and INBOX rows, inspected their key distributions and the five
illustration references. No image-content or visual-layout audit was performed.
No private Zoho exports were available; their counts and provenance remain dated
investigation claims rather than independently reproduced evidence.

Used an external temporary virtual environment with frozen dependencies and
managed CPython 3.11.16. Temporary fixtures and build output stayed outside the
repository; bytecode and mypy caches were redirected there too.

- `uv sync --frozen --python 3.11` passed with managed Python downloads enabled.
- `python -m pytest -q -p no:cacheprovider`: 39 passed, zero failed.
- `flake8 -j 1 palindromi_fi_builder`: seven findings, six E501 and one W391.
- `mypy --cache-dir <temporary-directory> .`: 177 errors in seven files, checking
  19 source files; it also warns that strict-concatenate is deprecated.
- A clean temporary copy ran `make build` successfully, producing 48 HTML files
  and the navigation JavaScript. The three Make invalidation probes failed to
  schedule rebuilding, as described in A.
- Direct render succeeded without generating JavaScript. Empty-database,
  empty-translation, raw-HTML, repeated-Syncer-write, phone-markup and scalar
  round-trip probes reproduced the outcomes cited above.
- `git diff --check` passed for the report. No application, data or workflow
  changes were made, and no drafts were filed. No push, deploy or remote workflow
  was attempted. Existing lint/type failures do not block this report-only issue.
