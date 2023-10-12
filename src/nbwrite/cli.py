from pathlib import Path

import click

import nbwrite.writer as writer


@click.group()
def cli():
    """Command line interface for nbwrite."""
    click.echo("Hello, world!")


@cli.command()
def index():
    """Build an index based on the python environment."""
    click.echo("Building index...")


@cli.command()
@click.argument(
    "notebook", type=click.Path(exists=True, path_type=Path, dir_okay=False)
)
@click.argument("out", type=click.Path(exists=False, path_type=Path, dir_okay=False))
def complete(notebook: Path, out: Path):
    """Write demo notebooks based on prompts in the notebook and the index"""
    click.echo("Searching index...")
    writer.complete(notebook, out)


if __name__ == "__main__":
    cli()
