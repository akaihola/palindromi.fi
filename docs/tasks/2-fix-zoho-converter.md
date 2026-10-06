---
depends-on: [1]
---

# Rewrite the Zoho converter to order exports by version

`adhoc/convert_zoho_html.py` extracts text correctly from most exports, but its
`zoho-history/*.txt` output is wrong. It orders exports by filename, several
filenames are wrong, and it reads the phone-app markup as one entry. Background is in
`docs/zoho-import.md`.

Requirements:

- Read the version from each page. The header is
  `<span>Versiot</span> <span>N.0</span>`, and the version-list item with class
  `selected-version-indicator` carries a timestamp like `10:27 AM - Nov 23, 2024`.
  Timestamps in 2025 have no year. Fail if header and selected item disagree.
- Sort snapshots by version and skip duplicate versions. Ignore filenames.
- Keep reading the first `parsed-html` attribute, but anchor the match to the editor
  element instead of relying on match order. Decode as cp1252.
- Handle both markups. In `<div>text<br></div><div><br></div>` a div holding only
  `<br>` is a blank line. In the phone-app variant `<div>text</div><div></div>`,
  which has no `<br>` at all, an empty leaf div is a blank line.
- Replace U+00A0 with a space, strip each line, and stop on any tag other than
  `<div>` and `<br>`.
- Replace the per-date `.txt` files with one table of distinct entries. Each
  blank-line-separated block gets the first and last version containing it, their
  timestamps, and the last captured version before it appeared.

Acceptance:

- v1142 gives 1,845 blocks, 1,809 distinct texts and 1,792 distinct letter-only
  keys. A letter-only key is the lowercased text with everything except a-zåäö and
  digits removed.
- v1074 (`2024-03-14.html`) gives 1,664 blocks.
- In version order, no entry disappears and later reappears.
- Unit tests cover both markups, NBSP handling and version parsing with small HTML
  fixtures, not the real exports.
- flake8, mypy and Black pass for the module.

Prototypes from the investigation are in `zoho-history/investigation-2026-10-05/`:
`fidelity/proto_extract.py` and `dating/leafdiv.py`.
