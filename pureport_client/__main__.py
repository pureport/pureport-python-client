# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import os
import glob
import importlib
import logging

from pkg_resources import iter_entry_points

from click import (
    group,
    option,
    pass_context,
    version_option
)

from pureport.session import Session
from pureport.credentials import default

from pureport_client.util import (
    construct_commands,
    find_client_commands
)


log = logging.getLogger(__name__)


@group(context_settings={'auto_envvar_prefix': 'PUREPORT'})
@option('-u', '--api_url', help='The api url for this client.')
@option('-k', '--api_key', help='The API Key.')
@option('-s', '--api_secret', help='The API Key secret.')
@option('-p', '--api_profile', help='The API Profile if using file-based configuration.')
@option('-t', '--access_token', help='The API Key access token.')
@version_option()
@pass_context
def cli(ctx, api_url, api_key, api_secret, api_profile, access_token):
    """
    \f
    :param ctx: internal context instance
    :type ctx: `click.Context`

    :param api_url: base URL for Pureport REST API
    :type api_url: str

    :param api_key: Pureport API key to use
    :type api_key: str

    :param api_secret: Pureport API secret to use
    :type: api_secret: str

    :param api_profile: Pureport configuration profile to use
    :type api_profile: str

    :param access_token: Pureport API access token
    :type access_token: str

    :returns: None
    """
    # FIXME current Session class doesn't allow credentials to be passed in so
    # we work around it with environment variables
    if api_url:
        os.environ['PUREPORT_API_BASE_URL'] = api_url
    if api_key:
        os.environ['PUREPORT_API_KEY'] = api_key
    if api_secret:
        os.environ['PUREPORT_API_SECRET'] = api_secret

    ctx.obj = Session(*default())


def load(pkg):
    command = {'name': pkg.split('.')[-1].replace('_', '-')}
    module = importlib.import_module(pkg)

    command['context'] = module.Command
    command['commands'] = list()

    for item in find_client_commands(module.Command):
        try:
            mod = importlib.import_module(".".join((module.__package__, item.__name__)))
            command['commands'].append({
                'name': item.__name__.replace('_', '-'),
                'context': getattr(module.Command, item.__name__),
                'commands': find_client_commands(mod.Command)
            })
        except ImportError:
            command['commands'].append(item)

    return command


def find(path):
    for item in glob.glob(os.path.join(path, 'commands/*')):
        if os.path.isdir(item):
            if not os.path.basename(item).startswith('_'):
                yield item


def load_plugins():
    plugins = list()

    for item in iter_entry_points('pureport_client.plugins'):
        plugin = item.load()

        plugin_name = item.name.replace('_', '-')
        plugin_commands = list()

        for item in find(os.path.dirname(plugin.__file__)):
            pkg = ".".join((plugin.__package__, 'commands', os.path.basename(item)))
            log.debug("loading plugin package {}".format(pkg))
            plugin_commands.append(load(pkg))

        module = importlib.import_module('.'.join((plugin.__package__, 'commands')))

        plugins.append({'name': plugin_name,
                        'context': getattr(module, 'Command'),
                        'commands': plugin_commands})

    return plugins


def make(cli):
    """Create the Pureport commands tree

    Iterate over all of the commands defined in the `pureport.commands`
    module and add them to the CLI tree.  Each command must implement
    the `pureport.commands.CommandBase` object.

    :param cli: the instance of the cli
    :type cli: `click.core.Group`

    :returns: None
    """
    # XXX: this function will dynamically discover the command tree based on
    # introspecting the Command class in each module.  By design the class
    # introspection is not more than two levels deep.  This will need to be
    # modified in the future, if more than two command levels are required.

    commands = load_plugins()

    for item in find(os.path.dirname(__file__)):
        pkg = ".".join((__package__, 'commands', os.path.basename(item)))
        log.debug("loading core package {}".format(pkg))
        commands.append(load(pkg))

    for command in construct_commands(commands):
        cli.add_command(command)


def run():
    """Main entry point for the command line interface
    """
    make(cli)
    cli()
