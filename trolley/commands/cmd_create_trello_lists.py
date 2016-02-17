import click

from trolley import core, options
from trolley.cli import pass_context


@click.command('create_trello_lists')
@click.option('--filename', default='etc/default_trello_lists.csv')
@options.trello_board_options
@pass_context
def cli(context, filename, trello_board):
    """Create Trello lists from a CSV file."""

    core.create_trello_lists(
        context.settings,
        trello_board or context.settings.TRELLO_BOARD_ID,
        filename,
    )
