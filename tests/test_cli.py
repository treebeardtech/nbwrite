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
