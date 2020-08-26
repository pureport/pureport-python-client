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
    """Display Pureport connection metrics
    """

    @argument('options', type=JSON)
    def usage_by_connection(self, options):
        """Display total usage by connection

        \f
        :param options: a UsageByConnectionOptions object
        :type options: dict

        :returns: a list of NetworkConnectionEgressIngress objects
        :rtype: list
        """
        return self.__call__('post', 'metrics/usageByConnection', json=options)

    @argument('options', type=JSON)
    def usage_by_connection_and_time(self, options):
        """Display usage for a connection over time

        \f
        :param: a UsageByConnectionAndTimeOptions object
        :type: dict

        :returns: a list of ConnectionTimeEgressIngress objects
        :rtype: list
        """
        return self.__call__('post', 'metrics/usageByConnectionAndTime', json=options)

    @argument('options', type=JSON)
    def usage_by_network_and_time(self, options):
        """Dispay usage of networks over time

        \f
        :param: a UsageByNetworkAndTimeOptions object
        :type: dict

        :returns: a list of NetworkTimeUsage objects
        :rtype: list
        """
        return self.__call__('post', 'metrics/usageByNetworkAndTime', json=options)
