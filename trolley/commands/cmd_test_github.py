import click

from trolley import core
from trolley.cli import pass_context


@click.command('test_github')
@pass_context
def cli(context):
    """Test GitHub."""

    try:
        context.log('test github')
    except Exception as e:
        print e
