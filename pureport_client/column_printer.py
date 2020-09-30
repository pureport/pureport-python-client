# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved
import json

# Defining the Titles and Widths of the columns for the supported response type
network_list_column_values = [
    {'id': 'id', 'title': 'ID', 'width': 35},
    {'id': 'name', 'title': 'NAME', 'width': 25},
    {'id': 'state', 'title': 'STATE', 'width': 25},
    {'id': 'tags', 'title': 'TAGS', 'width': -1}
]


def print_networks(response):
    """prints a column style output for a list of networks
       currently only supports 'pureport accounts network list

    :param response: the response object
    :type response: array

    :returns a formatted output string
    :rtype: str
    """
    # print Column Titles
    return_string = ''
    for column in network_list_column_values:
        title = column['title']
        formatted_title = title.ljust(column['width']) if column['width'] != -1 else title + '\n'
        return_string += formatted_title

    # print each row
    for row in response:
        for column in network_list_column_values:
            value = ''
            column_width = column['width']
            if hasattr(row, column['id']):
                value = getattr(row, column['id'])
                if column['id'] == 'tags':
                    if value is None:
                        value = 'No Tags'
                    else:
                        value = json.dumps(value)
            formatted_string = value.ljust(column_width) if column_width != -1 else value + '\n'

            return_string += formatted_string
    return return_string
