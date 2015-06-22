import click
import os

from trolley.cli import pass_context
from trolley.config import commit_changes, config, create_config, CONFIG_FILE
from trolley.core import (
    close_existing_github_issues,
    create_github_issues,
    create_github_labels,
    create_github_milestones,
    create_trello_cards,
    create_trello_labels,
    create_trello_lists,
    delete_existing_github_labels,
    delete_existing_github_milestones,
    list_trello_boards,
    list_trello_cards,
    list_trello_organizations,
    sync_github_issues_to_trello_cards,
    sync_trello_cards_to_github_issues,
    test_buffer,
)


@click.command('create_config')
@pass_context
def cli(ctx):
    """Create Config."""

    if os.path.exists(CONFIG_FILE):
        pass
    else:
        create_config()
        commit_changes()
