#!/usr/bin/env python
"""
Trolley syncs issues between CSV, Github, and Buffer with Trello.

"""

import csv
import datetime
import random

import click
import github3


# from buffpy.managers.updates import Updates
from buffpy.api import API as BufferAPI
from buffpy.managers.profiles import Profiles
from trello import TrelloClient


__author__ = 'Jeff Triplett'
__copyright__ = 'Copyright 2016, Jeff Triplett'
__license__ = 'BSD'
__version__ = '0.1.6'


# hold auth state
_buffer_auth = None
_github_auth = None
_trello_auth = None


# utils

def csv_to_dict_list(filename):
    """Open a CSV file and return a list of dict objects."""
    with open(filename) as f:
        values = list(csv.DictReader(f))
    return values


def get_random_color():
    filename = 'etc/color-blind-safe.csv'
    colors = csv_to_dict_list(filename)
    index = random.randint(0, len(colors))
    return colors[index]['color']


def print_version(context, param, value):
    if not value or context.resilient_parsing:
        return
    click.echo('version {}'.format(__version__))
    context.exit()


# github utils

def get_github_auth(settings):
    """Log me into github and return an object."""
    global _github_auth

    if _github_auth:
        return _github_auth

    assert settings.GITHUB_USERNAME
    assert settings.GITHUB_PASSWORD

    _github_auth = github3.login(
        settings.GITHUB_USERNAME,
        settings.GITHUB_PASSWORD)

    return _github_auth


def get_github_repository(settings, github_org, github_repo):
    """Return a repository object and log me in."""
    github = get_github_auth(settings)
    repository = github.repository(github_org, github_repo)
    return repository


def get_existing_github_issues(settings, github_org, github_repo):
    repository = get_github_repository(settings, github_org, github_repo)
    existing_issues = [item.title for item in repository.iter_issues()]
    return existing_issues


def get_existing_github_labels(settings, github_org, github_repo):
    repository = get_github_repository(settings, github_org, github_repo)
    existing_labels = [item.name for item in repository.iter_labels()]
    return existing_labels


def get_existing_github_milestones(settings, github_org, github_repo):
    repository = get_github_repository(settings, github_org, github_repo)
    existing_milestones = [item.title for item in repository.iter_milestones()]
    return existing_milestones


# github core

def close_existing_github_issues(settings, github_org, github_repo):
    repository = get_github_repository(settings, github_org, github_repo)
    issues = [issue.title for issue in repository.iter_issues()]

    click.echo('closing {} issues'.format(len(issues)))
    for issue in repository.iter_issues():
        click.echo(u'closing issue "{}"'.format(issue.title))
        issue.close()


def create_github_issues(settings, github_org, github_repo,
                         filename='etc/default_github_issues.csv'):
    issues = csv_to_dict_list(filename)
    repository = get_github_repository(settings, github_org, github_repo)
    existing_issues = get_existing_github_issues(settings, github_org, github_repo)

    click.echo('creating {} issues'.format(len(issues)))
    for issue in issues:
        title = issue['title']
        body = issue['body']
        labels = issue['labels']

        if labels:
            if ',' in labels:
                labels = labels.split(',')
            else:
                labels = [labels]
        else:
            labels = []

        if title not in existing_issues:
            click.echo(u'creating issue "{}"'.format(title))
            repository.create_issue(title, body, labels=labels)
        else:
            click.echo(u'issue "{}" already exists'.format(title))


def create_github_labels(settings, github_org, github_repo,
                         filename='etc/default_github_labels.csv'):
    labels = csv_to_dict_list(filename)
    repository = get_github_repository(settings, github_org, github_repo)
    existing_labels = get_existing_github_labels(settings, github_org, github_repo)

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


def create_github_milestones(settings, github_org, github_repo,
                             filename='etc/default_github_milestones.csv'):
    milestones = csv_to_dict_list(filename)
    repository = get_github_repository(settings, github_org, github_repo)
    existing_milestones = get_existing_github_milestones(settings, github_org, github_repo)

    click.echo('creating {} milestones'.format(len(milestones)))
    for milestone in milestones:
        title = str(milestone['title'])
        if title not in existing_milestones:
            click.echo('creating milestone "{}"'.format(title))
            repository.create_milestone(title)
        else:
            click.echo('milestone "{}" already exists'.format(title))


