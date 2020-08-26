# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import argument

from pureport_client.commands import (
    CommandBase,
    AccountsMixin
)

from pureport_client.util import JSON


class Command(AccountsMixin, CommandBase):
    """Manage Pureport account API keys
    """

    def list(self):
        """Get a list of all API keys for an account.

        \f
        :returns: list of account objects
        :rtype: list
        """
        return self.__call__('get', 'apikeys')

    @argument('api_key')
    def get(self, api_key):
        """Get an account's API Key with the provided API Key key.

        \f
        :param api_key: the key associated with the API Key to return
        :type api_key: str

        :returns: an APIKey object
        :rtype: dict
        """
        return self.__call__('get', 'apikeys/{}'.format(api_key))

    @argument('api_key', type=JSON)
    def create(self, api_key):
        """Create an API Key for the provided account.

        \f
        :param api_key: the key associated with the API Key to return
        :type api_key: str
        """
        return self.__call__('post', 'apikeys', json=api_key)

    @argument('api_key', type=JSON)
    def update(self, api_key):
        """Update an API Key for the provided account.

        \f
        :param api_key: the key associated with the API Key to return
        :type api_key: str
        """
        return self.__call__(
            'put', 'apikeys/{key}'.format(**api_key), json=api_key
        )

    @argument('api_key')
    def delete(self, api_key):
        """Delete an API Key from the provided account.

        \f
        :param api_key: the key associated with the API Key to return
        :type api_key: str
        """
        self.__call__('delete', 'apikeys/{}'.format(api_key))
