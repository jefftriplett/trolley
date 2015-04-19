# Trolley

Tools to help sync issues from CSVs to Github and to sync projects between Github and Trello.

Trolley is a useful tool for loading an initial set of issues, labels, and milestones on github.

Trolley was written to also help me manage a few projects where I need to selectively sync Issues and boards between Trello and Github.

## Installation

    pip install trolley

## Usage

### Example trolley.yml

    github:
        username: 'username'
        password: 'password'
        org: 'github'
        repo: 'gitignore'

    trello:
        app_key: 'get-this-from-trello'
        app_secret: 'get-this-from-trello'
        auth_token: 'get-this-from-trello'
        board_id: 'your-board-id-sha'
        default_list: 'Uncategorized'

### Usage

    trolley --conf trolley.yml --help

    trolley --conf trolley.yml create_github_issues

## Inspiration

This project shares ideas from the following projects:

- The CSV bits via: https://github.com/nprapps/app-template
