import click

from trolley import core
from trolley.cli import pass_context


@click.command('bootstrap')
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
@pass_context
def cli(context, github_org, github_repo):
    """Sets up github with some sensible defaults."""

    core.delete_existing_github_labels(
        context.settings,
        github_org or context.settings.GITHUB_ORG,
        github_repo or context.settings.GITHUB_REPO,
    )

    core.create_github_labels(
        context.settings,
        github_org or context.settings.GITHUB_ORG,
        github_repo or context.settings.GITHUB_REPO,
    )

    core.create_github_issues(
        context.settings,
        github_org or context.settings.GITHUB_ORG,
        github_repo or context.settings.GITHUB_REPO,
    )

    core.create_github_milestones(
        context.settings,
        github_org or context.settings.GITHUB_ORG,
        github_repo or context.settings.GITHUB_REPO,
    )
