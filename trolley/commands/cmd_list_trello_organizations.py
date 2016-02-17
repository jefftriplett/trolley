import click

from trolley import core
from trolley.cli import pass_context


@click.command('list_trello_organizations')
@pass_context
def cli(context):
    """List your Trello organizations."""

    core.list_trello_organizations(context.settings)
