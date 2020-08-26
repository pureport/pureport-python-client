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
    """Manage Pureport account consent details
    """

    def get(self):
        """Get the consent information for the provided account.

        \f
        :returns: the AccountConsent object
        :rtype: dict
        """
        return self.__call__('get', 'consent')

    def accept(self):
        """Accept consent for the provided account.

        \f
        :returns: an AccountConsent object
        :rtype: dict
        """
        return self.__call__('post', 'consent')
