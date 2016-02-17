import click

from trolley import core
from trolley.cli import pass_context


@click.command('delete_existing_github_milestones')
@click.option('--force/--no-force', default=False)
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
@pass_context
def cli(context, force, github_org, github_repo):
    """Delete milestones from GitHub repo."""

    message = 'Do you really want to delete all of the existing GitHub milestones?'
    if force or click.confirm(message):
        core.delete_existing_github_milestones(
            context.settings,
            github_org or context.settings.GITHUB_ORG,
            github_repo or context.settings.GITHUB_REPO,
        )
    else:
        click.echo('Action aborted')
