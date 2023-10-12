import click


@click.command()
def cli():
    """Command line interface for nbwrite."""
    click.echo("Hello, world!")


if __name__ == "__main__":
    cli()
