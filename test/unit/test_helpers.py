# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import datetime

import pytest

from pureport_client import helpers
from pureport import models

from ..utils import utils


def setup():
    models.make()


def test_format_date_string():
    for item in ('2020/01/01', '2020-01-01', '2020.01.01', '2020,01,01',
                 '2020-01-01T00', '2020-01-01T00:00', '2020-01-01T00:00:00'):
        helpers.format_date(item)


def test_format_date_string_invalid():
    with pytest.raises(ValueError):
        helpers.format_date(utils.random_string())


def test_format_date_date():
    helpers.format_date(datetime.date.today())


def test_format_output_json():
    output = helpers.format_output([], 'json')
    assert output == '[]'


def test_format_output_columns():
    response = [models.Network(id='id', name='name', state='ACTIVE')]
    output = helpers.format_output(response, 'column')
    title_row = 'ID' + (33 * ' ') + 'NAME' + (21 * ' ') + 'STATE' + (20 * ' ') + 'TAGS\n'
    second_row = 'id' + (33 * ' ') + 'name' + (21 * ' ') + 'ACTIVE' + (19 * ' ') + 'No Tags\n'
    assert output == (title_row + second_row)


def test_format_output_json_with_model():
    response = [models.Network(id='id', name='name', state='ACTIVE')]
    output = helpers.format_output(response, 'json')
    assert output == '[{"id": "id", "name": "name", "state": "ACTIVE"}]'


def test_format_output_column_fallback():
    response = [{'id': 'id'}]
    output = helpers.format_output(response, 'column')
    assert output == '[\n  {\n    "id": "id"\n  }\n]'


def test_format_output_yaml():
    response = [{'id': 'id'}]
    output = helpers.format_output(response, 'yaml')
    assert output == '- id: id\n'
