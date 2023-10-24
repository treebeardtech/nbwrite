import logging
import os
from pathlib import Path
from unittest.mock import patch

import nbformat
from click.testing import CliRunner
from langchain.llms.fake import FakeListLLM
from nbclient.client import NotebookClient
from py.path import local

from nbwrite.cli import cli

logger = logging.getLogger(__name__)


def test_complete(tmpdir: local):

    if os.getenv("NBWRITE_DEBUG_MODE"):
        outdir = "test-debug-out"
        [pp.unlink() for pp in Path(outdir).glob("*.ipynb")]
    else:
        outdir = str(tmpdir)
    runner = CliRunner()
    args = [
        "complete",
        "tests/resources/nbwrite-in/example.yaml",
        "--out",
        outdir,
    ]

    shell_fmt = " \\\n  ".join(["nbwrite", *args])
    logger.warn(f"Running\n{shell_fmt}")

    with patch("nbwrite.writer.get_llm") as mock_get_llm:
        mock_get_llm.return_value = FakeListLLM(
            responses=["Code:\n```python\nprint('Hello, world!')\n```\n"]
        )
        result = runner.invoke(cli, args)

        assert result.exit_code == 0

        logger.warn(f"Checking outputs in {outdir}")
        outputs = list(Path(outdir).glob("*.ipynb"))
        assert len(outputs) == 2

        nb = nbformat.read(outputs[0], as_version=4)

        client = NotebookClient(nb)
        client.execute()

        for cell in nb.cells:
            if cell.cell_type == "code" and 'print("Hello, world!")' in cell.source:
                assert "Hello, world!" in "".join(
                    output.text for output in cell.outputs
                )
