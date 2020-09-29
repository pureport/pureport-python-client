# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import os
import json

from unittest.mock import patch, Mock

from pureport_client import column_printer
from pureport import models

title_row = 'ID' + (33 * ' ') + 'NAME' + (21 * ' ') + 'STATE' + (20 * ' ') + 'TAGS\n'


def __make_models__(models, mock_get_api):
    basepath = os.path.dirname(__file__)
    content = json.loads(
        open(os.path.join(basepath, '../openapi.json')).read()
    )
    mock_get_api.return_value = content
    session = Mock()
    models.make(session)


@patch.object(models, 'get_api')
def test_empty_list(mock_get_api):
    __make_models__(models, mock_get_api)
    printString = column_printer.print_networks([])
    assert printString == title_row


@patch.object(models, 'get_api')
def test_empty_tags(mock_get_api):
    __make_models__(models, mock_get_api)
    sampleNetwork = models.Network(id='sample_id', name='sample_name')
    sampleNetwork.state = 'ACTIVE'
    printString = column_printer.print_networks([sampleNetwork])
    second_row = 'sample_id' + (26 * ' ') + 'sample_name' + (14 * ' ') + 'ACTIVE' + (19 * ' ') + 'No Tags\n'
    assert printString == title_row + second_row


@patch.object(models, 'get_api')
def test_with_tags(mock_get_api):
    __make_models__(models, mock_get_api)
    tag = {'tagkey': 'tagValue'}
    sampleNetwork = models.Network(id='sample_id', name='sample_name')
    sampleNetwork.state = 'ACTIVE'
    sampleNetwork.tags = tag
    printString = column_printer.print_networks([sampleNetwork])
    second_row = 'sample_id' + (26 * ' ') + 'sample_name' + (14 * ' ') + 'ACTIVE' + (19 * ' ') + '{"tagkey": "tagValue"}\n'
    assert printString == title_row + second_row
