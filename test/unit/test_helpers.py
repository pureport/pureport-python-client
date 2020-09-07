# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import datetime

import pytest

from pureport_client import helpers

from ..utils import utils


def test_format_date_string():
    for item in ('2020/01/01', '2020-01-01', '2020.01.01', '2020,01,01',
                 '2020-01-01T00', '2020-01-01T00:00', '2020-01-01T00:00:00'):
        helpers.format_date(item)


def test_format_date_string_invalid():
    with pytest.raises(ValueError):
        helpers.format_date(utils.random_string())


def test_format_date_date():
    helpers.format_date(datetime.date.today())
