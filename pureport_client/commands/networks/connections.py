# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import (
    option,
    argument
)

from pureport_client.util import JSON

from pureport_client.commands import (
    CommandBase,
    NetworksMixin
)

from pureport_client.commands.connections import (
    get_connection_until_state,
    ConnectionState
)


class Command(NetworksMixin, CommandBase):
    """Manage Pureport network connections
    """

    def list(self):
        """List all connections for the provided network

        \f
        :returns: a list of connection objects
        :rtype: list
        """
        return self.__call__('get', 'connections')

    @argument('connection', type=JSON)
    @option('-w', '--wait_until_active', is_flag=True,
            help='Wait until the connection is active.')
    def create(self, connection, wait_until_active=False):
        """Create a connection for the provided network.

        \f
        :param connection: the connection object to create
        :type connection: dict

        :param wait_until_active: wait until the connection is active using a backoff retry
        :type wait_until_active: bool

        :returns: a connection object
        :rtype: dict
        """
        connection = self.__call__('post', 'connections', json=connection)

        if wait_until_active:
            connection = get_connection_until_state(
                self.session,
                connection['id'],
                ConnectionState.ACTIVE,
                [ConnectionState.FAILED_TO_PROVISION]
            )

        return connection
