# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved
from unittest.mock import patch

from pureport_client import column_printer
from pureport import models
from .test_helpers import make_models

title_row = 'ID' + (33 * ' ') + 'NAME' + (21 * ' ') + 'STATE' + (20 * ' ') + 'TAGS\n'


@patch.object(models, 'get_api')
def test_empty_list(mock_get_api):
    make_models(models, mock_get_api)
    print_string = column_printer.print_networks([])
    assert print_string == title_row


@patch.object(models, 'get_api')
def test_empty_tags(mock_get_api):
    make_models(models, mock_get_api)
    sample_network = models.Network(id='sample_id', name='sample_name')
    sample_network.state = 'ACTIVE'
    print_string = column_printer.print_networks([sample_network])
    second_row = 'sample_id' + (26 * ' ') + 'sample_name' + (14 * ' ') + 'ACTIVE' + (19 * ' ') + 'No Tags\n'
    assert print_string == title_row + second_row


@patch.object(models, 'get_api')
def test_with_tags(mock_get_api):
    make_models(models, mock_get_api)
    tag = {'tagkey': 'tagValue'}
    sample_network = models.Network(id='sample_id', name='sample_name')
    sample_network.state = 'ACTIVE'
    sample_network.tags = tag
    print_string = column_printer.print_networks([sample_network])
    second_row = 'sample_id' + (26 * ' ') + 'sample_name' + (14 * ' ') + 'ACTIVE' + (19 * ' ') + '{"tagkey": "tagValue"}\n'
    assert print_string == title_row + second_row
