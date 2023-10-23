import logging
from pathlib import Path

from click.testing import CliRunner
from py.path import local

from nbwrite.cli import cli

placeholder_task = "Create a hello world notebook 'x.ipynb', use nbmake's NotebookRun class to test it from a Python application"


def test_complete(tmpdir: local):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
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
        ],
    )
    assert result.exit_code == 0

    import nbformat
    from nbclient.client import NotebookClient

    outputs = list(Path(tmpdir).glob("*.ipynb"))
    assert len(outputs) == 1
    #     nb = nbformat.read(f, as_version=4)

    # client = NotebookClient(nb)
    # client.execute()

    # for cell in nb.cells:
    #     if cell.cell_type == "code" and 'print("Hello, world!")' in cell.source:
    #         assert "Hello, world!" in "".join(output.text for output in cell.outputs)
