import click

from trolley import core
from trolley.cli import pass_context


@click.command('list_trello_cards')
@click.option('--trello-board', type=str)
@pass_context
def cli(context, trello_board):
    """List your Trello cards for a given board."""

    core.list_trello_cards(
        context.settings,
        trello_board or context.settings.TRELLO_BOARD_ID,
    )
