# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from . import run_command_test
from ...utils import utils


def test_get():
    run_command_test('ports', 'get', utils.random_string())


def test_get_accounts_using_port():
    run_command_test('ports', 'get-accounts-using-port', utils.random_string())


def test_update():
    run_command_test('ports', 'update', {'id': utils.random_string()})


def test_delete():
    run_command_test('ports', 'delete', utils.random_string())
