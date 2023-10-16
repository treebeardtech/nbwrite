from click.testing import CliRunner

from nbwrite.cli import cli


def test_index():
    runner = CliRunner()
    result = runner.invoke(cli, ["index"])
    assert result.exit_code == 0
    assert result.output == "Hello, world!\nBuilding index...\n"


def test_complete():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["complete", "tests/resources/demo.ipynb", "tests/resources/out.ipynb"]
    )
    print(result.output)
    assert result.exit_code == 0

    import nbformat
    from nbclient.client import NotebookClient

    with open("tests/resources/out.ipynb") as f:
        nb = nbformat.read(f, as_version=4)

    client = NotebookClient(nb)
    client.execute()

    for cell in nb.cells:
        if cell.cell_type == "code" and 'print("Hello, world!")' in cell.source:
            assert "Hello, world!" in "".join(output.text for output in cell.outputs)
