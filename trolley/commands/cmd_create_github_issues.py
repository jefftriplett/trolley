import click

from trolley import core
from trolley.cli import pass_context


@click.command('create_github_issues')
@click.option('--filename', default='etc/default_github_issues.csv')
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
@pass_context
def cli(context, filename, github_org, github_repo):
    """Create GitHub issues from a CSV file."""

    core.create_github_issues(
        context.settings,
        github_org or context.settings.GITHUB_ORG,
        github_repo or context.settings.GITHUB_REPO,
        filename,
    )
