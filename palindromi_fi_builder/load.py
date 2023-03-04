"""Subcommand for loading a YAML palindrome database and dumping it to the output"""

import sys
from pathlib import Path

import click

from palindromi_fi_builder.database import read_database, yaml


@click.command()
@click.argument("database_directory", default="./database")
def load(database_directory: str) -> None:
    """Load a YAML palindrome database and dump it to the output
    \f

    :param database_directory: Path to the directory with the palindrome database

    """
    palindromes = read_database(Path(database_directory))
    yaml.dump(palindromes, sys.stdout)
