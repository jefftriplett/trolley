import click

from trolley import core, options
from trolley.cli import pass_context


@click.command('list_trello_cards')
@options.trello_board_options
@pass_context
def cli(context, trello_board):
    """List your Trello cards for a given board."""

    core.list_trello_cards(
        context.settings,
        trello_board or context.settings.TRELLO_BOARD_ID,
    )
