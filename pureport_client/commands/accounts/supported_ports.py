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


class Command(AccountsMixin, CommandBase):
    """Display supported port information
    """

    @argument('facility_id')
    def list(self, facility_id):
        """Display the account supported ports

        \f
        :param facility_id: the id of the faility to retrieve ports for
        :type facility_id: str

        :returns: a list of SupportPort objects
        :rtype: list
        """
        params = {'facility': facility_id}
        return self.__call__('get', 'supportedPorts', params=params)
