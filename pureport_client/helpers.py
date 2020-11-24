# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import time
from json import dumps as json_dumps
from yaml import dump as yaml_dumps

from pureport_client.column_printer import print_columns as column_dumps

from functools import wraps
from datetime import (
    date,
    datetime
)

from pureport import models
from pureport_client.column_settings import column_settings

SERVER_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def format_date(value):
    """Formats a datetime, date or string as an ISO-8601 string

    :param value: the date time value to format
    :type value: object

    :returns a formatted datetime string
    :rtype: str
    """
    if isinstance(value, datetime):
        return value.strftime(SERVER_DATE_FORMAT)
    elif isinstance(value, date):
        return value.strftime(SERVER_DATE_FORMAT)
    elif (isinstance(value, int) or
          isinstance(value, float)):
        return datetime \
            .fromtimestamp(value) \
            .strftime(SERVER_DATE_FORMAT)
    elif isinstance(value, str):
        for fmt in [
            '%Y/%m/%d',
            '%Y-%m-%d',
            '%Y.%m.%d',
            '%Y,%m,%d',
            '%Y-%m-%dT%H',
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S.%fZ'
        ]:
            try:
                return datetime \
                    .strptime(value, fmt) \
                    .strftime(SERVER_DATE_FORMAT)
            except ValueError:
                pass
        raise ValueError(value)


def retry(exception, tries=10, delay=1, backoff=2, max_delay=30):
    """Retry calling the decorated function using an exponential backoff

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    The default here allows for 181 seconds of retry.
    1 + 2 + 4 + 8 + 16 + 30 + 30 + 30 + 30 + 30 = 181

    :param exception: the exception or list of exceptions to check
    :type exception: tuple

    :param tries: the number of times to try (not retry) before giving up
    :type tries: int

    :param delay: initial delay between retries in seconds
    :type delay: int

    :param backoff: backoff multiplier (e.g. value of 2 will double the
        delay each retry)
    :type backoff: int

    :param max_delay: the maximim time between each retry
    :type max_delay: int

    :returns: a wrapped function
    :rtype: function
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            m_tries, m_delay = tries, delay
            while m_tries > 1:
                try:
                    return f(*args, **kwargs)
                except exception:
                    time.sleep(min(m_delay, max_delay))
                    m_tries -= 1
                    m_delay *= backoff
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry


def paginate(client_fun, *args, **kwargs):
    """
    Given a client function that supports the page_size and page_number
    keyword arguments for pagination, this generator will yield all results
    from that function.
    :param function client_fun:
    :rtype: Iterator
    """
    resp = client_fun(*args, **kwargs)
    yield from resp['content']
    total_elements = resp['totalElements']
    page_size = resp['pageSize']
    page_number = resp['pageNumber'] + 1
    if 'page_number' in kwargs:
        kwargs.pop('page_number')
    while page_number * page_size < total_elements:
        resp = client_fun(*args, page_number=page_number, **kwargs)
        yield from resp['content']
        page_number = resp['pageNumber'] + 1


def format_output(response, response_format):
    """Formats the output of the response object into the specified format option

    :param response: the response object
    :type response: object

    :param response_format the format type to be printed, json_pp, json, yaml, and column are options
    :type response_format: str

    :returns a formatted output string
    :rtype: str
    """
    if response is not None:
        has_printed_columns = False
        # Check if the response has model obects
        if contains_model_object(response):
            response_type = get_response_type(response)
            if response_type in column_settings.keys() and response_format == 'column':
                return column_dumps(response, response_type)
            elif isinstance(response, list):
                response = [o.serialize() for o in response]
            else:
                response = response.serialize()

        # fallback mode
        if response_format == 'json_pp' or (response_format == 'column' and not has_printed_columns):
            return json_dumps(response, indent=2, sort_keys=True)
        elif response_format == 'json':
            return json_dumps(response)
        elif response_format == 'yaml':
            return yaml_dumps(response)


def contains_model_object(response):
    if hasattr(models, type(response).__name__):
        return True
    if isinstance(response, list) and len(response) > 0 and hasattr(models, type(response[0]).__name__):
        return True
    return False


def get_response_type(response):
    if isinstance(response, list):
        if len(response) > 0:
            return type(response[0]).__name__
    return type(response).__name__
