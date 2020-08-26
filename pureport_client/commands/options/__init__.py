# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import option

from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Display Pureport options information
    """

    @option('-t', '--types', multiple=True,
            help='A filter for the list of enumeration types')
    def list(self, types=None):
        """List all option objects provided by the API

        \f
        Option objects are constant enumerations that are used for
        various parts of the Pureport API.  An optional set of types
        may be passed in to filter the response.

        :param types: a filter for the list of enumeration types
        :type types: list

        :returns: a list of option objects
        :rtype: list
        """
        return self.__call__('get', '/options', params={'type': types})
