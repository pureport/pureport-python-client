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
    """Display supported connection information
    """

    def list(self):
        """Display a list of supported connections

        \f
        :returns: a list of SupportedConnection objects
        :rtype: list
        """
        return self.__call__('get', 'supportedConnections')
