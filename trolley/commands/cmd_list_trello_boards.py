import click

from trolley import core
from trolley.cli import pass_context


@click.command('list_trello_boards')
@pass_context
def cli(context):
    """List your Trello boards."""

    core.list_trello_boards(context.settings)
