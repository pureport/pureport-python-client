# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import os
import json
import shlex
import importlib

from re import compile, sub
from unittest.mock import MagicMock
from collections import namedtuple
from functools import partial


from click import group, pass_context, version_option
from click.testing import CliRunner

from pureport_client import __main__ as main


path = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, 'openapi.json')
open_api = json.loads(open(path).read())

urls = {}

for path, path_obj in open_api['paths'].items():
    url = compile('^' + sub(r'{[^}]+}', '([^/]+)', path) + '$')
    for method in path_obj:
        if url not in urls:
            urls[url] = list()
        urls[url].append(method.upper())


def create_mock_cli(pureport_client):
    """
    This creates a mock CLI using a mock client.
    :param Client pureport_client:
    :rtype: click.Command
    """
    @group(context_settings={'auto_envvar_prefix': 'PUREPORT'})
    @version_option()
    @pass_context
    def cli(ctx):
        """
        \f
        :param click.Context ctx:
        """
        ctx.obj = pureport_client

    main.make(cli)

    return cli


Response = namedtuple('Response', ('status', 'data', 'headers', 'json'))
response = partial(Response, status=200, data=None, headers=None, json=json.dumps({}))


def request(*args, **kwargs):
    for url in urls:
        match = url.match(args[0])
        if match:
            break
    else:
        raise AssertionError(args[0])
    return response()


def return_object(query=None):
    return []


client = MagicMock()
client.get.side_effect = request
client.post.side_effect = request
client.put.side_effect = request
client.delete.side_effect = request
# all client functions
client.find_networks.side_effect = return_object
client.find_all_accounts.side_effect = return_object
client.find_all_roles.side_effect = return_object
client.find_api_keys.side_effect = return_object
client.get_api_key.side_effect = return_object
client.find_connections.side_effect = return_object
client.get_connections.side_effect = return_object
client.find_account_invites.side_effect = return_object
client.find_ports.side_effect = return_object
client.find_all_roles.side_effect = return_object
client.get_account_supported_connections.side_effect = return_object
client.get_cloud_regions.side_effect = return_object
client.get_cloud_region.side_effect = return_object
client.get_cloud_services.side_effect = return_object
client.find_facilities.side_effect = return_object
client.get_facility.side_effect = return_object
client.find_locations.side_effect = return_object
client.get_locations.side_effect = return_object
client.get_location.side_effect = return_object
client.get_supported_ports.side_effect = return_object
client.get_cloud_service.side_effect = return_object
client.get_account_invite.side_effect = return_object
client.get_supported_connection.side_effect = return_object

runner = CliRunner()
cli = create_mock_cli(client)


def run_command_test(parent, child, *args, **kwargs):
    command = shlex.split(parent)

    cli_options = kwargs.pop('cli_options', None)
    cli_options_post = kwargs.pop('cli_options_post', None)

    if cli_options:
        command.extend(shlex.split(cli_options))

    command.append(child)

    if cli_options_post:
        command.extend(shlex.split(cli_options_post))

    for a in args:
        if isinstance(a, dict):
            command.append(json.dumps(a))
        else:
            command.append(str(a))

    result = runner.invoke(cli, args=command)
    assert result.exit_code == 0, result.output

    module = '.'.join(shlex.split(parent)).replace('-', '_')
    pkg = '.'.join(('pureport_client.commands', module))

    mod = importlib.import_module(pkg)

    if pkg.split('.')[-2] in ('accounts', 'networks'):
        obj = mod.Command(client, None)
    else:
        obj = mod.Command(client)

    child = child.replace('-', '_')
    response = getattr(obj, child)(*args, **kwargs)

    return (result, response)