def delete_existing_github_labels(settings, github_org, github_repo):
    repository = get_github_repository(settings, github_org, github_repo)

    labels = [str(label.name) for label in repository.iter_labels()]

    click.echo('removing {} labels'.format(len(labels)))
    for label in labels:
        click.echo('removing label "{}"'.format(label))
        repository.label(label).delete()


def delete_existing_github_milestones(settings, github_org, github_repo):
    repository = get_github_repository(settings, github_org, github_repo)
    milestones = repository.iter_milestones(github_org, github_repo)

    click.echo('removing {} milestones'.format(len(list(milestones))))
    for milestone in milestones:
        click.echo('removing milestone "{}"'.format(milestone.title))
        milestone.delete()


# trello utils

def get_trello_auth(settings):
    """Log me into trello and return an object."""
    global _trello_auth

    if _trello_auth:
        return _trello_auth

    assert settings.TRELLO_APP_KEY
    assert settings.TRELLO_APP_SECRET
    assert settings.TRELLO_AUTH_TOKEN

    _trello_auth = TrelloClient(
        api_key=settings.TRELLO_APP_KEY,
        api_secret=settings.TRELLO_APP_SECRET,
        token=settings.TRELLO_AUTH_TOKEN,
        # token_secret=str(trello_config.auth_token),
    )
    return _trello_auth


def get_existing_trello_boards(settings, trello_board_id):
    trello = get_trello_auth(settings)
    board = trello.get_board(trello_board_id)
    boards = [str(board.name) for board in board.get_cards()]
    return boards


def get_existing_trello_cards(settings, trello_board_id):
    trello = get_trello_auth(settings)
    board = trello.get_board(trello_board_id)
    cards = board.get_cards()
    cards = [str(card.name) for card in cards]
    return cards


def get_existing_trello_labels(settings, trello_board_id):
    trello = get_trello_auth(settings)
    board = trello.get_board(trello_board_id)
    labels = board.get_labels()
    labels = [label for label in labels]
    return labels


def get_existing_trello_lists(settings, trello_board_id):
    trello = get_trello_auth(settings)
    board = trello.get_board(trello_board_id)
    all_lists = board.all_lists()
    all_lists = [item.name for item in all_lists]
    return all_lists


def get_trello_list_lookup(settings, trello_board_id):
    trello = get_trello_auth(settings)
    board = trello.get_board(trello_board_id)
    all_lists = board.all_lists()
    list_lookup = {}
    for item in all_lists:
        id = item.id
        name = item.name
        list_lookup[name] = id
        list_lookup[id] = name

    default_list = settings.TRELLO_DEFAULT_LIST
    if default_list not in list_lookup:
        new_list = board.add_list(default_list)
        new_list_id = new_list.id
        list_lookup[default_list] = new_list_id
        list_lookup[new_list_id] = default_list

    return list_lookup


# trello core

def create_trello_cards(settings, trello_board_id,
                        filename='etc/default_trello_cards.csv'):
    cards = csv_to_dict_list(filename)
    trello = get_trello_auth(settings)
    existing_cards = get_existing_trello_cards(settings, trello_board_id)
    board_lookup = get_trello_list_lookup(settings, trello_board_id)
    category = board_lookup[settings.TRELLO_DEFAULT_LIST]
    board = trello.get_board(trello_board_id)

    click.echo('creating {} cards'.format(len(cards)))

    for card in cards:
        name = str(card.get('title', ''))
        description = str(card.get('body', ''))
        labels = card.get('labels', [])

        if labels:
            if ',' in labels:
                labels = labels.split(',')
            else:
                labels = [labels]

        if name not in existing_cards:
            click.echo('creating issue "{}"'.format(name))
            list_item = board.get_list(category)
            new_card = list_item.add_card(name, description, labels=labels)

            '''
            # currently labels are broken in the trello python client :/
            if len(labels):
                for label in labels:
                    trello.cards.new_label(new_card['id'], label)
            '''
        else:
            click.echo('issue "{}" already exists'.format(name))


def create_trello_labels(settings, trello_board_id,
                         filename='etc/default_trello_labels.csv'):
    labels = csv_to_dict_list(filename)
    existing_labels = get_existing_trello_labels(settings, trello_board_id)

    click.echo('creating {} labels'.format(len(labels)))
    for label in labels:
        name = str(label['name'])
        color = str(label['color'])
        if name not in existing_labels:
            click.echo('creating label "{}"'.format(name))
            if not len(color):
                color = get_random_color()
            # TODO: Create Trello label via API
            #repository.create_label(name, color)
        else:
            click.echo('label "{}" already exists'.format(name))


