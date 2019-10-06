import re
from typing import Match

QUOTED_RE = re.compile(r'(?: ^ | (?<=\W) )'
                       r'( ".*?" | '
                       r"  '.*?' )"
                       r'(?: $ | (?=\W) )', re.X)
INWORD_APOSTROPHE_RE = re.compile(r"(?<=\w)'(?=\w)")


def convert_quoted(match: Match) -> str:
    opening_quote = match[0][0]
    quoted_text = match[0][1:-1]
    if opening_quote == '"':
        return f'&ldquo;{quoted_text}&rdquo;'
    elif opening_quote == "'":
        return f'&lsquo;{quoted_text}&rsquo;'
    else:
        raise ValueError(f'Unrecognized quotes in: {match[0]}')


def typographic_quotes(s: str) -> str:
    return QUOTED_RE.sub(convert_quoted, s)


def inword_apostrophe(s: str) -> str:
    return INWORD_APOSTROPHE_RE.sub('&rsquo;', s)


def add_typography(s: str) -> str:
    return typographic_quotes(inword_apostrophe(s))
