import click

from trolley import core
from trolley.cli import pass_context


@click.command('sync_trello_cards_to_github_issues')
@click.option('--trello-board', type=str)
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
@pass_context
def cli(context, trello_board, github_org, github_repo):
    """Convert your Trello cards to GitHub issues."""

    core.sync_trello_cards_to_github_issues(
        context.settings,
        trello_board or context.settings.TRELLO_BOARD_ID,
        github_org or context.settings.GITHUB_ORG,
        github_repo or context.settings.GITHUB_REPO)
