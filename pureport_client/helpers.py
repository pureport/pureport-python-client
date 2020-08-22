# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import time

from functools import wraps
from datetime import (
    date,
    datetime
)


SERVER_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def format_date(value):
    """
    Formats a datetime, date or string as an ISO-8601 string,
    2020-01-01T00:00:00.00000Z
    :param datetime|date|int|str value:
    :rtype: str|None
    :raises: ValueError
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
        raise ValueError()
    return None


def retry(exception, tries=10, delay=1, backoff=2, max_delay=30):
    """
    Retry calling the decorated function using an exponential backoff.
    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    The default here allows for 181 seconds of retry.
    1 + 2 + 4 + 8 + 16 + 30 + 30 + 30 + 30 + 30 = 181
    :param Exception exception: the exception to check. may be a tuple of exceptions to check
    :param int tries: number of times to try (not retry) before giving up
    :param int delay: initial delay between retries in seconds
    :param int backoff: backoff multiplier e.g. value of 2 will double the delay each retry
    :param int max_delay: the maximum time between each retry
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
