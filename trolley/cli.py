#!/usr/bin/env python
"""
Trolley syncs issues between CSV, Github, and Buffer with Trello.

"""

import click
# import click_config
import os
import sys

from dynaconf import LazySettings


DYNACONF_NAMESPACE = 'TROLLEY'

settings = LazySettings(
    DYNACONF_NAMESPACE=DYNACONF_NAMESPACE,
    ENVVAR_FOR_DYNACONF='TROLLEY_SETTINGS_MODULE',
)

settings.configure()


CONTEXT_SETTINGS = dict(auto_envvar_prefix='TROLLEY')


class Context(object):

    def __init__(self):
        self.home = os.getcwd()
        self.settings = settings
        self.verbose = False

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

    def list_commands(self, context):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, context, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('trolley.commands.cmd_' + name,
                             None, None, ['cli'])
            # if hasattr(mod, 'enabled'):
            #     print name, mod.enabled()
        except ImportError:
            return
        return mod.cli


def print_version(context, param, value):
    from trolley import __version__

    if not value or context.resilient_parsing:
        return
    click.echo('version {}'.format(__version__))
    context.exit()


@click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def cli():
    # context.verbose = verbose
    pass
