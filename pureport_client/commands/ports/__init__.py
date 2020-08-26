# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import argument

from pureport_client.util import JSON
from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Manage Pureport ports
    """

    @argument('port_id')
    def get(self, port_id):
        """Get the port with the provided port id.

        \f
        :param port_id: the id of the port to retrieve
        :type port_id: str

        :returns: a port object
        :rtype: dict
        """
        return self.__call__('get', '/ports/{}'.format(port_id))

    @argument('port_id')
    def get_accounts_using_port(self, port_id):
        """Get the accounts using the port with the provided port id.

        \f
        :param port_id: the id of the port to use
        :type port_id: str

        :returns: a list of Link objects
        :rtype: list
        """
        return self.__call__('get', '/ports/{}/accounts'.format(port_id))

    @argument('port', type=JSON)
    def update(self, port):
        """Update an existing port

        \f
        :param port: the Port object
        :type port: dict

        :returns: a Port object
        :rtype: dict
        """
        return self.__call__('put', '/ports/{id}'.format(**port), json=port)

    @argument('port_id')
    def delete(self, port_id):
        """Delete a port.
        \f

        :param port: the Port object
        :type port: dict

        :returns: None
        """
        self.__call__('delete', '/ports/{}'.format(port_id))
