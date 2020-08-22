from datetime import date, datetime


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
