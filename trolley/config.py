import ConfigParser
import os
import sys


BUFFER_CLIENT_ID = os.environ.get('BUFFER_CLIENT_ID')
BUFFER_CLIENT_SECRET = os.environ.get('BUFFER_CLIENT_SECRET')
BUFFER_ACCESS_TOKEN = os.environ.get('BUFFER_ACCESS_TOKEN')

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

CONFIG_FILE = os.path.expanduser('~/.config/trolley/trolley.ini')
config_parser = ConfigParser.ConfigParser()


# might migrate to:
#   http://click.pocoo.org/4/options/#values-from-environment-variables
class config(object):

    class buffer(object):
        client_id = BUFFER_CLIENT_ID
        client_secret = BUFFER_CLIENT_SECRET
        access_token = BUFFER_ACCESS_TOKEN

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


def commit_changes():
    '''
    Write changes to the config file.
    '''
    with open(CONFIG_FILE, 'w') as configfile:
        config_parser.write(configfile)


def create_config():
    if os.path.exists(CONFIG_FILE):
        pass
    else:
        os.makedirs(os.path.dirname(CONFIG_FILE))
        open(CONFIG_FILE, 'w').close()
        config_parser.add_section('buffer')
        config_parser.set('buffer', 'client_id', '')
        config_parser.set('buffer', 'client_secret', '')
        config_parser.set('buffer', 'access_token', '')

        config_parser.add_section('github')
        config_parser.set('github', 'username', '')
        config_parser.set('github', 'password', '')
        config_parser.set('github', 'org', '')
        config_parser.set('github', 'repo', '')

        config_parser.add_section('trello')
        config_parser.set('trello', 'app_key', '')
        config_parser.set('trello', 'app_secret', '')
        config_parser.set('trello', 'auth_token', '')
        config_parser.set('trello', 'board_id', '')
        config_parser.set('trello', 'default_list', 'Uncategorized')

        return config_parser
