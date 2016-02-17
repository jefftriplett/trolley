import click

from trolley import core
from trolley.cli import pass_context


@click.command('create_trello_cards')
@click.option('--filename', default='etc/default_trello_cards.csv')
@click.option('--trello-board', type=str)
@pass_context
def cli(context, filename, trello_board):
    """Create Trello cards from a CSV file."""

    core.create_trello_cards(
        context.settings,
        trello_board or context.settings.TRELLO_BOARD_ID,
        filename,
    )
