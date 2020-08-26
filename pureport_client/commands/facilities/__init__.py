# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import argument

from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Display Pureport facility information
    """

    def list(self):
        """Get all available facilities.

        \f
        :returns: a list of all Pureport facilities
        :rtype: list
        """
        return self.__call__('get', '/facilities')

    @argument('facility_id')
    def get(self, facility_id):
        """Get a facility with the provided facility id.

        \f
        :param facility_id: the id of the facility to retrieve
        :type facility_id: str

        :returns: a facility object
        :rtype: dict
        """
        return self.__call__('get', '/facilities/{}'.format(facility_id))
