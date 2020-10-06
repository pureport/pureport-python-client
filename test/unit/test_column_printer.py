# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved
from unittest.mock import patch

from pureport_client import column_printer
from pureport import models
from .test_helpers import make_models

title_row_network = 'ID' + (33 * ' ') + 'NAME' + (21 * ' ') + 'STATE' + (20 * ' ') + 'TAGS\n'
title_row_account = 'ID' + (33 * ' ') + 'NAME\n'


@patch.object(models, 'get_api')
def test_empty_list(mock_get_api):
    make_models(models, mock_get_api)
    print_string = column_printer.print_columns([], 'Network')
    assert print_string == title_row_network


@patch.object(models, 'get_api')
def test_empty_tags(mock_get_api):
    make_models(models, mock_get_api)
    sample_network = models.Network(id='sample_id', name='sample_name')
    sample_network.state = 'ACTIVE'
    print_string = column_printer.print_columns([sample_network], 'Network')
    second_row = 'sample_id' + (26 * ' ') + 'sample_name' + (14 * ' ') + 'ACTIVE' + (19 * ' ') + '\n'
    assert print_string == title_row_network + second_row


@patch.object(models, 'get_api')
def test_with_tags(mock_get_api):
    make_models(models, mock_get_api)
    tag = {'tagkey': 'tagValue'}
    sample_network = models.Network(id='sample_id', name='sample_name')
    sample_network.state = 'ACTIVE'
    sample_network.tags = tag
    print_string = column_printer.print_columns([sample_network], 'Network')
    second_row = 'sample_id' + (26 * ' ') + 'sample_name' + (14 * ' ') + 'ACTIVE' + (19 * ' ') + '{"tagkey": "tagValue"}\n'
    assert print_string == title_row_network + second_row


@patch.object(models, 'get_api')
def test_account(mock_get_api):
    make_models(models, mock_get_api)
    sample_account = models.Account(id='sample_id', name='sample_name')
    print_string = column_printer.print_columns([sample_account], 'Account')
    second_row = 'sample_id' + (26 * ' ') + 'sample_name\n'
    assert print_string == title_row_account + second_row


@patch.object(models, 'get_api')
def test_unsupported_type(mock_get_api):
    make_models(models, mock_get_api)
    sample_account = models.Account(id='sample_id', name='sample_name')
    print_string = column_printer.print_columns([sample_account], 'Port')
    assert print_string == ''
