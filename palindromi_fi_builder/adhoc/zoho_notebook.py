"""Load palindromes from a Zoho Notebook."""

import argparse
import logging
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from itertools import chain
from urllib.parse import urlsplit

import requests

from palindromi_fi_builder.database import DbPalindrome, Translation
from palindromi_fi_builder.palindrome import is_palindrome

logger = logging.getLogger(__name__)


class Namespace(argparse.Namespace):  # pylint: disable=too-few-public-methods
    """Namespace class for options recognized by the argument parser. Helps Mypy."""

    url: str


def load_zoho_notebook_palindromes() -> Iterable[DbPalindrome]:
    """Load palindromes from a Zoho Notebook.

    The notebook URL is expected to be passed as the first argument to the script.

    :yields: Palindromes in the database format

    """
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL of the Zoho Notebook")
    opts = parser.parse_args(namespace=Namespace())
    logger.info("Loading palindromes from %s", opts.url)
    # The notebook URL is of the form:
    #   https://notebook.zoho.eu/app/index.html#/notebooks/<BOOK>/notecards/<CARD>
    # We need to extract the <CARD> part from the URL and use it to construct
    # the API URL for the notecard text content:
    #   https://notebook.zohopublic.eu/api/v1/public/notecards/<CARD>
    notecard_hash = urlsplit(opts.url).fragment.rsplit("/", 1)[-1]
    api_url = f"https://notebook.zohopublic.eu/api/v1/public/notecards/{notecard_hash}"
    response = requests.get(api_url, timeout=10)
    # parse response using ElementTree
    response_content: ET.Element = ET.fromstring(response.text)
    notebook_doc: ET.Element = ET.fromstring(
        response_content.findtext("ZContent") or ""
    )
    br_to_newline(notebook_doc)
    block: list[str]
    palindrome: str
    translation: str
    for block in split_by_empty_lines(notebook_doc.itertext()):
        try:
            palindrome, translation = parse_block(block)
        except NoPalindromeFound as exc_info:
            logger.warning("Not a palindrome: %s", exc_info)
            continue
        yield DbPalindrome(
            text=palindrome,
            translations=[
                Translation(language="en", text=translation, author="Antti Kaihola")
            ]
            if translation
            else [],
            author="Antti Kaihola",
        )


def br_to_newline(html_root: ET.Element) -> None:
    """Convert ``<br>`` tags to newlines

    :param html_root: The root element of the HTML document. Modified in-place.

    """
    parent: ET.Element
    for parent in html_root.findall(".//*[br]"):
        br_tags: list[ET.Element] = parent.findall(".//br")
        br_tails: str = "\n".join(br.tail or "" for br in br_tags)
        for br_tag in br_tags:
            parent.remove(br_tag)
        parent.text = f"{parent.text or ''}\n{br_tails}"


def split_by_empty_lines(content_stream: Iterable[str]) -> Iterable[list[str]]:
    """Split a stream of text into blocks separated by empty lines

    :param content_stream: The stream of text
    :yield: The blocks of text

    """
    current_block: list[str] = []
    for line in chain("".join(content_stream).splitlines(), [""]):
        if line.strip():
            current_block.append(line)
        elif current_block:
            yield current_block
            current_block = []


class NoPalindromeFound(Exception):
    """Raised when a block of text does not contain a palindrome"""


def parse_block(lines: list[str]) -> tuple[str, str]:
    """Parse a block of text into a palindrome and its translation

    :param lines: The lines of the block
    :return: A tuple of the palindrome and its translation
    :raises ValueError: If the block does not contain a palindrome

    """
    for num_palindrome_lines in range(1, len(lines) + 1):
        palindrome = "\n".join(line.rstrip() for line in lines[:num_palindrome_lines])
        if is_palindrome(palindrome):
            translation = "\n".join(lines[num_palindrome_lines:])
            return palindrome, translation
    raise NoPalindromeFound(f"Could not find palindrome in block: {lines}")


def main() -> None:
    """Load palindromes from a Zoho Notebook and print them to stdout."""
    for palindrome in load_zoho_notebook_palindromes():
        print(palindrome)


if __name__ == "__main__":
    main()
