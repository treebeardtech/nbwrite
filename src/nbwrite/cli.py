from pathlib import Path

import click


@click.group()
def cli():
    """Command line interface for nbwrite."""
    click.echo("Hello, world!")


@cli.command()
def index():
    """Build an index based on the python environment."""
    click.echo("Building index...")


@cli.command()
@click.argument("notebook", type=click.Path(exists=True))
def complete(path: Path):
    """Write demo notebooks based on prompts in the notebook and the index"""
    click.echo("Searching index...")


if __name__ == "__main__":
    cli()
