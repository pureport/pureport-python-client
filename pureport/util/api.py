# -*- coding: utf-8 -*-
import time
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


class PureportSession(RelativeSession, RaiseForStatusSession):
    def __init__(self, *args, **kwargs):
        """
        A :class:`requests.Session` subclass that includes functionality from
        both :class:`RelativeSession` and :class:`RaiseForStatusSession`
        :param str base_url: the base url
        """
        super(PureportSession, self).__init__(*args, **kwargs)

        self._access_token = None
        self._refresh_token = None
        self._token_expire_time = None

    def login(self, key, secret):
        """
        Login to Pureport ReST API with the specified key and secret
        This stores the access token on this client instance's session for usage.
        :param str key: the key to use for login
        :param str secret: the secret to user for login
        :returns: the obtained access_token
        :rtype: str
        :raises: .exception.ClientHttpException
        :raises: .exception.MissingAccessTokenException
        """
        result = self.post('/login', json={'key': key, 'secret': secret}).json()
        self.set_access_token(result['access_token'])
        self._refresh_token = result['refresh_token']
        self._token_expire_time = time.time() + result['expires_in']

        return self._access_token

    def set_access_token(self, access_token):
        self._access_token = access_token
        self.headers.update({'Authorization': 'Bearer %s' % access_token})

    def request(self, method, url, **kwargs):
        if self._refresh_token and self._token_expire_time and time.time() > self._token_expire_time:
            # Automatically refresh the access token using the refresh token
            self._access_token = None
            self._token_expire_time = None
            del self.headers['Authorization']
            result = self.post('/login/refresh', json={'refreshToken': self._refresh_token}).json()
            self.set_access_token(result['access_token'])
            self._token_expire_time = time.time() + result['expires_in']

        return super(PureportSession, self).request(method, url, **kwargs)
