import click

from trolley import core
from trolley.cli import pass_context


@click.command('sync_github_issues_to_trello_cards')
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
@click.option('--trello-board', type=str)
@pass_context
def cli(context, github_org, github_repo, trello_board):
    """Convert your GitHub issues to Trello cards."""

    core.sync_github_issues_to_trello_cards(
        context.settings,
        github_org or context.settings.GITHUB_ORG,
        github_repo or context.settings.GITHUB_REPO,
        trello_board or context.settings.TRELLO_BOARD_ID)
