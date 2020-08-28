# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from . import run_command_test
from ...utils import utils


def test_list():
    run_command_test('locations', 'list')


def test_get():
    run_command_test('locations', 'get', utils.random_string())
