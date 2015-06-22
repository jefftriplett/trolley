import click

from trolley.cli import pass_context
from trolley.config import config
from trolley.core import test_buffer


@click.command('test_buffer')
@pass_context
def cli(ctx):
    """Test Buffer."""

    try:
        test_buffer(config)
    except Exception as e:
        print e
