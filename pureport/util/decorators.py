import time
from functools import wraps


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
