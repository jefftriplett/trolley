import click

from trolley import core, options
from trolley.cli import pass_context


@click.command('delete_existing_github_labels')
@options.force_options
@options.github_org_options
@options.github_repo_options
@pass_context
def cli(context, force, github_org, github_repo):
    """Delete labels from GitHub repo."""

    message = 'Do you really want to delete all of the existing GitHub labels?'
    if force or click.confirm(message):
        core.delete_existing_github_labels(
            context.settings,
            github_org or context.settings.GITHUB_ORG,
            github_repo or context.settings.GITHUB_REPO,
        )
    else:
        click.echo('Action aborted')
