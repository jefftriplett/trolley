import click

from trolley.cli import pass_context
from trolley.config import config
from trolley.core import test_buffer


@click.command('test_trello')
@pass_context
def cli(ctx):
    """Test Trello."""

    try:
        ctx.log('test trello')
    except Exception as e:
        print e
