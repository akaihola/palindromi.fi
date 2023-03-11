"""Read a palindrome database and convert it to the format for rendering the site."""

from hashlib import sha256
from pathlib import Path
from typing import List, NotRequired, TypedDict, cast

import ruamel.yaml
from base58 import b58encode

yaml = ruamel.yaml.YAML()


class Illustration(TypedDict):
    """Metadata about an illustration for a palindrome"""

    image: str
    author: str
    has_text: bool


class Translation(TypedDict):
    """A translation of a palindrome"""

    language: str
    text: str
    author: str


class DbPalindrome(TypedDict):
    """A palindrome in the palindrome YAML database format"""

    text: str
    author: str
    illustrations: NotRequired[List[Illustration]]
    translations: List[Translation]
    created: NotRequired[str]


class Links(TypedDict):
    """Links to the preceding and following palindromes on the site"""

    next: NotRequired[str]
    previous: NotRequired[str]


class SitePalindrome(DbPalindrome):
    """A palindrome in the format for rendering the site"""

    identifier: str
    links: Links


def db_to_site_palindrome(db_palindrome: DbPalindrome) -> SitePalindrome:
    """Convert a palindrome from the database format to the site format

    :param db_palindrome: A palindrome in the database format
    :return: The palindrome in the site format

    """
    site_palindrome = SitePalindrome(
        identifier=calculate_identifier(db_palindrome["text"]),
        text=db_palindrome["text"],
        author=db_palindrome["author"],
        translations=db_palindrome["translations"],
        links={},
    )
    if "illustrations" in db_palindrome:
        site_palindrome["illustrations"] = db_palindrome["illustrations"]
    if "created" in db_palindrome:
        site_palindrome["created"] = db_palindrome["created"]
    return site_palindrome


def read_database(database_directory: Path) -> List[SitePalindrome]:
    """Read a palindrome YAML database and return palindromes in the site format

    :param database_directory: Path to the directory with the palindrome database
    :return: List of palindromes in the site format

    """
    db_palindromes: List[DbPalindrome] = []
    yaml_paths = (database_directory / "palindromes").glob("*.yaml")
    for database_file_path in sorted(yaml_paths):
        with database_file_path.open() as database_file:
            next_batch = cast(List[DbPalindrome], yaml.load(database_file))
        db_palindromes.extend(next_batch)
    site_palindromes = [
        db_to_site_palindrome(palindrome) for palindrome in db_palindromes
    ]
    for older, newer in zip(
        site_palindromes, site_palindromes[1:] + [site_palindromes[0]]
    ):
        # reverse order: last one is newest, forwards goes back in time
        newer["links"]["next"] = older["identifier"]
        older["links"]["previous"] = newer["identifier"]
    return site_palindromes


def calculate_identifier(text: str) -> str:
    """Calculate the identifier for a palindrome from its text

    :param text: The palindrome text
    :return: The palindrome identifier

    """
    text_bytes = text.encode("utf-8")
    hashed = sha256(text_bytes)
    hash_4_bytes = hashed.digest()[:4]
    base58_bytes = b58encode(hash_4_bytes)
    base58_str = base58_bytes.decode("ascii")
    return base58_str
