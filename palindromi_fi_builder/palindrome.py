"""Helpers for inspecting palindromes."""

import re


def is_palindrome(text: str) -> bool:
    """Check symmetry after lowercasing and retaining only a-z, 0-9, ä and ö

    At least three retained characters are required. Punctuation and other
    characters are ignored; this does not distinguish complete entries from drafts.

    :param text: The text to check
    :return: `True` if the text is a palindrome, `False` otherwise

    """
    letters = re.sub(r"[^a-z0-9äö]", "", text.lower())
    if len(letters) < 3:
        return False
    return letters == letters[::-1]
