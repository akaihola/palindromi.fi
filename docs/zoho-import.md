# Importing palindromes from Zoho Notebook

Status on 2026-10-05. This replaces `zoho-history/ANALYSIS.md`, which is
local-only and partly wrong.

Antti keeps his working list of palindromes in one Zoho Notebook note. On
2025-12-06/07 he saved 52 versions of it from Zoho's version-history view with
the browser's "Save page as" into `zoho-history/`. That directory is
git-ignored: 870 MB, and the pages contain an email address and a Zoho user id.
Investigation scripts and full result tables from 2026-10-05 are in
`zoho-history/investigation-2026-10-05/`. `DIGEST.txt` there summarises them.

## Where things stand

- Almost nothing from the note is in the database yet. The newest export has
  1,809 distinct entries. Only two of them are already in the database:
  "Aimo, saispa lapsia somia!" and "Ojenna Niilo lavitsalle…".
- `adhoc/convert_zoho_html.py` extracts text correctly from most exports. Its
  `zoho-history/*.txt` output is wrong, though, so don't use it. It orders
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
the live note at export time, which is v1142, in every file. The
`*_tiedostot/index.html` files also show v1142 and carry no history.

**Encoding and markup.** Every file is windows-1252. The content uses only
`<div>`, `<br>` and `&nbsp;`, in two variants:

- `<div>text<br></div><div><br></div>`: most exports.
- `<div>text</div><div></div>` with no `<br>` at all: v1074, v1076, v1077 and
  v1080, all saved from the phone app. Here an empty leaf `<div>` is the blank
  line. The current converter only treats `<br>` as a blank line, so it reads
  these whole notes as one entry.

A few lines contain non-breaking spaces. Convert them to spaces before
comparing texts.

**Version window.** The free Zoho plan shows only the newest 100 versions,
v1043 (2024-02-19) to v1142 (2025-11-30). Every new edit to the note pushes the
oldest one out of reach. The earliest captured version, v1049, already holds
1,602 entries.

### Misnamed exports

| File                          | Actually holds          | Note                                         |
| ----------------------------- | ----------------------- | -------------------------------------------- |
| `2023-11-23.html`             | v1121, 2024-11-23 10:27 | Year typo. The converter used it as baseline |
| `2024-04-17.html`             | v1092, 2024-04-18 22:45 | v1091 (2024-04-17 06:43) was never saved     |
| `2025-10-11.html`             | v1142, 2025-11-30 21:31 | Copy of `2025-11-30.html`. v1132 not saved   |
| `2025-10-29.html`             | v1142, 2025-11-30 21:31 | Copy of `2025-11-30.html`. v1133 not saved   |
| `2024-09-06/15/22/25.html`    | 2024, names are right   | Their asset dirs say `2025-09-*` by mistake  |

All other files hold the last version of the day in their name. The full table
is `zoho-history/investigation-2026-10-05/dating/per_file.tsv`.

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
  old `parse_block()` in `adhoc/zoho_notebook.py` splits 4 real palindromes in
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

## Database constraints

- Only `database/palindromes/*.yaml` is rendered. `database/INBOX.yaml` is an
  unpublished backlog, so imports there change nothing on the site.
- A published palindrome needs a translation. The template indexes
  `translations[0]`, so an empty list fails the build, and a missing key raises
  `KeyError` in `database.py`.
- URL identifiers are a SHA-256 of the exact text. Line breaks and trailing
  newlines chosen at import time fix the future URLs.
- `INBOX.yaml` has 37 duplicate groups, added by `3daa724`. They are
  multi-line entries reflowed onto one line, without grading. Since `3daa724`
  is unpushed, it can still be fixed cleanly.

## Plan

1. **Refresh the exports.** You do this in Zoho, before editing the note
   again. Check the current version number. If it is past v1142, save the
   current version too. `adhoc/zoho_notebook.py` can fetch it if the note is
   still shared publicly. If they are still listed, re-save v1091 (2024-04-17),
   v1132 (2025-10-11) and v1133 (2025-10-29). Then rename `2023-11-23.html` to
   `2024-11-23.html` and delete the two v1142 copies.
2. **Fix the converter.** Read the version number and timestamp from each
   page, sort by version, and skip duplicate versions. Decode as cp1252,
   handle both markups, turn NBSP into spaces, and stop on unexpected tags.
   Instead of per-date `.txt` files, write one table of distinct entries with
   the version that first and last contains each. Assert known counts: v1142
   gives 1,845 blocks, 1,809 distinct texts and 1,792 letter-only keys, and
   v1074 gives 1,664 blocks. Add tests for both markups. Prototypes are in
   `zoho-history/investigation-2026-10-05/fidelity/proto_extract.py` and
   `dating/leafdiv.py`.
3. **Remove the 37 INBOX duplicates.** Fix up `3daa724` before pushing.
4. **Decide the import rules.** My recommendations:
   - Target file: a new `database/zoho-inbox.yaml`, so that ~1,700 entries
     don't bury the 151 curated INBOX ones. Nothing reads either file yet.
   - `created`: leave it out for entries already in v1049. For later ones,
     store the first version that contains them, in a separate key such as
     `zoho_first_seen`, since that date is only an upper bound.
   - Variants: import every member and group them with `series:`. Never drop
     one automatically.
   - Fragments and near-palindromes: leave them in Zoho. Import only finished
     palindromes.
   - Multi-line blocks: generate a review sheet with a proposed split
     (palindrome lines, translation lines, language), and confirm all 202 by
     hand.
5. **Import.** Use the new converter's table. Deduplicate inside the note by
   letter-only key, preferring the form that passes `is_palindrome()`, then
   the topmost one. Skip entries already in the database. Compare after
   splitting off translation lines, and treat a text contained in another only
   as a flag for review. Use author "Antti Kaihola" and `translations: []`.
   Review the diff, commit, then push.
6. **Tidy up.** These can happen at any time:
   - Delete the untracked `analyze_zoho_html.py` and
     `extract_zoho_revisions.py` from the repo root. They only did exploration
     that this document now covers, they read a hard-coded export, and one of
     them decodes the file wrongly.
   - Delete `lock.json` and `flake.lock`, left over from the Nix setup removed
     in `eaa78ee`.
   - CI: `linting.yaml` installs the `-e .[test]` extra, which no longer
     exists, and deploy installs with unpinned `pip`. Consider
     `uv sync --frozen`. `render.py` imports `pkg_resources`, which
     recent setuptools releases no longer ship.

Publishing imported palindromes, with translations and grading, is a separate
curation job after this.
