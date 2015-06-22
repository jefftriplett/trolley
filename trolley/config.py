import os


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
