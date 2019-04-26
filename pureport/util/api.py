# -*- coding: utf-8 -*-
from requests import Session

from ..exception.api import raise_response_exception

__docformat__ = 'reStructuredText'


class RelativeSession(Session):
    def __init__(self, base_url, **kwargs):
        """
        A :class:`requests.Session` subclass that prepends a base url to all requests.
        :param str base_url: the base url
        """
        super(RelativeSession, self).__init__()
        self._base_url = base_url

    def request(self, method, url, **kwargs):
        return super(RelativeSession, self).request(method, self._base_url + url, **kwargs)


class RaiseForStatusSession(Session):
    def __init__(self, *args, **kwargs):
        """
        A :class:`requests.Session` subclass that always raises_for_status on each request
        throwing a :class:`..exception.api.ClientHttpException` if necessary.
        """
        super(RaiseForStatusSession, self).__init__()

    def request(self, method, url, **kwargs):
        response = super(RaiseForStatusSession, self).request(method, url, **kwargs)
        raise_response_exception(response)
        return response


class RelativeRaiseForStatusSession(RelativeSession, RaiseForStatusSession):
    def __init__(self, *args, **kwargs):
        """
        A :class:`requests.Session` subclass that includes functionality from
        both :class:`RelativeSession` and :class:`RaiseForStatusSession`
        :param str base_url: the base url
        """
        super(RelativeRaiseForStatusSession, self).__init__(*args, **kwargs)
