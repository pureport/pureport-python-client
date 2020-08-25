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
    """Manage Pureport account roles
    """

    def list(self):
        """Display all roles for the provided account

        \f
        :returns: a list of AccountRole objects
        :rtype: list
        """
        return self.__call__('get', 'roles')

    @argument('role_id')
    def get(self, role_id):
        """Display role identified by ID

        \f
        :param role_id: the id of the role to retrieve
        :type role_id: str

        :returns: an AccountRole object
        :rtype: dict
        """
        return self.__call__('get', 'roles/{}'.format(role_id))

    @argument('role', type=JSON)
    def create(self, role):
        """Create a role for the provided account

        \f
        :param role: an AccountRole object
        :type role: dict

        :returns: a created AccountRole object
        :rtype: dickt
        """
        return self.__call__('post', 'roles', json=role)

    @argument('role', type=JSON)
    def update(self, role):
        """Update a role for the provided account

        \f
        :param role: an AccountRole object
        :type role: dict

        :returns: an updated AccountRole object
        :rtype: dickt
        """
        return self.__call__('put', 'roles/{id}'.format(**role), json=role)

    @argument('role_id')
    def delete(self, role_id):
        """Delete a role identified by ID

        \f
        :param role_id: the id of the role to retrieve
        :type role_id: str

        :returns: None
        """
        self.__call__('delete', 'roles/{}'.format(role_id))
