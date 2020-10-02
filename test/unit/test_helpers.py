# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import datetime
import os
import json
import pytest
from unittest.mock import patch, Mock

from pureport_client import helpers
from pureport import models
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


def test_format_output_json():
    output = helpers.format_output([], 'json')
    assert output == '[]'


def make_models(models, mock_get_api):
    basepath = os.path.dirname(__file__)
    content = json.loads(
        open(os.path.join(basepath, '../openapi.json')).read()
    )
    mock_get_api.return_value = content
    session = Mock()
    models.make(session)


@patch.object(models, 'get_api')
def test_format_output_columns(mock_get_api):
    make_models(models, mock_get_api)

    response = [models.Network(id='id', name='name', state='ACTIVE')]
    output = helpers.format_output(response, 'column')
    title_row = 'ID' + (33 * ' ') + 'NAME' + (21 * ' ') + 'STATE' + (20 * ' ') + 'TAGS\n'
    second_row = 'id' + (33 * ' ') + 'name' + (21 * ' ') + 'ACTIVE' + (19 * ' ') + 'No Tags\n'
    assert output == (title_row + second_row)


@patch.object(models, 'get_api')
def test_format_output_json_with_model(mock_get_api):
    make_models(models, mock_get_api)
    response = [models.Network(id='id', name='name', state='ACTIVE')]
    output = helpers.format_output(response, 'json')
    assert json.loads(output) == [{"id": "id", "name": "name", "state": "ACTIVE"}]


@patch.object(models, 'get_api')
def test_format_output_column_fallback(mock_get_api):
    make_models(models, mock_get_api)
    response = [{'id': 'id'}]
    output = helpers.format_output(response, 'column')
    assert output == '[\n  {\n    "id": "id"\n  }\n]'


@patch.object(models, 'get_api')
def test_format_output_yaml(mock_get_api):
    make_models(models, mock_get_api)
    response = [{'id': 'id'}]
    output = helpers.format_output(response, 'yaml')
    assert output == '- id: id\n'
