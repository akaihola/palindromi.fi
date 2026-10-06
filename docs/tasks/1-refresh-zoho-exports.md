# Refresh the Zoho exports before editing the note

Do this in Zoho before the next edit to the palindrome note. The free plan shows
only the newest 100 versions, and every edit pushes the oldest one out of reach.

1. Open the note's version history and write down the newest version number. The
   exports in `zoho-history/` end at v1142 (2025-11-30 21:31).
2. If the newest version is past v1142, save it with "Save page as" into
   `zoho-history/`. If the note is still shared publicly, `adhoc/zoho_notebook.py`
   can fetch its current text too.
3. Re-save these versions if they are still listed. The first export run captured
   the wrong version for each of them:
   - v1091, 2024-04-17 06:43. `2024-04-17.html` holds v1092 from Apr 18.
   - v1132, 2025-10-11 13:05. `2025-10-11.html` holds v1142.
   - v1133, 2025-10-29 23:36. `2025-10-29.html` holds v1142.
4. Name new saves `YYYY-MM-DD-vNNNN.html` so they can't clash with existing files.
   Task 2 reads the version from each page, so names only need to be unique.
5. Optionally rename `2023-11-23.html` to `2024-11-23.html` (it is v1121), and
   delete `2025-10-11.html` and `2025-10-29.html` once their real versions are saved.

Record here which versions were no longer listed.

Versions before v1043 (2024-02-19) need a paid plan. The earliest captured version,
v1049, already holds 1,602 entries, so that history mostly matters for dating.

See "Misnamed exports" in `docs/zoho-import.md`.
