import click


force_options = click.option(
    '--force/--no-force',
    default=False,
)


github_org_options = click.option(
    '--github-org',
    type=str,
)

github_repo_options = click.option(
    '--github-repo',
    type=str,
)

trello_board_options = click.option(
    '--trello-board',
    type=str,
)
