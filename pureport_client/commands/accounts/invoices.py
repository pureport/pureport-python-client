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
        # FIXME: to write a better descriptoin for parameters
        :param dict invoice_filter: a filter object that matches Stripe's invoice filter
            https://stripe.com/docs/api/invoices/list
        :rtype: list[NetworkInvoice]
        :raises: .exception.ClientHttpError
        """
        return self.__call__('post', 'invoices', json=invoice_filter)

    def list_upcoming(self):
        """List all upcoming invoices for an account.

        \f
        :returns: a list of NetworkInvoice objects
        :rtype: list
        """
        return self.__call__('get', 'invoices/upcoming')
