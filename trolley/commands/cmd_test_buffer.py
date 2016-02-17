import click

from trolley import core
from trolley.cli import pass_context


@click.command('test_buffer')
@pass_context
def cli(context):
    """Test Buffer."""

    try:
        core.test_buffer(context.settings)
    except Exception as e:
        print e
