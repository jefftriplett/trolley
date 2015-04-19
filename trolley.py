#!/usr/bin/env python
"""
Trolley syncs issues from CSVs to Github and to sync projects between
Github and Trello.
"""

import csv
import os
import random

import click
import click_config
import github3

from trello import TrelloApi


__author__ = 'Jeff Triplett'
__copyright__ = 'Copyright 2015, Jeff Triplett'
__license__ = 'BSD'
__version_info__ = (0, 0, 1)
__version__ = '.'.join(map(str, __version_info__))


# hold auth state
_github_auth = None
_trello_auth = None

GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
GITHUB_PASSWORD = os.environ.get('GITHUB_PASSWORD')
GITHUB_ORG = os.environ.get('GITHUB_ORG')
GITHUB_REPO = os.environ.get('GITHUB_REPO')
GITHUB_SCOPES = ['user', 'repo']

TRELLO_APP_KEY = os.environ.get('TRELLO_APP_KEY')
TRELLO_APP_SECRET = os.environ.get('TRELLO_APP_SECRET')
TRELLO_AUTH_TOKEN = os.environ.get('TRELLO_AUTH_TOKEN')
TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
TRELLO_DEFAULT_LIST = os.environ.get('TRELLO_DEFAULT_LIST', 'Uncategorized')


# might migrate to:
#   http://click.pocoo.org/4/options/#values-from-environment-variables
class config(object):

    class github(object):
        username = GITHUB_USERNAME
        password = GITHUB_PASSWORD
        org = GITHUB_ORG
        repo = GITHUB_REPO

    class trello(object):
        app_key = TRELLO_APP_KEY
        app_secret = TRELLO_APP_SECRET
        auth_token = TRELLO_AUTH_TOKEN
        board_id = TRELLO_BOARD_ID
        default_list = TRELLO_DEFAULT_LIST


# utils

def get_random_color():
    filename = 'etc/color-blind-safe.csv'
    with open(filename) as f:
        colors = list(csv.DictReader(f))

    index = random.randint(0, len(colors))
    return colors[index]['color']


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('version {}'.format(__version__))
    ctx.exit()


# github utils

def get_github_auth(github_config):
    """Log me into github and return an object."""
    global _github_auth

    if _github_auth:
        return _github_auth

    _github_auth = github3.login(github_config.username, github_config.password)
    return _github_auth


def get_github_repository(config, github_org, github_repo):
    """Return a repository object and log me in."""
    github = get_github_auth(config.github)
    repository = github.repository(github_org, github_repo)
    return repository


def get_existing_github_issues(config, github_org, github_repo):
    repository = get_github_repository(config, github_org, github_repo)
    existing_issues = [str(item.title) for item in repository.iter_issues()]
    return existing_issues


def get_existing_github_labels(config, github_org, github_repo):
    repository = get_github_repository(config, github_org, github_repo)
    existing_labels = [str(item.name) for item in repository.iter_labels()]
    return existing_labels


def get_existing_github_milestones(config, github_org, github_repo):
    repository = get_github_repository(config, github_org, github_repo)
    existing_milestones = [str(item.title) for item in repository.iter_milestones()]
    return existing_milestones


# github core

def close_existing_github_issues(config, github_org, github_repo):
    repository = get_github_repository(config, github_org, github_repo)
    issues = [str(issue.title) for issue in repository.iter_issues()]

    click.echo('closing {} issues'.format(len(issues)))
    for issue in repository.iter_issues():
        click.echo('closing issue "{}"'.format(issue.title))
        issue.close()


def create_github_issues(config, github_org, github_repo,
                         filename='etc/default_issues.csv'):
    with open(filename) as f:
        issues = list(csv.DictReader(f))

    repository = get_github_repository(config, github_org, github_repo)
    existing_issues = get_existing_github_issues(config, github_org, github_repo)

    click.echo('creating {} issues'.format(len(issues)))
    for issue in issues:
        title = str(issue['title'])
        body = str(issue['body'])
        labels = issue['labels']

        if labels:
            if ',' in labels:
                labels = labels.split(',')
            else:
                labels = [labels]

        if title not in existing_issues:
            click.echo('creating issue "{}"'.format(title))
            repository.create_issue(title, body, labels=labels)
        else:
            click.echo('issue "{}" already exists'.format(title))


