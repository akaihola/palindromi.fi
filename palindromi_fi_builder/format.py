"""Subcommand for reformatting palindrome database files with consistent YAML formatting"""

import sys
from io import StringIO
from pathlib import Path

import click

from palindromi_fi_builder.database import DbPalindrome
from palindromi_fi_builder.syncer import Syncer
from palindromi_fi_builder.yaml_utils import create_yaml_dumper


def reformat_yaml_file(yaml_file: Path, syncer: Syncer) -> bool:
    """Reformat a single YAML file with the standard dumper.

    :param yaml_file: Path to the YAML file to reformat
    :param syncer: Syncer instance for tracking changes
    :return: True if file was written, False if unchanged

    """
    from palindromi_fi_builder.yaml_utils import maybe_preserve_literal

    yaml = create_yaml_dumper()
    with yaml_file.open() as f:
        palindromes: list[DbPalindrome] = yaml.load(f) or []

    for palindrome in palindromes:
        if "text" in palindrome and isinstance(palindrome["text"], str):
            palindrome["text"] = maybe_preserve_literal(palindrome["text"])

        if "translations" in palindrome:
            for translation in palindrome["translations"]:
                if "text" in translation and isinstance(translation["text"], str):
                    translation["text"] = maybe_preserve_literal(translation["text"])

    buffer = StringIO()
    yaml.dump(palindromes, buffer)
    formatted_yaml = buffer.getvalue()

    return syncer.write_text(formatted_yaml, yaml_file)


@click.command()
@click.argument("path", default="./database/palindromes", type=click.Path(exists=True))
def format(path: str) -> None:
    """Reformat palindrome database files with consistent YAML formatting
    \f

    Applies maybe_preserve_literal() to palindrome and translation text fields.
    Values of at most 50 characters without LF newlines are left by the helper;
    other values use literal blocks with chomping based on trailing newlines. Conversion
    normalizes CRLF/CR to LF. The dumper's preferred line width is 88 characters.

    Only writes files that have changed, preserving timestamps for unchanged files.

    PATH can be:
    - A directory (reformats its immediate *.yaml files)
    - A single YAML file (reformats that file only)

    Defaults to ./database/palindromes. Does not validate or publish entries.

    :param path: Path to a YAML file or directory containing YAML files

    """
    target = Path(path)

    if target.is_file():
        if not target.suffix == ".yaml":
            click.echo(f"Error: Not a YAML file: {target}", err=True)
            sys.exit(1)

        syncer = Syncer(target.parent)
        if reformat_yaml_file(target, syncer):
            click.echo(f"Updated: {target.name}")
        else:
            click.echo(f"Unchanged: {target.name}")

    elif target.is_dir():
        syncer = Syncer(target)
        yaml_files = sorted(target.glob("*.yaml"))

        if not yaml_files:
            click.echo(f"No YAML files found in {target}")
            return

        files_processed = 0
        files_changed = 0

        for yaml_file in yaml_files:
            files_processed += 1
            if reformat_yaml_file(yaml_file, syncer):
                files_changed += 1
                click.echo(f"Updated: {yaml_file.name}")
            else:
                click.echo(f"Unchanged: {yaml_file.name}")

        click.echo(f"\nProcessed {files_processed} file(s), {files_changed} changed")

    else:
        click.echo(f"Error: Path not found: {target}", err=True)
        sys.exit(1)
