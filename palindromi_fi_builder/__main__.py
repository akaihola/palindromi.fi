import shutil
import sys
from hashlib import sha256
from pathlib import Path
from typing import Dict, List

import click
import pkg_resources
import ruamel.yaml
from base58 import b58encode
from jinja2 import PackageLoader, Environment

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


def render_palindrome(palindrome: Dict,
                      palindrome_path: Path,
                      illustrations: List[str],
                      static_url: str):
    env = Environment(loader=PackageLoader('palindromi_fi_builder'))
    env.filters['add_typography'] = add_typography
    template = env.get_template('palindrome.html')
    new_content = template.render(static_url=static_url,
                                  illustrations=illustrations,
                                  palindrome=palindrome,
                                  PAGE_EXTENSION=PAGE_EXTENSION)
    if palindrome_path.is_file():
        old_content = palindrome_path.read_text()
    else:
        old_content = ''
    if new_content != old_content:
        with palindrome_path.open('w'):
            palindrome_path.write_text(new_content)


@cli.command()
@click.argument('database_directory', default='./database')
@click.option('-o', '--output-directory', default='./html')
def render(database_directory: str,
           output_directory: str):
    db_dir = Path(database_directory)
    ill_dir = db_dir / 'illustrations'
    palindromes = read_database(db_dir)
    html_root = Path(output_directory)

    static_url = 'static'
    static_destination = html_root / static_url
    shutil.rmtree(static_destination, ignore_errors=True)
    static_source = pkg_resources.resource_filename('palindromi_fi_builder',
                                                    'static')
    shutil.copytree(static_source, static_destination)

    for palindrome in palindromes:
        illustrations_paths = []
        identifier = palindrome['identifier']
        illustrations = palindrome.get('illustrations', [])
        for index, illustration in enumerate(illustrations):
            dest_name = f'{identifier}{index}.jpg'
            shutil.copy(ill_dir / illustration['image'],
                        static_destination / dest_name)
            illustrations_paths.append(dest_name)
        palindrome_path = html_root / f'{identifier}{PAGE_EXTENSION}'
        render_palindrome(palindrome,
                          palindrome_path,
                          illustrations_paths,
                          static_url)
        if palindrome is palindromes[-1]:
            shutil.copy(palindrome_path, html_root / 'index.html')


def main():
    cli()


if __name__ == '__main__':
    main()
