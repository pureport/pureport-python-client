# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved
import json

column_settings = json.loads(open('column_settings.json').read())


def print_columns(response, response_type):
    """prints a column style output for a list of networks
       currently only supports 'pureport accounts network list

    :param response: the response object
    :type response: array

    :returns a formatted output string
    :rtype: str
    """
    column_values = pick_list(response_type)

    return_string = ''
    # print Column Titles
    for column in column_values:
        title = column['title']
        formatted_title = title.ljust(column['width']) if column['width'] != -1 else title + '\n'
        return_string += formatted_title

    if (isinstance(response, list)):
        for row in response:
            return_string += print_row(row, column_values)
    else:
        return_string += print_row(response, column_values)

    return return_string


def print_row(row, column_values):
    row_string = ''
    for column in column_values:
        value = ''
        column_width = column['width']
        if hasattr(row, column['id']):
            value = getattr(row, column['id'])
            if 'json' in column:
                if value is not None:
                    value = json.dumps(value)
                else:
                    value = ''
            elif 'serialize' in column:
                if value is not None:
                    value = json.dumps(value.serialize())
                else:
                    value = ''

        formatted_string = value.ljust(column_width) if column_width != -1 else value + '\n'

        row_string += formatted_string
    return row_string


def pick_list(response_type):
    if response_type in column_settings.keys():
        return column_settings[response_type]
    else:
        return []
