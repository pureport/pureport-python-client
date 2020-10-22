# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import os
from unittest.mock import patch

from . import run_command_test
from ...utils import utils
from ..test_helpers import make_models
from pureport import models

os.environ['PUREPORT_ACCOUNT_ID'] = utils.random_string()


def test_list():
    run_command_test('accounts networks', 'list')


@patch.object(models, 'get_api')
def test_create(mock_get_api):
    make_models(models, mock_get_api)
    run_command_test('accounts networks', 'create', {'name': utils.random_string()})
