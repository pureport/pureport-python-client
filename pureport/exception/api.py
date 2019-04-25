# -*- coding: utf-8 -*-

__docformat__ = 'reStructuredText'


class MissingAccessTokenException(IOError):
    pass


class ClientHttpException(IOError):
    def __init__(self, *args, **kwargs):
        """
        An exception representing a bad http call from the client
        :param int code: the http status code
        :param str message: the message describing the issue
        :param requests.Response response: the response object returned from the Http library
        """
        self.status_code = kwargs.pop('status_code', None)
        self.response = kwargs.pop('response', None)
        super(ClientHttpException, self).__init__(*args, **kwargs)
