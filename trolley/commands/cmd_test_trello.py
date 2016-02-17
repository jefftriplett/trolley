import click

from trolley import core
from trolley.cli import pass_context


@click.command('test_trello')
@pass_context
def cli(context):
    """Test Trello."""

    try:
        context.log('test trello')
    except Exception as e:
        print e
