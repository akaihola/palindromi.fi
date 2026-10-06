# Decide the rules for importing Zoho palindromes

Decisions for Antti before task 5. Each item has a recommendation. Record the
decisions in this file.

- **Target file.** Recommended: a new `database/zoho-inbox.yaml`, so ~1,700 new
  entries don't bury the 151 curated ones in `INBOX.yaml`. The site renders neither.
- **`created`.** 1,556 entries were already in the earliest captured version (v1049,
  2024-02-19), and some of them go back to 2018. Recommended: leave `created` out
  for those. For later entries, store the first version containing them in a
  separate key such as `zoho_first_seen`, because that date is only an upper bound.
- **Variant families.** There are 145 clusters of near-identical palindromes, such as
  "Noutajia, Aija/Kaija/Maija/… tuon." Recommended: import every member and group
  them with `series:`. Never drop one automatically.
- **Fragments and near-palindromes.** 81 drafts like `..apinan ipana..` and 53
  entries that fail `is_palindrome()`. Recommended: leave them in Zoho and import
  only finished palindromes.
- **Multi-line blocks.** 202 blocks: 171 read as one palindrome across all lines, 24
  are a palindrome plus its translation, and 7 are drafts. Recommended: generate a
  review sheet that proposes a split into palindrome lines, translation lines and
  language, then confirm every block by hand. `parse_block()` in
  `adhoc/zoho_notebook.py` splits 4 real palindromes in half, so don't reuse it as is.
- **Duplicates inside the note.** 36 texts appear twice and 17 groups differ only in
  punctuation. Recommended: dedupe by letter-only key and prefer the form that passes
  `is_palindrome()`, then the topmost one. "Newest copy wins" would keep regressions
  such as "Tää poni… sanat".
- **Cleanup in Zoho.** Optionally remove the duplicated section in the note first.
  It was added on 2024-04-17/18 and pasted again with edits on 2025-05-03.
