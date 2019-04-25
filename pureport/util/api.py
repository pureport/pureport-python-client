# -*- coding: utf-8 -*-
from requests import Session, HTTPError

from ..exception.api import ClientHttpException

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
        throwing an error.
        """
        super(RaiseForStatusSession, self).__init__()

    def request(self, method, url, **kwargs):
        response = super(RaiseForStatusSession, self).request(method, url, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise ClientHttpException(*e.args, status_code=e.response.status_code, response=e.response)
        return response


class RelativeRaiseForStatusSession(RelativeSession, RaiseForStatusSession):
    def __init__(self, *args, **kwargs):
        """
        A :class:`requests.Session` subclass that includes functionality from
        both :class:`RelativeSession` and :class:`RaiseForStatusSession`
        :param str base_url: the base url
        """
        super(RelativeRaiseForStatusSession, self).__init__(*args, **kwargs)
