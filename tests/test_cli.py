import logging
from pathlib import Path
from typing import List

import nbformat
from click.testing import CliRunner
from nbclient.client import NotebookClient
from py.path import local

from nbwrite.cli import cli

logger = logging.getLogger(__name__)

placeholder_task = "Create a hello world notebook 'x.ipynb', use nbmake's NotebookRun class to test it from a Python application"


def test_complete(tmpdir: local):
    runner = CliRunner()
    args = [
        "complete",
        placeholder_task,
        "--step",
        "create a hello world notebook using nbformat",
        "--step",
        "use nbmake's NotebookRun class to execute it from a Python application",
        "--step",
        "check the output notebook printed what we were expecting",
        "--package",
        "nbmake",
        "--package",
        "nbformat",
        "--package",
        "nbclient",
        "--out",
        str(tmpdir),
    ]

    shell_fmt = " \\\n  ".join(["nbwrite", *args])
    logger.warn(f"Running\n{shell_fmt}")
    result = runner.invoke(cli, args)

    assert result.exit_code == 0

    logger.warn(f"Checking outputs in {tmpdir}")
    outputs = list(Path(tmpdir).glob("*.ipynb"))
    assert len(outputs) == 1
    #     nb = nbformat.read(f, as_version=4)

    # client = NotebookClient(nb)
    # client.execute()

    # for cell in nb.cells:
    #     if cell.cell_type == "code" and 'print("Hello, world!")' in cell.source:
    #         assert "Hello, world!" in "".join(output.text for output in cell.outputs)