def create_github_labels(config, github_org, github_repo,
                         filename='etc/default_labels.csv'):
    with open(filename) as f:
        labels = list(csv.DictReader(f))

    repository = get_github_repository(config, github_org, github_repo)
    existing_labels = get_existing_github_labels(config, github_org, github_repo)

    click.echo('creating {} labels'.format(len(labels)))
    for label in labels:
        name = str(label['name'])
        color = str(label['color'])
        if name not in existing_labels:
            click.echo('creating label "{}"'.format(name))
            if not len(color):
                color = get_random_color()
            repository.create_label(name, color)
        else:
            click.echo('label "{}" already exists'.format(name))


def create_github_milestones(config, github_org, github_repo,
                             filename='etc/default_milestones.csv'):
    with open(filename) as f:
        milestones = list(csv.DictReader(f))

    repository = get_github_repository(config, github_org, github_repo)
    existing_milestones = get_existing_github_milestones(config, github_org, github_repo)

    click.echo('creating {} milestones'.format(len(milestones)))
    for milestone in milestones:
        title = str(milestone['title'])
        if title not in existing_milestones:
            click.echo('creating milestone "{}"'.format(title))
            repository.create_milestone(title)
        else:
            click.echo('milestone "{}" already exists'.format(title))


def delete_existing_github_labels(config, github_org, github_repo):
    repository = get_github_repository(config, github_org, github_repo)

    labels = [str(label.name) for label in repository.iter_labels()]

    click.echo('removing {} labels'.format(len(labels)))
    for label in labels:
        click.echo('removing label "{}"'.format(label))
        repository.label(label).delete()


def delete_existing_github_milestones(config, github_org, github_repo):
    repository = get_github_repository(config, github_org, github_repo)
    milestones = repository.iter_milestones(github_org, github_repo)

    click.echo('removing {} milestones'.format(len(list(milestones))))
    for milestone in milestones:
        click.echo('removing milestone "{}"'.format(milestone.title))
        milestone.delete()


# trello utils

def get_trello_auth(trello_config):
    """Log me into trello and return an object."""
    global _trello_auth

    if _trello_auth:
        return _trello_auth

    _trello_auth = TrelloApi(trello_config.app_key,
                             token=trello_config.auth_token)
    return _trello_auth


def get_existing_trello_boards(config, trello_board_id):
    trello = get_trello_auth(config.trello)
    boards = trello.boards.get_list(trello_board_id)
    boards = [str(board['name']) for board in boards]
    return boards


def get_existing_trello_cards(config, trello_board_id):
    trello = get_trello_auth(config.trello)
    cards = trello.boards.get_card(trello_board_id)
    cards = [str(card['name']) for card in cards]
    return cards


def get_existing_trello_labels(config, trello_board_id):
    trello = get_trello_auth(config.trello)
    labels = []
    return labels


def get_trello_board_lookup(config, trello_board_id):
    trello = get_trello_auth(config.trello)
    boards = trello.boards.get_list(trello_board_id)
    list_lookup = {}
    for board in boards:
        id = board['id']
        name = board['name']
        click.secho('{} - {}'.format(id, name), fg='blue')
        list_lookup[name] = id
        list_lookup[id] = name

    default_list = config.trello.default_list
    if default_list not in list_lookup:
        new_list = trello.boards.new_list(trello_board_id, default_list)
        new_list_id = new_list['id']
        list_lookup[default_list] = new_list_id
        list_lookup[new_list_id] = default_list

    return list_lookup


# trello core

