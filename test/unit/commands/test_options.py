# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from . import run_command_test


def test_list():
    run_command_test('options', 'list')
