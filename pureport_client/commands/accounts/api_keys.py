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
from pureport import models


class Command(AccountsMixin, CommandBase):
    """Manage Pureport account API keys
    """

    def list(self):
        """Get a list of all API keys for an account.

        \f
        :returns: list of account objects
        :rtype: list
        """
        return self.client.find_api_keys()

    @argument('api_key')
    def get(self, api_key):
        """Get an account's API Key with the provided API Key key.

        \f
        :param api_key: the key associated with the API Key to return
        :type api_key: str

        :returns: an APIKey object
<<<<<<< HEAD
        :rtype: ApiKey
=======
        :rtype: models.ApiKey
>>>>>>> 631bf48... Adding object model refactors for a few more command types (#66)
        """
        return self.client.get_api_key(api_key)

    @argument('api_key', type=JSON)
    def create(self, api_key):
        """Create an API Key for the provided account.

        \f
        :param api_key: the key associated with the API Key to return
        :type api_key: str
        """
        model = models.load("ApiKey", api_key)
        model.account_id = self.account_id
        return self.client.create_api_key(model=model)

    @argument('api_key', type=JSON)
    def update(self, api_key):
        """Update an API Key for the provided account.

        \f
        :param api_key: the key associated with the API Key to return
        :type api_key: str
        """
        model = models.load("ApiKey", api_key)
        model.account_id = self.account_id
        return self.client.update_api_key(model=model)

    @argument('api_key')
    def delete(self, api_key):
        """Delete an API Key from the provided account.

        \f
        :param api_key: the key associated with the API Key to return
        :type api_key: str
        """
        self.client.delete_api_key(api_key)
