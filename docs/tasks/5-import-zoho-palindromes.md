---
depends-on: [1, 2, 3, 4]
---

# Import the Zoho palindromes into the database

Build the import from task 2's table for the newest version, following the rules
decided in task 4.

- Deduplicate inside the note by letter-only key as decided in task 4.
- Skip entries already in the database. Compare letter-only keys after splitting off
  translation lines. Expect exactly two matches: "Aimo, saispa lapsia somia!" and
  "Ojenna Niilo lavitsalle…". Treat a text contained in another only as a review
  flag, because "Anne, joulu ojenna!" sits inside the different palindrome
  "Naatti-Manne, joulu ojenna, mittaan.".
- Mark English palindromes with `language: en`, as INBOX does. "Rotative lei, bra,
  Barbie. Levitator!" is one. List first lines without ä or ö and without common
  Finnish words, and review them.
- Fill `author: Antti Kaihola`. Use the translation lines found in the note, or
  `translations: []`.
- The exact `text` decides the future URL identifier, a SHA-256 of the text. Keep the
  note's line breaks and strip trailing newlines.
- Write with `yaml_utils` so that `format` round-trips the file. Consider making the
  importer a `palindromi_fi_builder` subcommand next to `format`.

Expected size from the v1142 analysis: 1,673 distinct new texts that pass
`is_palindrome()`, 1,656 distinct letter-only keys among them.

Review the diff, commit, and push `main` once task 3 is done.
