import click

from trolley import core, options
from trolley.cli import pass_context


@click.command('bootstrap')
@options.github_org_options
@options.github_repo_options
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
