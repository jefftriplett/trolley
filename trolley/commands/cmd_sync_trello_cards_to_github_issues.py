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


@click.command('sync_trello_cards_to_github_issues')
@click.option('--trello-board', type=str)
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
@pass_context
def cli(ctx, trello_board, github_org, github_repo):
    """Convert your Trello cards to GitHub issues."""
    sync_trello_cards_to_github_issues(
        config,
        trello_board or config.trello.board_id,
        github_org or config.github.org,
        github_repo or config.github.repo)
