# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved
import json

# Defining the Titles and Widths of the columns for the supported response type
network_list_column_values = {
    'id': {'title': 'ID', 'width': 35},
    'name': {'title': 'NAME', 'width': 25},
    'state': {'title': 'STATE', 'width': 25},
    'tags': {'title': 'TAGS', 'width': -1}
}


def print_networks(response):
    """prints a column stle output for a list of networks
       currently only supports 'pureport accounts network list

    :param response: the response object
    :type response: array

    :returns a formatted output string
    :rtype: str
    """
    # print Column Titles
    return_string = ''
    for key in network_list_column_values.keys():
        column_width = network_list_column_values[key]['width']
        title = network_list_column_values[key]['title']
        formatted_title = title.ljust(network_list_column_values[key]['width']) if column_width != -1 else title + '\n'
        return_string += formatted_title

    # print each row
    for row in response:
        for key in network_list_column_values.keys():
            value = ''
            column_width = network_list_column_values[key]['width']
            if hasattr(row, key):
                value = getattr(row, key)
                if key == 'tags':
                    if value is None:
                        value = 'No Tags'
                    else:
                        value = json.dumps(value)
            formatted_string = value.ljust(column_width) if column_width != -1 else value + '\n'

            return_string += formatted_string
    return return_string
