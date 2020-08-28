# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from . import run_command_test
from ...utils import utils


def test_get():
    run_command_test('gateways', 'get', utils.random_string())


def test_get_bgp_routes():
    run_command_test('gateways', 'get-bgp-routes', utils.random_string())


def test_get_connectivity_over_time():
    run_command_test('gateways', 'get-connectivity-over-time',
                     utils.random_string(), {'gt': utils.random_string()})


def test_get_latest_connectivity():
    run_command_test('gateways', 'get-latest-connectivity', utils.random_string())


def test_get_tasks():
    run_command_test('gateways', 'get-tasks', utils.random_string())


def test_create_task():
    run_command_test('gateways', 'create-task', utils.random_string(), {})
