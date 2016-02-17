Trolley
=======

Trolley syncs issues from CSVs to Github and to sync projects between
Github and Trello.

Trolley is a useful tool for loading an initial set of issues, labels,
and milestones on github.

Trolley was written to also help me manage a few projects where I need
to selectively sync Issues and boards between Trello and Github.

.. figure:: http://upload.wikimedia.org/wikipedia/commons/a/a6/Fraum%C3%BCnster_-_Classic_Trolley_-_M%C3%BCnsterhof_2010-08-27_17-28-10.JPG
   :alt: 

By Roland zh (Own work) [CC BY-SA 3.0 (http://creativecommons.org/licenses/by-sa/3.0)], via Wikimedia Commons

Installation
------------

.. code-block:: bash

    $ pip install trolley

Usage
-----

Example trolley_settings.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    export TROLLEY_SETTINGS_MODULE='trolley_settings'

.. code-block:: python

    BUFFER_ACCESS_TOKEN = ''
    BUFFER_CLIENT_ID = ''
    BUFFER_CLIENT_SECRET = ''

    GITHUB_USERNAME = ''
    GITHUB_PASSWORD = ''
    GITHUB_ORG = ''
    GITHUB_REPO = ''

    TRELLO_APP_KEY = ''
    TRELLO_APP_SECRET = ''
    TRELLO_AUTH_TOKEN = ''
    TRELLO_BOARD_ID = ''
    TRELLO_DEFAULT_LIST = ''

Usage
~~~~~

.. code-block:: bash

    $ trolley --help

    $ trolley create_github_issues

Commands
~~~~~~~~

``bootstrap`` 
    Sets up github with some sensible defaults.

``close_existing_github_issues`` 
    Close all existing GitHub issues.

``create_github_issues`` 
    Create GitHub issues from a CSV file.

``create_github_labels`` 
    Create GitHub labels from a CSV file.

``create_github_milestones`` 
    Create GitHub milestones from a CSV file.

``create_trello_cards`` 
    Create Trello cards from a CSV file.

``create_trello_labels`` 
    Create Trello labels from a CSV file.

``create_trello_lists`` 
    Create Trello lists from a CSV file.

``delete_existing_github_labels``
    Delete labels from GitHub repo.

``delete_existing_github_milestones``
    Delete milestones from GitHub repo.

``list_trello_boards``
    List your Trello boards.

``list_trello_cards``
    List your Trello cards for a given board.

``list_trello_organizations``
    List your Trello organizations.

``sync_github_issues_to_trello_cards``
    Convert your GitHub issues to Trello cards.

``sync_trello_cards_to_github_issues``
    Convert your Trello cards to GitHub issues.

Object Overview
---------------

+---------------+---------------+---------+
| Github        | Trello        | Notes   |
+===============+===============+=========+
| Organization  | Organization  | ==      |
+---------------+---------------+---------+
| Repository    | Board         | ==      |
+---------------+---------------+---------+
|               | Lists         |         |
+---------------+---------------+---------+
| Issues        | Cards         | ==      |
+---------------+---------------+---------+
| Labels        | Labels        | ==      |
+---------------+---------------+---------+
| Milestones    |               |         |
+---------------+---------------+---------+

Milestones and Lists may be mapped together but they are fundamentally
treated very differently.

Future features
---------------

-  Needs allowed list / blocked list for handling via labels.
-  This is basically "works for me" but it needs error handling.

Inspiration
-----------

This project shares ideas from the following projects:

-  The CSV bits via: https://github.com/nprapps/app-template
