"""Command line interface for palindromi.fi builder."""

import sys
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List

import click
import pkg_resources
import ruamel.yaml
from base58 import b58encode
from jinja2 import Environment, PackageLoader

from palindromi_fi_builder.syncer import Syncer
from palindromi_fi_builder.typography import add_typography

yaml = ruamel.yaml.YAML()


PAGE_EXTENSION = ''


def read_database(database_directory: Path):
    palindromes = None
    yaml_paths = (database_directory / 'palindromes').glob('*.yaml')
    for database_file_path in sorted(yaml_paths):
        with database_file_path.open() as database_file:
            next_batch = yaml.load(database_file)
        if not palindromes:
            palindromes = next_batch
        else:
            palindromes.extend(next_batch)
    for palindrome in palindromes:
        palindrome['identifier'] = calculate_identifier(palindrome['text'])
        palindrome['links'] = {}
    for older, newer in zip(palindromes, palindromes[1:] + [palindromes[0]]):
        # reverse order: last one is newest, forwards goes back in time
        newer['links']['next'] = older['identifier']
        older['links']['previous'] = newer['identifier']
    return palindromes


@click.group()
def cli():
    pass


@cli.command()
@click.argument('database_directory', default='./database')
def load(database_directory: str):
    palindromes = read_database(Path(database_directory))
    yaml.dump(palindromes, sys.stdout)


def calculate_identifier(text: str):
    text_bytes = text.encode('utf-8')
    hashed = sha256(text_bytes)
    hash_4_bytes = hashed.digest()[:4]
    base58_bytes = b58encode(hash_4_bytes)
    base58_str = base58_bytes.decode('ascii')
    return base58_str


def render_palindrome_page(
    palindrome: Dict, illustrations: List[str], static_url: str
) -> str:
    """Render one palindrome and illustrations to HTML page using the Jinja2 template

    :param palindrome: Data for the palindrome to render
    :param illustrations: List of illustration filenames for the palindrome
    :param static_url: URL prefix for static files
    :return: Rendered HTML page

    """
    env = Environment(loader=PackageLoader("palindromi_fi_builder"))
    env.filters["add_typography"] = add_typography
    template = env.get_template("palindrome.html")
    return template.render(
        static_url=static_url,
        illustrations=illustrations,
        palindrome=palindrome,
        PAGE_EXTENSION=PAGE_EXTENSION,
    )


@cli.command()
@click.argument('database_directory', default='./database')
@click.option('-o', '--output-directory', default='./html')
def render(database_directory: str,
           output_directory: str):
    """Render all palindromes and images to HTML pages, don't touch unmodified ones

    :param database_directory: Path to the directory with the palindrome database
    :param output_directory: Path to the output directory for the HTML pages and static
                             content

    """
    db_dir = Path(database_directory)
    palindromes = read_database(db_dir)
    html_root = Path(output_directory)
    syncer = Syncer(html_root)

    static_url = 'static'
    static_destination = html_root / static_url
    static_source = pkg_resources.resource_filename('palindromi_fi_builder',
                                                    'static')
    syncer.copytree(Path(static_source), static_destination)

    for palindrome in palindromes:
        palindrome_path = render_palindrome_and_illustrations(
            db_dir, html_root, palindrome, static_url, syncer
        )
        if palindrome is palindromes[-1]:
            syncer.copy(palindrome_path, html_root / "index.html")

    syncer.remove_deleted()


def render_palindrome_and_illustrations(
    db_dir: Path,
    html_root: Path,
    palindrome: Dict[str, Any],
    static_url: str,
    syncer: Syncer,
) -> Path:
    """Render one palindrome and its illustrations to files in the destination directory

    Don't touch unmodified files, return the path to the rendered

    :param db_dir: Path to the database directory
    :param html_root: Path to the root of the HTML directory
    :param palindrome: The palindrome to render
    :param static_url: URL prefix for static files
    :param syncer: Syncer instance
    :return: Path to the rendered HTML page

    """
    identifier = palindrome["identifier"]
    illustrations = palindrome.get("illustrations", [])
    illustrations_paths = []
    for index, illustration in enumerate(illustrations):
        dest_name = f"{identifier}{index}.jpg"
        syncer.copy(
            db_dir / "illustrations" / illustration["image"],
            html_root / static_url / dest_name,
        )
        illustrations_paths.append(dest_name)
    palindrome_path = html_root / f"{identifier}{PAGE_EXTENSION}"
    rendered = render_palindrome_page(palindrome, illustrations_paths, static_url)
    syncer.write_text(rendered, palindrome_path)
    return palindrome_path


def main():
    cli()


if __name__ == '__main__':
    main()
