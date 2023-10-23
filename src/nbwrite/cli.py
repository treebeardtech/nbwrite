import json
from pathlib import Path
from typing import List

import click
from dotenv import load_dotenv

import nbwrite.writer as writer
from nbwrite.constants import DEFAULT_MODEL

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
    type=click.Path(path_type=Path, dir_okay=True, file_okay=False),
    default="nbwrite-out",
    help="The directory to write the generated notebooks to",
)
@click.option(
    "--model",
    default=[DEFAULT_MODEL],
    multiple=True,
    help="The API names of the models as per https://platform.openai.com/docs/models/ and https://app.endpoints.anyscale.com/",
)
@click.option(
    "--generations",
    default=1,
    type=int,
    help="The number of notebooks to generate per model",
)
def complete(
    task: str,
    step: List[str],
    package: List[str],
    out: Path,
    model: List[str],
    generations: int,
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
    }

    click.echo(f"Writing notebook with options:\n\n{json.dumps(config, indent=2)}")

    conf_obj = writer.Config(**config)
    writer.gen(conf_obj)


if __name__ == "__main__":
    cli()