def create_trello_lists(settings, trello_board_id,
                        filename='etc/default_trello_lists.csv'):
    lists = csv_to_dict_list(filename)
    trello = get_trello_auth(settings)
    existing_lists = get_existing_trello_lists(settings, trello_board_id)

    click.echo('creating {} lists'.format(len(lists)))

    for item in lists:
        title = str(item['title'])
        if title not in existing_lists:
            click.echo('creating list "{}"'.format(title))
            trello.boards.new_list(trello_board_id, title)
        else:
            click.echo('list "{}" already exists'.format(title))


def list_trello_boards(settings):

    print settings.keys()

    trello = get_trello_auth(settings)
    boards = trello.list_boards()
    for board in boards:
        click.echo('{0}: {1}{2}'.format(
            board.id,
            board.name,
            ' (closed)' if board.closed else ''
        ))


def list_trello_organizations(settings):
    trello = get_trello_auth(settings)
    organizations = trello.list_organizations()
    for organization in organizations:
        click.echo('{0}: {1}'.format(
            organization.id,
            organization.name
        ))


# sync github and trello

def sync_github_issues_to_trello_cards(settings, github_org, github_repo,
                                       trello_board_id):
    trello = get_trello_auth(settings)
    board_lookup = get_trello_list_lookup(settings, trello_board_id)
    existing_trello_cards = get_existing_trello_cards(settings, trello_board_id)
    repository = get_github_repository(settings, github_org, github_repo)
    issues = repository.iter_issues()

    # click.echo('creating {} issues'.format(issues.count))

    for issue in issues:
        title = issue.title
        desc = issue.body
        category = board_lookup[settings.TRELLO_DEFAULT_LIST]
        if title not in existing_trello_cards:
            click.echo('creating issue "{}"'.format(title))
            trello.cards.new(title, category, desc=desc)
        else:
            click.echo('issue "{}" already exists'.format(title))


def sync_trello_cards_to_github_issues(settings, trello_board_id, github_org, github_repo):
    trello = get_trello_auth(settings)
    existing_github_issues = get_existing_github_issues(settings, github_org, github_repo)
    repository = get_github_repository(settings, github_org, github_repo)
    board = trello.get_board(trello_board_id)
    cards = board.all_cards()

    click.echo('creating {} cards'.format(len(cards)))
    for card in cards:
        name = card.name
        # id = card['id']
        # list_id = card['idList']
        description = card.description
        labels = card.labels

        if name not in existing_github_issues:
            click.echo('creating card "{}"'.format(name))
            repository.create_issue(name, description, labels=labels)

        else:
            click.echo('card "{}" already exists'.format(name))


def list_trello_cards(settings, trello_board_id):
    assert settings.TRELLO_BOARD_ID

    trello = get_trello_auth(settings)
    board = trello.get_board(settings.TRELLO_BOARD_ID)
    cards = [card for card in board.open_cards()]

    for card in cards:
        name = card.name
        card_id = card.id
        description = card.description
        click.echo('{0}: {1}'.format(card_id, name))
        if len(description):
            click.echo(description)


def get_buffer_auth(settings):
    """Log me into buffer and return an object."""
    global _buffer_auth

    if _buffer_auth:
        return _buffer_auth

    assert settings.BUFFER_CLIENT_ID
    assert settings.BUFFER_CLIENT_SECRET
    assert settings.BUFFER_ACCESS_TOKEN

    _buffer_auth = BufferAPI(
        client_id=settings.BUFFER_CLIENT_ID,
        client_secret=settings.BUFFER_CLIENT_SECRET,
        access_token=settings.BUFFER_ACCESS_TOKEN,
    )

    return _buffer_auth


def test_buffer(settings):
    client = get_buffer_auth(settings)

    profiles = Profiles(api=client).filter(service='twitter')
    if not len(profiles):
        raise Exception('Your twitter account is not configured')

    profile = profiles[0]
    print profile
    print
    pending = profile.updates.pending
    for item in pending:
        print item
        print item.id
        print item.text
        print item.scheduled_at
        print datetime.datetime.fromtimestamp(item.scheduled_at)
