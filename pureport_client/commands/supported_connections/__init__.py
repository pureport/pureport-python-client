# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import argument

from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Display Pureport supported connection information
    """

    @argument('supported_connection_id')
    def get(self, supported_connection_id):
        """Get the supported connection with the specified ID

        \f
        :param supported_connection_id: the id of the supported connection
            to retrieve
        :type supported_connection_id: str

        :returns: a supported connection object
        :type: dict
        """
        return self.__call__(
            'get', '/supportedConnections/{}'.format(supported_connection_id)
        )
