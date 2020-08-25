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
    """Manage Pureport account billing details
    """

    def get(self):
        """Get the billing information for the provided account.

        \f
        :returns: an AccountBilling object
        :rtype: dict
        """
        return self.__call__('get', 'billing')

    def get_configured(self):
        """Display all billing information

        \f
        :returns: a boolean if billing is configured
        :rtype: bool
        """
        return self.__call__('get', 'billing/configured')

    @argument('account_billing', type=JSON)
    def create(self, account_billing):
        """Add a payment method to provided account.

        \f
        :param account_billing: an AccountBilling object
        :type account_billing: dict

        :returns: an updated AccountBilling object
        :rtype: dict
        """
        return self.__call__('post', 'billing', json=account_billing)

    @argument('account_billing', type=JSON)
    def update(self, account_billing):
        """Update the payment method for the provided account.

        \f
        :param account_billing: an AccountBilling object
        :type account_billing: dict

        :returns: an updated AccountBilling object
        :rtype: dict
        """
        return self.__call__('put', 'billing', json=account_billing)

    def delete(self):
        """Delete the current billing information
        \f
        :returns: None
        """
        self.__call__('delete', 'billing')
