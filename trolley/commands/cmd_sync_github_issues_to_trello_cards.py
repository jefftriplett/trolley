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


@click.command('sync_github_issues_to_trello_cards')
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
@click.option('--trello-board', type=str)
@pass_context
def cli_sync_github_issues_to_trello_cards(ctx, github_org, github_repo, trello_board):
    """Convert your GitHub issues to Trello cards."""
    sync_github_issues_to_trello_cards(
        config,
        github_org or config.github.org,
        github_repo or config.github.repo,
        trello_board or config.trello.board_id)