def sync_github_to_trello_issues(config, github_org, github_repo,
                                 trello_board_id):
    trello = get_trello_auth(config.trello)
    board_lookup = get_trello_board_lookup(config, trello_board_id)
    existing_trello_cards = get_existing_trello_cards(config, trello_board_id)
    repository = get_github_repository(config, github_org, github_repo)
    issues = repository.iter_issues()

    #click.echo('creating {} issues'.format(issues.count))
    for issue in issues:
        title = issue.title
        desc = issue.body
        category = board_lookup[config.trello.default_list]
        if title not in existing_trello_cards:
            click.echo('creating issue "{}"'.format(title))
            trello.cards.new(title, category, desc=desc)
        else:
            click.echo('issue "{}" already exists'.format(title))


def sync_trello_to_github_issues(config, trello_board_id, github_org, github_repo):
    trello = get_trello_auth(config.trello)
    existing_github_issues = get_existing_github_issues(config, github_org, github_repo)
    repository = get_github_repository(config, github_org, github_repo)
    cards = trello.boards.get_card(config.trello.board_id)

    click.echo('creating {} cards'.format(len(cards)))
    for card in cards:
        name = card['name']
        #id = card['id']
        #list_id = card['idList']
        description = card['desc']  # boolean...
        labels = []

        if name not in existing_github_issues:
            click.echo('creating card "{}"'.format(name))
            repository.create_issue(name, description, labels=labels)

        else:
            click.echo('card "{}" already exists'.format(name))


# cli methods we are exposing to be used via terminal

@click.group()
@click_config.wrap(module=config, sections=('github', 'trello'))
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def cli():
    pass


@cli.command('bootstrap')
def cli_bootstrap():
    """Sets up github with some sensible defaults."""
    delete_existing_github_labels(
        config,
        config.github.org,
        config.github.repo)

    create_github_labels(
        config,
        config.github.org,
        config.github.repo)

    create_github_issues(
        config,
        config.github.org,
        config.github.repo)

    create_github_milestones(
        config,
        config.github.org,
        config.github.repo)


@cli.command('close_existing_github_issues')
@click.option('--force/--no-force', default=False)
def cli_close_existing_github_issues(force):
    message = 'Do you really want to close all of your existing GitHub issues?'
    if force or click.confirm(message):
        close_existing_github_issues(
            config,
            config.github.org,
            config.github.repo)
    else:
        click.echo('Action aborted')


@cli.command('create_github_issues')
@click.option('--filename', default='etc/default_issues.csv')
def cli_create_github_issues(filename):
    create_github_issues(
        config,
        config.github.org,
        config.github.repo,
        filename)


@cli.command('create_github_labels')
@click.option('--filename', default='etc/default_labels.csv')
def cli_create_github_labels(filename):
    create_github_labels(
        config,
        config.github.org,
        config.github.repo,
        filename)


@cli.command('create_github_milestones')
@click.option('--filename', default='etc/default_milestones.csv')
def cli_create_github_milestones(filename):
    create_github_milestones(
        config,
        config.github.org,
        config.github.repo,
        filename)


@cli.command('delete_existing_github_labels')
@click.option('--force/--no-force', default=False)
def cli_delete_existing_github_labels(force):
    message = 'Do you really want to delete all of the existing GitHub labels?'
    if force or click.confirm(message):
        delete_existing_github_labels(
            config,
            config.github.org,
            config.github.repo)
    else:
        click.echo('Action aborted')


@cli.command('delete_existing_github_milestones')
@click.option('--force/--no-force', default=False)
def cli_delete_existing_github_milestones(force):
    message = 'Do you really want to delete all of the existing GitHub milestones?'
    if force or click.confirm(message):
        delete_existing_github_milestones(
            config,
            config.github.org,
            config.github.repo)
    else:
        click.echo('Action aborted')


@cli.command('sync_github_to_trello_issues')
def cli_sync_github_to_trello_issues():
    sync_github_to_trello_issues(
        config,
        config.github.org,
        config.github.repo,
        config.trello.board_id)


@cli.command('sync_trello_to_github_issues')
def cli_sync_trello_to_github_issues():
    sync_trello_to_github_issues(
        config,
        config.trello.board_id,
        config.github.org,
        config.github.repo)


if __name__ == '__main__':
    cli()
