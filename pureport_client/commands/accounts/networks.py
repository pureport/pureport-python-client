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
from pureport import models


class Command(AccountsMixin, CommandBase):
    """Manage Pureport account networks
    """

    def list(self):
        """Display all networks for the provided account

        \f
        :returns: a list of Network objects
        :rtype: list
        """
        return self.client.find_networks()

    @argument('network', type=JSON)
    def create(self, network):
        """Create a network for the provided account.

        \f
        :param network: a Network object to be created
        :type network: dict

        :returns: an new Network object
        :rtype: models.Network
        """
        model = models.load("Network", network)
        model.account_id = self.account_id
        return self.client.add_network(model=model)
