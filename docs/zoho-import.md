# Importing palindromes from Zoho Notebook

Current status checked against source on 2026-10-22. The export investigation
below is an October 5 snapshot, not a fresh check of Zoho or its free-plan limits.
It replaces the local-only, partly wrong [original analysis].

Antti keeps his working list of palindromes in one Zoho Notebook note. On
2025-12-06/07 he saved 52 versions of it from Zoho's version-history view with
the browser's "Save page as" into the [local export directory]. That directory is
git-ignored: 870 MB, and the pages contain an email address and a Zoho user id.
Investigation scripts and full result tables from 2026-10-05 are in
the [local investigation directory]. Its [digest] summarises them.

## Current status, 2026-10-22

The [duplicate-removal task] removed the reflowed duplicates in `bcc051c`;
[INBOX] contains 109 rows, all graded. The old duplicate and unpushed-commit
statements below are historical. The local `origin/main` reference includes
`3daa724`; no remote freshness check was made for this review.

See the [data contract] for curated versus unpublished input, exact-text
identifiers, translation requirements and the fields omitted by `load`.

The [export refresh], [converter rewrite], [import rules] and [database import]
still own the remaining work. The [current converter] accepts only date-only
export names, so the rewrite must support version-suffixed names from the
export-refresh plan. Its output remains unsafe to import.

## Current scripts

The [current converter] reads local exports from the repository's
[local export directory], sorts date-only filenames, and extracts the first
`parsed-html` attribute. It writes a same-date text file containing blocks absent
from earlier files, or deletes that text file if none remain. Repetitions within
one export are retained; it does not validate palindromes. Empty `<div>` separators
are lost. The converter can be invoked for diagnosis after the [project setup]:

```bash
uv run --no-sync python -m palindromi_fi_builder.adhoc.convert_zoho_html
```

The 2023 [public-note downloader] reads a notecard through the public API and
prints Python dictionaries. Its `parse_block()` takes the first palindrome
prefix and treats the rest as an English translation, which can split real
multi-line palindromes. It is not the planned historical-export importer.

The root [HTML analysis script] and [revision analysis script] are exploratory
diagnostics. They decode as UTF-8 with replacement despite the investigated
exports' Windows-1252 encoding, and use BeautifulSoup's `lxml` parser. Their
inline uv script metadata declares `lxml`; the project dependency set does not.
They are not validated import steps.

## Where things stood on 2026-10-05

- Almost nothing from the note is in the database yet. The newest export has
  1,809 distinct entries. Only two of them are already in the database:
  "Aimo, saispa lapsia somia!" and "Ojenna Niilo lavitsalle…".
- The [current converter] extracted text correctly from most exports. Its
  text output in the [local export directory] was wrong, though. It ordered
  exports by filename, several filenames are wrong, and it misreads the markup
  of four exports.
- The last 7 commits, including the INBOX reformat in `3daa724`, are not pushed
  yet.

## What the exports contain

**Each page knows its own version.** The version-history pane shows a header
`<span>Versiot</span> <span>1121.0</span>`, and the selected item in the
100-item version list has the class `selected-version-indicator`, plus a
timestamp like `10:27 AM - Nov 23, 2024`. The 2025 timestamps carry no year.
Date and order snapshots by this, not by filename.

**Content attributes.** The first three `parsed-html="…"` attributes hold the
selected version. `current-version-parsed-content` and `initial-content` hold
the live note at export time, which is v1142, in every file. The asset-directory index pages in the
[local export directory] also show v1142 and carry no history.

**Encoding and markup.** Every file is windows-1252. The content uses only
`<div>`, `<br>` and `&nbsp;`, in two variants:

- `<div>text<br></div><div><br></div>`: most exports.
- `<div>text</div><div></div>` with no `<br>` at all: v1074, v1076, v1077 and
  v1080, all saved from the phone app. Here an empty leaf `<div>` is the blank
  line. The current converter only treats `<br>` as a blank line, so it reads
  these whole notes as one entry.

A few lines contain non-breaking spaces. Convert them to spaces before
comparing texts.

**Version window at capture time.** The free Zoho plan showed the newest 100 versions,
v1043 (2024-02-19) to v1142 (2025-11-30). Every new edit to the note pushes the
oldest one out of reach under that limit. The earliest captured version, v1049, held
1,602 entries.

### Misnamed exports

