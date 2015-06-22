#!/usr/bin/env python
"""
Trolley syncs issues between CSV, Github, and Buffer with Trello.

"""

import click
import click_config

from trolley.config import config
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


def print_version(ctx, param, value):
    from trolley import __version__

    if not value or ctx.resilient_parsing:
        return
    click.echo('version {}'.format(__version__))
    ctx.exit()


# cli methods we are exposing to be used via terminal

@click.group()
@click_config.wrap(module=config, sections=('github', 'trello'))
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def cli():
    # assert config.buffer
    pass


@cli.command('bootstrap')
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
def cli_bootstrap(github_org, github_repo):
    """Sets up github with some sensible defaults."""
    delete_existing_github_labels(
        config,
        github_org or config.github.org,
        github_repo or config.github.repo)

    create_github_labels(
        config,
        github_org or config.github.org,
        github_repo or config.github.repo)

    create_github_issues(
        config,
        github_org or config.github.org,
        github_repo or config.github.repo)

    create_github_milestones(
        config,
        github_org or config.github.org,
        github_repo or config.github.repo)


@cli.command('close_existing_github_issues')
@click.option('--force/--no-force', default=False)
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
def cli_close_existing_github_issues(force, github_org, github_repo):
    """Close all existing GitHub issues."""
    message = 'Do you really want to close all of your existing GitHub issues?'
    if force or click.confirm(message):
        close_existing_github_issues(
            config,
            github_org or config.github.org,
            github_repo or config.github.repo)
    else:
        click.echo('Action aborted')


@cli.command('create_github_issues')
@click.option('--filename', default='etc/default_github_issues.csv')
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
def cli_create_github_issues(filename, github_org, github_repo):
    """Create GitHub issues from a CSV file."""
    create_github_issues(
        config,
        github_org or config.github.org,
        github_repo or config.github.repo,
        filename)


@cli.command('create_github_labels')
@click.option('--filename', default='etc/default_github_labels.csv')
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
def cli_create_github_labels(filename, github_org, github_repo):
    """Create GitHub labels from a CSV file."""
    create_github_labels(
        config,
        github_org or config.github.org,
        github_repo or config.github.repo,
        filename)


@cli.command('create_github_milestones')
@click.option('--filename', default='etc/default_github_milestones.csv')
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
def cli_create_github_milestones(filename, github_org, github_repo):
    """Create GitHub milestones from a CSV file."""
    create_github_milestones(
        config,
        github_org or config.github.org,
        github_repo or config.github.repo,
        filename)


@cli.command('create_trello_cards')
@click.option('--filename', default='etc/default_trello_cards.csv')
@click.option('--trello-board', type=str)
def cli_create_trello_cards(filename, trello_board):
    """Create Trello cards from a CSV file."""
    create_trello_cards(
        config,
        trello_board or config.trello.board_id,
        filename)


@cli.command('create_trello_labels')
@click.option('--filename', default='etc/default_trello_labels.csv')
@click.option('--trello-board', type=str)
def cli_create_trello_labels(filename, trello_board):
    """Create Trello labels from a CSV file."""
    create_trello_labels(
        config,
        trello_board or config.trello.board_id,
        filename)


@cli.command('create_trello_lists')
@click.option('--filename', default='etc/default_trello_lists.csv')
@click.option('--trello-board', type=str)
def cli_create_trello_lists(filename, trello_board):
    """Create Trello lists from a CSV file."""
    create_trello_lists(
        config,
        trello_board or config.trello.board_id,
        filename)


@cli.command('delete_existing_github_labels')
@click.option('--force/--no-force', default=False)
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
def cli_delete_existing_github_labels(force, github_org, github_repo):
    """Delete labels from GitHub repo."""
    message = 'Do you really want to delete all of the existing GitHub labels?'
    if force or click.confirm(message):
        delete_existing_github_labels(
            config,
            github_org or config.github.org,
            github_repo or config.github.repo)
    else:
        click.echo('Action aborted')


@cli.command('delete_existing_github_milestones')
@click.option('--force/--no-force', default=False)
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
def cli_delete_existing_github_milestones(force, github_org, github_repo):
    """Delete milestones from GitHub repo."""
    message = 'Do you really want to delete all of the existing GitHub milestones?'
    if force or click.confirm(message):
        delete_existing_github_milestones(
            config,
            github_org or config.github.org,
            github_repo or config.github.repo)
    else:
        click.echo('Action aborted')


@cli.command('sync_github_issues_to_trello_cards')
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
@click.option('--trello-board', type=str)
def cli_sync_github_issues_to_trello_cards(github_org, github_repo, trello_board):
    """Convert your GitHub issues to Trello cards."""
    sync_github_issues_to_trello_cards(
        config,
        github_org or config.github.org,
        github_repo or config.github.repo,
        trello_board or config.trello.board_id)


@cli.command('sync_trello_cards_to_github_issues')
@click.option('--trello-board', type=str)
@click.option('--github-org', type=str)
@click.option('--github-repo', type=str)
def cli_sync_trello_cards_to_github_issues(trello_board, github_org, github_repo):
    """Convert your Trello cards to GitHub issues."""
    sync_trello_cards_to_github_issues(
        config,
        trello_board or config.trello.board_id,
        github_org or config.github.org,
        github_repo or config.github.repo)


@cli.command('list_trello_boards')
def cli_list_trello_boards():
    """List your Trello boards."""

    list_trello_boards(config)


@cli.command('list_trello_cards')
@click.option('--trello-board', type=str)
def cli_list_trello_cards(trello_board):
    """List your Trello cards for a given board."""

    list_trello_cards(
        config,
        trello_board or config.trello.board_id)


@cli.command('list_trello_organizations')
def cli_list_trello_organizations():
    """List your Trello organizations."""

    list_trello_organizations(config)


@cli.command('test_buffer')
def cli_test_buffer():
    """Convert your Trello cards to GitHub issues."""

    try:
        test_buffer(config)
    except Exception as e:
        print e
