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
    """Manage Pureport account roles
    """

    def list(self):
        """Display all roles for the provided account

        \f
        :returns: a list of AccountRole objects
        :rtype: list
        """
        return self.client.find_all_roles()

    @argument('role_id')
    def get(self, role_id):
        """Display role identified by ID

        \f
        :param role_id: the id of the role to retrieve
        :type role_id: str

        :returns: an AccountRole object
        :rtype: models.Role
        """
        return self.client.get_role(role_id)

    @argument('role', type=JSON)
    def create(self, role):
        """Create a role for the provided account

        \f
        :param role: an AccountRole object
        :type role: dict

        :returns: a created AccountRole object
        :rtype: models.Role
        """
        model = models.load('Role', role)
        model.account_id = self.account_id

        return self.client.create_role(model)

    @argument('role', type=JSON)
    def update(self, role):
        """Update a role for the provided account

        \f
        :param role: an AccountRole object
        :type role: dict

        :returns: an updated AccountRole object
        :rtype: models.Role
        """
        model = models.load('Role', role)
        model.account_id = self.account_id

        return self.client.update_role(model)

    @argument('role_id')
    def delete(self, role_id):
        """Delete a role identified by ID

        \f
        :param role_id: the id of the role to retrieve
        :type role_id: str

        :returns: None
        """
        self.client.delete_role(role_id)
