from click.testing import CliRunner

from nbwrite.cli import cli


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(cli, ["index"])
    assert result.exit_code == 0
    assert result.output == "Hello, world!\nBuilding index...\n"
