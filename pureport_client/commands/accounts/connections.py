# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from pureport_client.commands import (
    CommandBase,
    AccountsMixin
)


class Command(AccountsMixin, CommandBase):
    """Display account connection information
    """

    def list(self):
        """Display a list of all account connections

        \f
        :returns: a list of connection objects
        :rtype: list
        """
        return self.__call__('get', 'connections')
