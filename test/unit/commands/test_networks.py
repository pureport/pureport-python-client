# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from . import run_command_test
from ...utils import utils


def test_networks_get():
    run_command_test('networks', 'get', utils.random_string())


def test_networks_update():
    run_command_test('networks', 'update', {'id': utils.random_string()})


def test_networks_delete():
    run_command_test('networks', 'delete', utils.random_string())


def test_networks_connections_list():
    run_command_test('networks connections', 'list',
                     cli_options='-n {}'.format(utils.random_string()))


def test_networks_connections_create():
    run_command_test('networks connections', 'create', {},
                     cli_options='-n {}'.format(utils.random_string()))
