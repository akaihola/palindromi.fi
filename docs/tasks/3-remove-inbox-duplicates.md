# Remove the reflowed duplicates that 3daa724 added to INBOX.yaml

Commit `3daa724` (2025-12-06) added 42 entries to `database/INBOX.yaml`. 37 of them
repeat entries already in the file. Each is the same palindrome reflowed from
several lines onto one, with the same `created` date and no `grading`. For example,
the graded "Ne napakisat...\nTurtana hanat ruttasi Kapanen." now has an ungraded
twin "Ne napakisat... Turtana hanat ruttasi Kapanen.".

Group INBOX entries by letter-only key (lowercase, keep only a-zåäö and digits) to
find them. Expect 37 groups with 38 surplus entries, one group having three
members. Keep the original graded entry of each group unless the reflowed text is
better, and review the 5 other entries that `3daa724` added.

`3daa724` is not pushed yet. Fix it with a new commit before pushing `main`. Don't
rewrite history: `main` also lives in `agent@gogo:~/prg/palindromi.fi`.

While at it, check the 5 INBOX entries whose letters match published palindromes:
"Aimo, saispa lapsia somia!", "Ei vessoja, aha. …", "Nousi savu tuo hutera
tuotannosta. …", "Sotii, kas sisko, Putin nuhaa. …" and "Iski ruumis. …".

`format` round-trips `INBOX.yaml` unchanged, so it is safe to run on that file.
Don't run it on `database/palindromes/` in the same commit: it would reformat 5
unrelated strings there.
