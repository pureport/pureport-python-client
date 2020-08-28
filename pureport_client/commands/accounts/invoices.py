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
    """Display Pureport account invoice information
    """

    @argument('invoice_filter', type=JSON)
    def list(self, invoice_filter):
        """List all invoices for an account.

        \f
        """
        return self.__call__('get', 'invoices', json=invoice_filter)

    def list_upcoming(self):
        """List all upcoming invoices for an account.

        \f
        :returns: a list of NetworkInvoice objects
        :rtype: list
        """
        return self.__call__('get', 'invoices/upcoming')
