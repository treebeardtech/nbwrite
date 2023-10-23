from pathlib import Path

import click
from dotenv import load_dotenv

import nbwrite.writer as writer

load_dotenv()


@click.group()
def cli():
    """Command line interface for nbwrite."""
    pass


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
