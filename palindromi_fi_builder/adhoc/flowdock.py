"""Script to convert Flowdock HTML export to a YAML palindrome database."""

import argparse
import re
import sys
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Any, Optional, Sequence, Union, cast

from bs4 import BeautifulSoup, ResultSet, Tag
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString, preserve_literal

from palindromi_fi_builder.database import DbPalindrome, Translation
from palindromi_fi_builder.palindrome import is_palindrome


def maybe_preserve_literal(text: str) -> Union[str, LiteralScalarString]:
    """Use a multi-line YAML literal if the text contains a newline or is too long

    :param text: The text to check
    :return: The text, possibly wrapped in a YAML literal

    """
    if "\n" in text or len(text) > 50:
        return preserve_literal(text)
    return text


def yaml_dump(data: Any) -> str:  # type: ignore[misc]
    """Dump data as YAML with a line width of 88 and return the result as a string

    :param data: The data to dump
    :return: The YAML string

    """
    yaml = YAML()
    yaml.width = 88  # type: ignore[assignment]
    buffer = StringIO()
    yaml.dump(data, buffer)  # type: ignore[misc]
    return buffer.getvalue()


def main() -> None:
    """Read a Flowdock HTML export and convert it to a YAML palindrome database

    The HTML export is expected to be in the file ``eniram-flowdock-palindromes.html``
    """
    opts = parse_arguments()
    messages = read_flowdock_messages(opts.path)
    entries: list[DbPalindrome] = []
    for message in messages:
        palindrome: Optional[str] = None
        translations: list[Translation] = []
        date_element = cast(Tag, message.find_previous("date", class_="timestamp"))
        created = datetime.strptime(
            date_element.attrs["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        author = cast(Tag, message.find_previous("span", class_="message-author")).text
        children = cast(Sequence[Tag], message.contents)
        chunks: list[str] = [
            line
            for child in children
            for line in re.sub(r"\n +", "\n", child.text.strip()).split("\n\n")
            if line
        ]
        for text in chunks:
            if is_palindrome(text):
                if palindrome:
                    emit_entry(entries, palindrome, created, translations, author)
                    translations = []
                palindrome = text
                continue
            if not palindrome:
                continue
            if text.startswith("Google Translate:"):
                translations.append(
                    {
                        "language": "en",
                        "text": maybe_preserve_literal(
                            text[len("Google Translate:") :].strip()
                        ),
                        "author": "Google Translate",
                    }
                )
            else:
                translations.append(
                    {
                        "language": "en",
                        "text": maybe_preserve_literal(text),
                        "author": "Antti Kaihola",
                    }
                )
        if not palindrome:
            child_texts = [m.text for m in children]
            stripped_child_texts = [s.strip() for s in child_texts]
            palindrome_as_yaml = yaml_dump(stripped_child_texts)
            print(f"No palindrome in\n{palindrome_as_yaml}", end="")
            continue
        emit_entry(entries, palindrome, created, translations, author)
    print_db_as_yaml(entries)


class Namespace(argparse.Namespace):  # pylint: disable=too-few-public-methods
    """Namespace with a path attribute that is a pathlib.Path"""

    path: Path


def parse_arguments() -> Namespace:
    """Parse command-line arguments

    :return: The parsed arguments

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="Path to the HTML export of the Flowdock conversation",
        # the lambda is needed to make Mypy happy
        type=lambda s: Path(s),  # pylint: disable=unnecessary-lambda
    )
    opts: Namespace = parser.parse_args(namespace=Namespace())
    return opts


def read_flowdock_messages(path: Path) -> ResultSet[Tag]:
    """Read the messages from the Flowdock HTML export

    :param path: The path to the file containing the HTML export
    :return: The DIV elements containing the messages

    """
    with path.open() as flowdock_export_file:
        document = BeautifulSoup(flowdock_export_file, "html.parser")
        messages: ResultSet[Tag] = document.find_all("div", class_="msg-body")
    return messages


AUTHORS = {
    "AnttiK": "Antti Kaihola",
    "Jarno": "Jarno Saarimäki",
    "Google Translate": "Google Translate",
}


def emit_entry(
    entries: list[DbPalindrome],
    palindrome: str,
    created: datetime,
    translations: list[Translation],
    author: str,
) -> None:
    """Emit a palindrome entry

    :param entries: The list of palindrome database entries to append to
    :param palindrome: The palindrome text
    :param created: The creation date of the palindrome
    :param translations: The translations of the palindrome
    :param author: The name of the author of the palindrome

    """
    entries.append(
        DbPalindrome(
            text=maybe_preserve_literal(palindrome),
            author=AUTHORS[author],
            created=created.strftime("%Y-%m-%d"),
            translations=translations,
        )
    )


def print_db_as_yaml(entries: list[DbPalindrome]) -> None:
    """Print the palindrome database as YAML

    :param entries: The palindrome database entries

    """
    yaml = YAML()
    yaml.width = 88  # type: ignore[assignment]
    yaml.dump(entries, sys.stdout)


if __name__ == "__main__":
    main()
