"""Dump derived site YAML, including identifiers and navigation, to stdout."""

import sys
from pathlib import Path

import click

from palindromi_fi_builder.database import read_database
from palindromi_fi_builder.yaml_utils import create_yaml_dumper


@click.command()
@click.argument("database_directory", default="./database")
def load(database_directory: str) -> None:
    """Dump derived site YAML, not a lossless database backup
    \f

    Reads curated palindromes/*.yaml through read_database(). Source fields such
    as grading and series are omitted. The default database directory is ./database.

    :param database_directory: Path to the directory with the palindrome database

    """
    palindromes = read_database(Path(database_directory))
    yaml = create_yaml_dumper()
    yaml.dump(palindromes, sys.stdout)
