import click
import os

from trolley.cli import pass_context
from trolley.config import commit_changes, create_config, CONFIG_FILE


@click.command('create_config')
@pass_context
def cli(context):
    """Create Config."""

    if os.path.exists(CONFIG_FILE):
        pass
    else:
        create_config()
        commit_changes()
