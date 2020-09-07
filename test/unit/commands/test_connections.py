# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved


from __future__ import absolute_import

from . import run_command_test
from ...utils import utils


def test_get():
    run_command_test('connections', 'get', utils.random_string())


def test_update():
    run_command_test('connections', 'update', {'id': utils.random_string()})


# FIXME currently the run_command_test doesn't provide a way to control the
# response from the mocked object.  need to update the run_command_test
# function to include this option
# def test_update_wait():
#     run_command_test('connections', 'update', {'id': utils.random_string()},
#                      cli_options_post="-w")


def test_delete():
    run_command_test('connections', 'delete', utils.random_string())


def test_get_tasks():
    run_command_test('connections', 'get-tasks', utils.random_string())


def test_create_task():
    run_command_test('connections', 'create-task', utils.random_string(),
                     {'id': utils.random_string()})