| File                          | Actually holds          | Note                                         |
| ----------------------------- | ----------------------- | -------------------------------------------- |
| [November 23 export]         | v1121, 2024-11-23 10:27 | Year typo (2023 filename). Used as baseline |
| [April 17 export]            | v1092, 2024-04-18 22:45 | v1091 (2024-04-17 06:43) was never saved     |
| [October 11 export]          | v1142, 2025-11-30 21:31 | Copy of [November 30 export]. v1132 not saved |
| [October 29 export]          | v1142, 2025-11-30 21:31 | Copy of [November 30 export]. v1133 not saved |
| September 6, 15, 22, 25 exports | 2024, names are right | Their asset directory names mistakenly use 2025 |

All other files hold the last version of the day in their name. The full table
is in the [local dating table].

## What the newest version (v1142) contains

| Kind                                                   | Distinct texts |
| ------------------------------------------------------ | -------------: |
| Already in the database                                |              2 |
| New, passes `is_palindrome()`                          |          1,673 |
| Fragment drafts such as `..apinan ipana..`             |             81 |
| Near-palindromes that fail `is_palindrome()`           |             53 |
| Total                                                  |          1,809 |

The 1,673 include 172 multi-line entries.

Things the import has to handle:

- **Duplicates inside the note.** 36 texts appear twice, and 17 groups differ
  only in punctuation. Most come from a section first added on 2024-04-17/18
  and pasted again with edits on 2025-05-03. Those edits went both ways. For
  example, the newer "Tää poni… sanat" no longer reads as a palindrome, while
  the older "saivat" form does. Within a group, prefer the form that passes
  `is_palindrome()` over the newest copy.
- **Variant families.** 145 clusters of near-identical palindromes, such as
  "Noutajia, Aija/Kaija/Maija/… tuon." The database already has a `series:`
  key for these.
- **Multi-line blocks.** 202 in total. 171 read as one palindrome across all
  lines, though at least one of those is two variants stacked. 24 are a
  palindrome followed by its translation, and 7 are drafts. "Rotative lei, bra,
  Barbie. Levitator!" is an English palindrome with a Finnish translation. The
  old `parse_block()` in the [public-note downloader] splits 4 real palindromes in
  half, so review these blocks by hand.
- **Fragments.** Drafts are marked with `..` at the start or end, a `X.. ..Y`
  gap, or `---`. Six have no marker. All of them pass `is_palindrome()`, so
  that check can't filter them out.
- **History.** Older versions add almost nothing. 15 texts exist only in older
  versions, and all of them were later edited, completed, split or re-marked.
  Nothing was deleted outright.
- **Dates.** 1,556 entries were already in v1049, so for them we only know
  "on or before 2024-02-19". Some go back to 2018. For the roughly 200 entries
  added later, the last captured version without the entry and the first one
  with it bracket the date.

## Historical database finding

On October 5, [INBOX] had 37 duplicate groups added by `3daa724`: multi-line
entries reflowed onto one line without grading. They have since been removed;
see the current status above. Current database requirements live in the
[data contract].

## Plan

The [tracker][tasks] owns work status and dependencies. Finish the
[export refresh], [converter rewrite] and [import rules], then the
[database import]. The [duplicate removal][duplicate-removal task] and
[CI dependency fixes] are complete.
Publishing the imported palindromes, with translations and grading, is a separate
curation job after that.

[tasks]: ../TASKS.md
[original analysis]: ../zoho-history/ANALYSIS.md
[local export directory]: ../zoho-history/
[local investigation directory]: ../zoho-history/investigation-2026-10-05/
[digest]: ../zoho-history/investigation-2026-10-05/DIGEST.txt
[local dating table]: ../zoho-history/investigation-2026-10-05/dating/per_file.tsv
[INBOX]: ../database/INBOX.yaml
[data contract]: development.md#data-and-rendering
[project setup]: ../README.md
[current converter]: ../palindromi_fi_builder/adhoc/convert_zoho_html.py
[public-note downloader]: ../palindromi_fi_builder/adhoc/zoho_notebook.py
[HTML analysis script]: ../analyze_zoho_html.py
[revision analysis script]: ../extract_zoho_revisions.py
[export refresh]: tasks/1-refresh-zoho-exports.md
[converter rewrite]: tasks/2-fix-zoho-converter.md
[duplicate-removal task]: tasks/3-remove-inbox-duplicates.md
[import rules]: tasks/4-zoho-import-rules.md
[database import]: tasks/5-import-zoho-palindromes.md
[CI dependency fixes]: tasks/6-ci-dependency-installs.md
[November 23 export]: ../zoho-history/2023-11-23.html
[April 17 export]: ../zoho-history/2024-04-17.html
[October 11 export]: ../zoho-history/2025-10-11.html
[October 29 export]: ../zoho-history/2025-10-29.html
[November 30 export]: ../zoho-history/2025-11-30.html
