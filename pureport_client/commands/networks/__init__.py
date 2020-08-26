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
from pureport_client.commands import CommandBase

from pureport_client.commands.networks import connections


class Command(CommandBase):
    """Manage Pureport networks
    """

    @argument('network_id')
    def get(self, network_id):
        """Get a network with the provided network id.

        \f
        :param network_id: the network id to retrieve
        :type network_id: str

        :returns: a network object
        :rtype: dict
        """
        return self.__call__('get', '/networks/{}'.format(network_id))

    @argument('network', type=JSON)
    def update(self, network):
        """Update an exsiting network object

        \f
        :param network: the updated network object
        :type network: dict

        :returns: a network object
        :rtype: dict
        """
        return self.__call__('put', '/networks/{id}'.format(**network), json=network)

    @argument('network_id')
    def delete(self, network_id):
        """Delete an existing network

        \f
        :param network_id: the network id to delete
        :type network_id: str

        :returns: None
        """
        self.__call__('delete', '/networks/{}'.format(network_id))

    @option('-n', '--network_id', envvar='PUREPORT_NETWORK_ID', required=True)
    def connections(self, network_id):
        """Get the connections associated with this network

        \f
        :param network_id: the network id to retrieve from the server
        :type network_id: str

        :returns: a network object
        :rtype: dict
        """
        return connections.Command(self.client, network_id)
