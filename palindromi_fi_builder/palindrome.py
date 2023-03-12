"""Helpers for inspecting palindromes."""

import re


def is_palindrome(text: str) -> bool:
    """Check if a text is a palindrome

    :param text: The text to check
    :return: `True` if the text is a palindrome, `False` otherwise

    """
    letters = re.sub(r"[^a-z0-9äö]", "", text.lower())
    if len(letters) < 3:
        return False
    return letters == letters[::-1]
