# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import os

from . import run_command_test
from ...utils import utils

os.environ['PUREPORT_ACCOUNT_ID'] = utils.random_string()


def test_usage_by_connection():
    run_command_test('accounts metrics', 'usage-by-connection', {})


def test_usage_by_connection_and_time():
    run_command_test('accounts metrics', 'usage-by-connection-and-time', {})


def test_usage_by_network_and_time():
    run_command_test('accounts metrics', 'usage-by-network-and-time', {})
