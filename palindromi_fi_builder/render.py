"""Subcommand for rendering the palindrome database to HTML pages"""

from pathlib import Path
from typing import List

import click
import pkg_resources
from jinja2 import Environment, PackageLoader

from palindromi_fi_builder.database import SitePalindrome, read_database
from palindromi_fi_builder.syncer import Syncer
from palindromi_fi_builder.typography import add_typography

PAGE_EXTENSION = ""


def render_palindrome_page(
    palindrome: SitePalindrome, illustration_filenames: List[str], static_url: str
) -> str:
    """Render one palindrome and illustrations to HTML page using the Jinja2 template

    :param palindrome: Data for the palindrome to render
    :param illustration_filenames: List of illustration filenames for the palindrome
    :param static_url: URL prefix for static files
    :return: Rendered HTML page

    """
    env = Environment(loader=PackageLoader("palindromi_fi_builder"))
    env.filters["add_typography"] = add_typography
    template = env.get_template("palindrome.html")
    return template.render(
        static_url=static_url,
        illustrations=illustration_filenames,
        palindrome=palindrome,
        PAGE_EXTENSION=PAGE_EXTENSION,
    )


@click.command()
@click.argument("database_directory", default="./database")
@click.option(
    "-o",
    "--output-directory",
    default="./html",
    help="The directory to render the static webpages into",
)
def render(database_directory: str, output_directory: str) -> None:
    """Render all palindromes and images to HTML pages, don't touch unmodified ones
    \f

    :param database_directory: Path to the directory with the palindrome database
    :param output_directory: Path to the output directory for the HTML pages and static
                             content

    """
    db_dir = Path(database_directory)
    palindromes = read_database(db_dir)
    html_root = Path(output_directory)
    syncer = Syncer(html_root)

    static_url = "static"
    static_destination = html_root / static_url
    static_source = pkg_resources.resource_filename("palindromi_fi_builder", "static")
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
    palindrome: SitePalindrome,
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
    illustrations_filenames = []
    for index, illustration in enumerate(illustrations):
        dest_name = f"{identifier}{index}.jpg"
        syncer.copy(
            db_dir / "illustrations" / illustration["image"],
            html_root / static_url / dest_name,
        )
        illustrations_filenames.append(dest_name)
    palindrome_path = html_root / f"{identifier}{PAGE_EXTENSION}"
    rendered = render_palindrome_page(palindrome, illustrations_filenames, static_url)
    syncer.write_text(rendered, palindrome_path)
    return palindrome_path
