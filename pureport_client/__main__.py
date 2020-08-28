# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import os
import glob
import importlib

from click import (
    group,
    option,
    pass_context,
    version_option
)

from pureport_client.client import Client

from pureport_client.util import (
    construct_commands,
    find_client_commands
)


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
    :param click.Context ctx:
    :param str api_url:
    :param str api_key:
    :param str api_secret:
    :param str api_profile:
    :param str access_token:
    """
    ctx.obj = Client(base_url=api_url,
                     key=api_key,
                     secret=api_secret,
                     profile=api_profile,
                     access_token=access_token)


def make(cli):
    # XXX: this function will dynamically discover the command tree based on
    # introspecting the Command class in each module.  By design the class
    # introspection is not more than two levels deep.  This will need to be
    # modified in the future, if more than two command levels are required.

    commands = list()

    for item in glob.glob(os.path.join(os.path.dirname(__file__), 'commands/*')):
        if os.path.isdir(item):
            name = item.split('/')[-1]

            if not name.startswith('_'):
                kwargs = {}

                kwargs['name'] = name.replace('_', '-')

                pkg = "pureport_client.commands.{}".format(name)
                mod = importlib.import_module(pkg)
                kwargs['context'] = mod.Command

                kwargs['commands'] = list()

                for item in find_client_commands(mod.Command):
                    try:
                        sub = importlib.import_module(".".join((pkg, item.__name__)))
                        kwargs['commands'].append({
                            'name': item.__name__.replace('_', '-'),
                            'context': getattr(mod.Command, item.__name__),
                            'commands': find_client_commands(sub.Command)
                        })
                    except ImportError:
                        kwargs['commands'].append(item)

                commands.append(kwargs)

    for command in construct_commands(commands):
        cli.add_command(command)


def run():
    make(cli)
    cli()
