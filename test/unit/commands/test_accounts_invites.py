# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import os
from unittest.mock import patch

from . import run_command_test
from ...utils import utils
from pureport import models
from ..test_helpers import make_models

os.environ['PUREPORT_ACCOUNT_ID'] = utils.random_string()


def test_list():
    run_command_test('accounts invites', 'list')


def test_get():
    run_command_test('accounts invites', 'get', utils.random_string())


@patch.object(models, 'get_api')
def test_create(mock_get_api):
    make_models(models, mock_get_api)
    run_command_test('accounts invites', 'create', {'id': utils.random_string(),
                                                    'account': {'name': utils.random_string(), 'href': utils.random_string()},
                                                    'email': utils.random_string(),
                                                    'roles': [{'id': utils.random_string(), 'href': utils.random_string()}]})


@patch.object(models, 'get_api')
def test_update(mock_get_api):
    make_models(models, mock_get_api)
    run_command_test('accounts invites', 'create', {'id': utils.random_string(),
                                                    'account': {'name': utils.random_string(), 'href': utils.random_string()},
                                                    'email': utils.random_string(),
                                                    'roles': [{'id': utils.random_string(), 'href': utils.random_string()}]})


def test_delete():
    run_command_test('accounts invites', 'delete', utils.random_string())
