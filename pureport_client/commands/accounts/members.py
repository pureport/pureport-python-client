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
    """Manage Pureport account members
    """

    @argument('user_id')
    def get(self, user_id):
        """Display account information for the provided id

        \f
        :param user_id: the id of the user to retrieve
        :type user_id: str

        :returns: an AccountMember object
        :rtype: dict
        """
        return self.__call__('get', 'members/{}'.format(user_id))

    @argument('member', type=JSON)
    def create(self, member):
        """Create an member for the provided account.

        \f
        :param member: an AccountMember object
        :type member: dict

        :returns: the created AccountMember object
        :rtype: dict
        """
        return self.__call__('post', 'members', json=member)

    @argument('member', type=JSON)
    def update(self, member):
        """Update a member for the provided account.

        \f
        :param member: an AccountMember object
        :type member: dict

        :returns: the created AccountMember object
        :rtype: dict
        """
        return self.__call__('put', 'members/{user}'.format(**member), json=member)

    @argument('user_id')
    def delete(self, user_id):
        """Delete a member from the provided account.

        \f
        :param user_id: the id of the member to delete
        :type user_id: str

        :returns: None
        """
        self.__call__('delete', 'members/{}'.format(user_id))
