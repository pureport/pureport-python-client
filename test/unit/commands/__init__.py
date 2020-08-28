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

from click import group, pass_context, version_option
from click.testing import CliRunner

from requests_mock import Adapter

from pureport_client import __main__ as main
from pureport_client.client import Client
from pureport_client.session import PureportSession


def __create_mock_client():
    """
    This creates a mock :class:`Client` instance.  It uses
    a real client to call out to the server for the OpenAPI data
    and constructs mock paths that can emulate the resources available
    on the server
    :rtype: Client
    """
    adapter = Adapter()

    # Loads all paths from OpenAPI as mock path matchers
    # The paths come in the form '/accounts/{account_id}', which we'll
    # instead convert to proper Regex path's /accounts/([^/]+)

    path = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, 'openapi.json')
    open_api = json.loads(open(path).read())

    for path, path_obj in open_api['paths'].items():
        url = compile('^mock://' + sub(r'{[^}]+}', '([^/]+)', path) + '$')
        for method, method_obj in path_obj.items():
            adapter.register_uri(method.upper(), url, json={})

    adapter.register_uri('POST',
                         'mock:///login',
                         json={
                             'access_token': '',
                             'refresh_token': '',
                             'expires_in': 2 ^ 31
                         })

    session = PureportSession(base_url='mock://')
    session.mount('mock', adapter)

    return Client(base_url='mock://', key='', secret='', session=session)


def __create_mock_cli(pureport_client):
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


client = __create_mock_client()
runner = CliRunner()
cli = __create_mock_cli(client)


def run_command_test(parent, child, *args, **kwargs):
    command = shlex.split(parent)
    cli_options = kwargs.pop('cli_options', None)

    if cli_options:
        command.extend(shlex.split(cli_options))

    command.append(child)

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
