# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved


from pureport_client import column_printer
from pureport import models

title_row = 'ID' + (33 * ' ') + 'NAME' + (21 * ' ') + 'STATE' + (20 * ' ') + 'TAGS\n'


def setup():
    models.make()


def test_empty_list():
    printString = column_printer.print_networks([])
    assert printString == title_row


def test_empty_tags():
    sampleNetwork = models.Network(id='sample_id', name='sample_name')
    sampleNetwork.state = 'ACTIVE'
    printString = column_printer.print_networks([sampleNetwork])
    second_row = 'sample_id' + (26 * ' ') + 'sample_name' + (14 * ' ') + 'ACTIVE' + (19 * ' ') + 'No Tags\n'
    assert printString == title_row + second_row


def test_with_tags():
    tag = {'tagkey': 'tagValue'}
    sampleNetwork = models.Network(id='sample_id', name='sample_name')
    sampleNetwork.state = 'ACTIVE'
    sampleNetwork.tags = tag
    printString = column_printer.print_networks([sampleNetwork])
    second_row = 'sample_id' + (26 * ' ') + 'sample_name' + (14 * ' ') + 'ACTIVE' + (19 * ' ') + '{"tagkey": "tagValue"}\n'
    assert printString == title_row + second_row
