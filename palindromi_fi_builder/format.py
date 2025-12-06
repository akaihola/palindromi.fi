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

    # Apply formatting rules to text fields
    for palindrome in palindromes:
        # Format the main palindrome text
        if "text" in palindrome and isinstance(palindrome["text"], str):
            palindrome["text"] = maybe_preserve_literal(palindrome["text"])

        # Format all translation texts
        if "translations" in palindrome:
            for translation in palindrome["translations"]:
                if "text" in translation and isinstance(translation["text"], str):
                    translation["text"] = maybe_preserve_literal(translation["text"])

    # Dump with formatted YAML
    buffer = StringIO()
    yaml.dump(palindromes, buffer)
    formatted_yaml = buffer.getvalue()

    # Write if changed, preserving timestamps
    return syncer.write_text(formatted_yaml, yaml_file)


@click.command()
@click.argument("path", default="./database/palindromes", type=click.Path(exists=True))
def format(path: str) -> None:
    """Reformat palindrome database files with consistent YAML formatting
    \f

    Reformats YAML files using standard formatting rules:
    - Short text values (≤50 characters) stay inline
    - Longer/multi-line text uses YAML block literal format (|-)
    - Line width set to 88 characters (matching Black formatter)

    Only writes files that have changed, preserving timestamps for unchanged files.

    PATH can be:
    - A directory (reformats all *.yaml files in it)
    - A single YAML file (reformats that file only)

    :param path: Path to a YAML file or directory containing YAML files

    """
    target = Path(path)

    if target.is_file():
        # Single file
        if not target.suffix == ".yaml":
            click.echo(f"Error: Not a YAML file: {target}", err=True)
            sys.exit(1)

        syncer = Syncer(target.parent)
        if reformat_yaml_file(target, syncer):
            click.echo(f"Updated: {target.name}")
        else:
            click.echo(f"Unchanged: {target.name}")

    elif target.is_dir():
        # Directory
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
