import click


@click.group(name='hazm', help='hazm\'s Command-line Interface')
def app():
    pass


def setup_cli():
    """
    Setups command-line interface for hazm.
    """
    # Ensure that the help messages always display the correct prompt
    app(prog_name='python -m hazm')
