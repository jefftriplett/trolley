import click

from trolley.cli import pass_context
from trolley.config import config
from trolley.core import (
    close_existing_github_issues,
    create_github_issues,
    create_github_labels,
    create_github_milestones,
    create_trello_cards,
    create_trello_labels,
    create_trello_lists,
    delete_existing_github_labels,
    delete_existing_github_milestones,
    list_trello_boards,
    list_trello_cards,
    list_trello_organizations,
    sync_github_issues_to_trello_cards,
    sync_trello_cards_to_github_issues,
    test_buffer,
)


@click.command('create_trello_lists')
@click.option('--filename', default='etc/default_trello_lists.csv')
@click.option('--trello-board', type=str)
@pass_context
def cli(ctx, filename, trello_board):
    """Create Trello lists from a CSV file."""

    create_trello_lists(
        config,
        trello_board or config.trello.board_id,
        filename)
