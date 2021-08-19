import re
import os
from os.path import join

import click

from .base import app


@app.command('clear')
def clear_command() -> None:
    """
    Clears the resources directory.
    """
    clear()


def clear() -> None:
    """
    Function version of `clear_command` to be available in the package.
    """
    pattern = re.compile(r'.+\.(xml|md|props)$')
    resources_path = 'resources'
    for file_name in os.listdir(resources_path):
        if not re.match(pattern, file_name):
            file_path = join(resources_path, file_name)
            os.remove(file_path)
            click.echo(f'{file_name} removed.')
