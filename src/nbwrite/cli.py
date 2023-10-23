import json
from pathlib import Path
from typing import List

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
    "task",
    type=str,
)
@click.option(
    "--step", default=[], multiple=True, help="Steps in the problem solving process"
)
@click.option(
    "--package", default=[], multiple=True, help="Local Python packages to use for RAG"
)
@click.option(
    "--out",
    type=click.Path(exists=False, path_type=Path, dir_okay=True, file_okay=False),
    default="out",
    help="The directory to write the generated notebooks to",
)
@click.option(
    "--model",
    default=["gpt-3.5-turbo"],
    multiple=True,
    help="The API names of the models as per https://platform.openai.com/docs/models/ and https://app.endpoints.anyscale.com/",
)
@click.option(
    "--generations",
    default=1,
    type=int,
    help="The number of notebooks to generate per model",
)
@click.option(
    "--phoenix-trace/--no-phoenix-trace",
    default=False,
    type=bool,
    help="Whether to trace using Phoenix https://docs.arize.com/phoenix/",
)
def complete(
    task: str,
    step: List[str],
    package: List[str],
    out: Path,
    model: List[str],
    generations: int,
    phoenix_trace: bool,
):
    """Writes example notebooks which complete a given TASK

    e.g. nbwrite complete "Use Pandas to visualise the Titanic dataset"
    """
    config = {
        "task": task,
        "steps": step,
        "packages": package,
        "out": str(out),
        "models": model,
        "generations": generations,
        "phoenix_trace": phoenix_trace,
    }

    click.echo(f"Writing notebook with options:\n\n{json.dumps(config, indent=2)}")


if __name__ == "__main__":
    cli()
