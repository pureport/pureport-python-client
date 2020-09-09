# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import urllib

from logging import getLogger

log = getLogger(__name__)


class CommandBase(object):
    """Base implementation of a CLI command
    """

    def __init__(self, client=None):
        """Create a new instance of `CommandBase`

        :param client: the Pureport API client instance
        :type client: `pureport_client.client.Client`

        :returns: an instance of CommandBase
        :rtype: `pureport_client.commands.CommandBase`
        """
        self._client = client

    client = property(lambda self: self._client)

    def __call__(self, method, url, *args, **kwargs):
        """Send the request to the API and return the results

        :param method: the HTTP method to call
        :type method: str

        :param url: the URL to send the call to
        :type url: str

        :returns: the body of the reponse convered from json
        :rtype: dict (or list)
        """
        log.debug('{} {}'.format(method.upper(), url))
        if 'params' in kwargs:
            kwargs['query'] = kwargs.pop('params')
        return getattr(self.client, method)(url, *args, **kwargs).json


class AccountsMixin(object):
    """Mixin class for prepending accounts url
    """

    def __init__(self, client, account_id):
        """Create a new instance of `AccountsMixin`

        :param client: the Pureport API client instance
        :type client: `pureport_client.client.Client`

        :param account_id: the Pureport account ID to use as the URL base
        :type account_id: str

        :returns: an instance of AccountsMixin
        :rtype: `pureport_client.commands.AccountsMixin`
        """

        super(AccountsMixin, self).__init__(client)
        self._account_id = account_id

    account_id = property(lambda self: self._account_id)

    def __call__(self, method, url, *args, **kwargs):
        """Send the request to the API and return the results

        This overload prepends `/accounts/{ account_id }` to the
        provided URL before sending it to the remote server.

        :param method: the HTTP method to call
        :type method: str

        :param url: the URL to send the call to
        :type url: str

        :returns: the body of the reponse convered from json
        :rtype: dict (or list)
        """
        url = urllib.parse.urljoin('/accounts/{}/'.format(self.account_id), url)
        return super(AccountsMixin, self).__call__(method, url, *args, **kwargs)


class NetworksMixin(object):
    """Mixin class for prepending networks url
    """

    def __init__(self, client, network_id):
        """Create a new instance of `NetworksMixin`

        :param client: the Pureport API client instance
        :type client: `pureport_client.client.Client`

        :param account_id: the Pureport network ID to use as the URL base
        :type account_id: str

        :returns: an instance of NetworksMixin
        :rtype: `pureport_client.commands.NetworksMixin`
        """
        super(NetworksMixin, self).__init__(client)
        self._network_id = network_id

    network_id = property(lambda self: self._network_id)

    def __call__(self, method, url, *args, **kwargs):
        """Send the request to the API and return the results

        This overload prepends `/networks/{ network_id }` to the
        provided URL before sending it to the remote server.

        :param method: the HTTP method to call
        :type method: str

        :param url: the URL to send the call to
        :type url: str

        :returns: the body of the reponse convered from json
        :rtype: dict (or list)
        """
        url = urllib.parse.urljoin('/networks/{}/'.format(self.network_id), url)
        return super(NetworksMixin, self).__call__(method, url, *args, **kwargs)
