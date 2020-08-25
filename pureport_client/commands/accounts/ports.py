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
    """Manage Pureport account ports
    """

    def list(self):
        """Display all account ports

        \f
        :returns: a list of Port objects
        :rtype: list
        """
        return self.__call__('get', 'ports')

    @argument('port', type=JSON)
    def create(self, port):
        """Create a port for the provided account

        \f
        :param port: a Port object
        :type port: dict

        :returns: an updated Port object
        :rtype: dict
        """
        return self.__call__('post', 'ports', json=port)
