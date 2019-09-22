import re
from typing import Match

QUOTED_RE = re.compile('".*?"|\'.*?\'')


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
