# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import argument

from pureport_client.util import JSON
from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Display Pureport gateway information
    """

    @argument('gateway_id')
    def get(self, gateway_id):
        """Get a gateway by its id

        \f
        :param gateway_id: the id of the gateway to retrieve
        :type gateway_id: str

        :returns: a gateway object
        :rtype: dict
        """
        return self.__call__('get', '/gateways/{}'.format(gateway_id))

    @argument('gateway_id')
    def get_bgp_routes(self, gateway_id):
        """Get the bgp routes for a gateway.

        \f
        :param gateway_id: the id of the gateway to retrieve bgp routes from
        :type gateway_id: str

        :returns: a  list of bgp route objects
        :rtype: list
        """
        return self.__call__('get', '/gateways/{}/bgpRoutes'.format(gateway_id))

    @argument('gateway_id')
    @argument('date_filter', type=JSON)
    def get_connectivity_over_time(self, gateway_id, date_filter):
        """Get the connectivity details for a gateway by id over time.

        \f
        :param gateway_id: the id of the gateway to retrieve bgp routes from
        :type gateway_id: str

        :param date_filter: a date filter consisting of 'gt', 'lt',
            'gte', 'lte' properties
        :type date_filter: dict
        """
        return self.__call__(
            'post',
            '/gateways/{}/metrics/connectivity'.format(gateway_id),
            json=date_filter
        )

    @argument('gateway_id')
    def get_latest_connectivity(self, gateway_id):
        """Get the current connectivity details for a gateway by id.

        \f
        :param gateway_id: the id of the gateway to retrieve stats from
        :type gateway_id: str

        """
        return self.__call__(
            'get',
            '/gateways/{}/metrics/connectivity/current'.format(gateway_id)
        )

    @argument('gateway_id')
    def get_tasks(self, gateway_id):
        """Get the tasks for a gateway.

        \f
        :param gateway_id: the id of the gateway to retrieve stats from
        :type gateway_id: str

        :returns: a Task object
        :rtype: dict
        """
        self.__call__('get', '/gateways/{}/tasks'.format(gateway_id))

    @argument('gateway_id')
    @argument('task', type=JSON)
    def create_task(self, gateway_id, task):
        """Create a task for a gateway.

        \f
        :param gateway_id: the id of the gateway to retrieve stats from
        :type gateway_id: str

        :param task: task object to be created
        :type task: dict
        """
        self.__call__('post', '/gateways/{}/tasks'.format(gateway_id), json=task)
