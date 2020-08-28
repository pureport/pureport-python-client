# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import os

from . import run_command_test
from ...utils import utils

os.environ['PUREPORT_ACCOUNT_ID'] = utils.random_string()


def test_list():
    run_command_test('accounts invites', 'list')


def test_get():
    run_command_test('accounts invites', 'get', utils.random_string())


def test_create():
    run_command_test('accounts invites', 'create', {'id': utils.random_string()})


def test_update():
    run_command_test('accounts invites', 'update', {'id': utils.random_string()})


def test_delete():
    run_command_test('accounts invites', 'delete', utils.random_string())
