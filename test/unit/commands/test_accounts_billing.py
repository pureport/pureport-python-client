# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import os

from . import run_command_test
from ...utils import utils

os.environ['PUREPORT_ACCOUNT_ID'] = utils.random_string()


def test_get():
    run_command_test('accounts billing', 'get')


def test_get_configured():
    run_command_test('accounts billing', 'get-configured')


def test_create():
    run_command_test('accounts billing', 'create', {})


def test_update():
    run_command_test('accounts billing', 'update', {})


def test_delete():
    run_command_test('accounts billing', 'delete')
