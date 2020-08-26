# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from os import getenv
from os.path import (
    exists,
    expanduser
)

from logging import getLogger

from yaml import safe_load

from pureport_client.exceptions import (
    ClientHttpError,
    MissingAccessTokenError
)

from pureport_client.session import PureportSession


log = getLogger(__name__)

API_URL = "https://api.pureport.com"
API_CONFIG_PATH = expanduser('~/.pureport/credentials.yml')
ENVIRONMENT_API_URL = 'PUREPORT_API_URL'
ENVIRONMENT_API_KEY = 'PUREPORT_API_KEY'
ENVIRONMENT_API_SECRET = 'PUREPORT_API_SECRET'
ENVIRONMENT_API_PROFILE = 'PUREPORT_API_PROFILE'


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


class Client(object):

    def __init__(self, base_url=None,
                 key=None, secret=None,
                 access_token=None, profile=None,
                 session=None):
        """
        Client for the Pureport ReST API
        This client is a thin wrapper around :module:`requests`.
        All API methods return a :class:`requests.Response` object.  It's up to the user
        to handle exceptions thrown by the API in the form of bad error codes.
        :param str base_url: a base url for the client
        :param str key: the key to use for login
        :param str secret: the secret to user for login
        :param str access_token: the access token obtained externally for an API key
        :param str profile: the pureport profile to use when using credentials from a file
        :param PureportSession session: a session variable for testing
        """

        # Storing the base_url for compatibility, for usage in `login`.
        # We used to create the client with the base_url and then login with
        # credentials.  This `base_url` would have been "forgotten" and reverted
        # back to using the PROD API_URL, but if we store it and use this as the default,
        # then it works exactly as it did before.
        self.base_url = base_url if base_url is not None else API_URL
        self.session = session if session else PureportSession(self.base_url)

        try:
            # Attempt login with the parameters provided.  Unlike above,
            # we are passing None for base_url by default to prevent cases
            # where environment credentials are different from the passed in base_url.
            self.login(key, secret, access_token, profile, base_url)
        except MissingAccessTokenError:
            pass
        except ClientHttpError as e:
            log.exception('There was an attempt to authenticate with '
                          'Pureport, but it failed.', e)

    @staticmethod
    def to_link(standard_object, title):
        """
        Many objects from the ReST API have reference to other objects that can
        also be retrieved from the ReST API.  That reference is typically a Link object.
        This function converts a standard API object to a Link.
        :param dict standard_object: the object to be converted to a link
        :param str title: an optional title value to give this object
        :rtype: Link
        """
        return {
            'id': standard_object['id'],
            'href': standard_object['href'],
            'title': title,
        }

    @staticmethod
    def __get_file_based_credentials(profile=None):
        if exists(API_CONFIG_PATH):
            with open(API_CONFIG_PATH) as f:
                config = safe_load(f)
                if 'profiles' in config:
                    profiles = config['profiles']
                    potential_profiles = [
                        profile,
                        getenv(ENVIRONMENT_API_PROFILE),
                        config['current_profile'] if 'current_profile' in config else None,
                        'default'
                    ]
                    for potential_profile in potential_profiles:
                        if potential_profile is not None and potential_profile in profiles:
                            return profiles[potential_profile]
        return None

    def login(self, key=None, secret=None, access_token=None, profile=None, api_url=None):
        """
        Login to Pureport ReST API with the specified key and secret or
        pass in a previously obtained access_token.
        This stores the access token on this client instance's session for usage.
        :param str key: the key to use for login
        :param str secret: the secret to user for login
        :param str access_token: the access token obtained externally for an API key
        :param str profile: the pureport profile to use when using credentials from a file
        :param str api_url: the api base url
        :returns: the obtained access_token
        :rtype: str
        :raises: .exception.ClientHttpException
        :raises: .exception.MissingAccessTokenError
        """
        file_credentials = Client.__get_file_based_credentials(profile)
        # Update api base_url
        base_url = self.base_url
        if api_url is not None:
            base_url = api_url
        elif getenv(ENVIRONMENT_API_URL) is not None:
            base_url = getenv(ENVIRONMENT_API_URL)
        elif file_credentials is not None and 'api_url' in file_credentials:
            base_url = file_credentials['api_url']
        self.base_url = base_url
        self.session._base_url = base_url
        # Update auth token
        if access_token is not None:
            self.session.set_access_token(access_token)
            return access_token
        elif key is not None and secret is not None:
            return self.session.login(key, secret)
        elif getenv(ENVIRONMENT_API_KEY) is not None and getenv(ENVIRONMENT_API_SECRET) is not None:
            return self.session.login(getenv(ENVIRONMENT_API_KEY), getenv(ENVIRONMENT_API_SECRET))
        elif file_credentials is not None and 'api_key' in file_credentials and 'api_secret' in file_credentials:
            return self.session.login(file_credentials['api_key'],
                                      file_credentials['api_secret'])
        raise MissingAccessTokenError()

    def open_api(self):
        """
        Get's the open api documentation
        :rtype: dict
        """
        return self.session.get('/openapi.json').json()
