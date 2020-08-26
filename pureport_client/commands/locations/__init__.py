# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import argument

from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Display Pureport location information
    """

    def list(self):
        """Display list of Pureport locations

        \f
        :returns: a list of location objects
        :rtype: list
        """
        return self.__call__('get', '/locations')

    @argument('location_id')
    def get(self, location_id):
        """Get a location with the provided location id.

        \f
        :param location_id: the id of the location to retrieve
        :type location_id: str

        :returns: a location object
        :rtype: dict
        """
        return self.__call__('get', '/locations/{}'.format(location_id))
