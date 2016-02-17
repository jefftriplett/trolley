import click

from trolley import core, options
from trolley.cli import pass_context


@click.command('close_existing_github_issues')
@options.force_options
@options.github_org_options
@options.github_repo_options
@pass_context
def cli(context, force, github_org, github_repo):
    """Close all existing GitHub issues."""

    message = 'Do you really want to close all of your existing GitHub issues?'
    if force or click.confirm(message):
        core.close_existing_github_issues(
            context.settings,
            github_org or context.settings.GITHUB_ORG,
            github_repo or context.settings.GITHUB_REPO,
        )
    else:
        click.echo('Action aborted')
