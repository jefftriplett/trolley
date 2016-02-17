import click

from trolley import core, options
from trolley.cli import pass_context


@click.command('create_github_labels')
@click.option('--filename', default='etc/default_github_labels.csv')
@options.github_org_options
@options.github_repo_options
@pass_context
def cli(context, filename, github_org, github_repo):
    """Create GitHub labels from a CSV file."""

    core.create_github_labels(
        context.settings,
        github_org or context.settings.GITHUB_ORG,
        github_repo or context.settings.GITHUB_REPO,
        filename,
    )
