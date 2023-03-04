"""Command line interface for palindromi.fi builder."""

import click

from palindromi_fi_builder.load import load
from palindromi_fi_builder.render import render


@click.group()
def cli():
    pass


def main():
    cli.add_command(render)
    cli.add_command(load)
    cli()


if __name__ == "__main__":
    main()
