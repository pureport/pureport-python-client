# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from pureport_client.commands import (
    CommandBase,
    AccountsMixin
)


class Command(AccountsMixin, CommandBase):
    """Display Pureport account permissions
    """

    def get(self):
        """Display permissions for the provided account

        \f
        :returns: an AccountPermissions object
        :rtype: dict
        """
        return self.__call__('get', 'permissions')
