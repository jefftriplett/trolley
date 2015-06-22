#!/usr/bin/env python
"""
Trolley syncs issues between CSV, Github, and Buffer with Trello.

"""

import click
import click_config
import os
import sys

from trolley.config import config


CONTEXT_SETTINGS = dict(auto_envvar_prefix='TROLLEY')


class Context(object):

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('trolley.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


def print_version(ctx, param, value):
    from trolley import __version__

    if not value or ctx.resilient_parsing:
        return
    click.echo('version {}'.format(__version__))
    ctx.exit()


@click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
@click_config.wrap(module=config, sections=('trello', 'github', 'buffer'))
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
# @pass_context
# def cli(ctx, verbose):
def cli(verbose):
    # assert config.buffer
    # ctx.verbose = verbose
    pass
