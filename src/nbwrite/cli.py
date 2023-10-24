import json
import os
from pathlib import Path

import click
import yaml
from dotenv import load_dotenv
from rich import print

import nbwrite.writer as writer
from nbwrite.config import Config

load_dotenv()


@click.group()
def cli():
    """Command line interface for nbwrite."""
    pass


@cli.command()
@click.argument(
    "spec",
    type=click.Path(path_type=Path, dir_okay=False, file_okay=True),
)
@click.option(
    "--out",
    type=click.Path(path_type=Path, dir_okay=True, file_okay=False),
    default="nbwrite-out",
    help="The directory to write the generated notebooks to",
)
def complete(
    spec: Path,
    out: Path,
):
    """Writes example notebooks which complete a given SPEC

    e.g. nbwrite complete "./spec.yaml"
    """

    spec = yaml.safe_load(spec.read_text())
    config = Config(**{**spec, "out": str(out)})

    if os.getenv("NBWRITE_DEBUG_MODE"):
        print(config)

    writer.gen(config)


if __name__ == "__main__":
    cli()
