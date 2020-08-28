# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import (
    option,
    argument
)

from pureport_client.util import JSON
from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Manage Pureport accounts
    """

    @option('-i', '--ids', multiple=True, help='Find a particular set of accounts by their ids.')
    @option('-p', '--parent_id', help='Find all children accounts of a single parent account.')
    @option('-n', '--name', help='Search for accounts by their name.')
    @option('-l', '--limit', type=int, help='Limit the number of results.')
    def list(self, ids=None, parent_id=None, name=None, limit=None):
        """Get a list of all accounts.

        \f
        :param ids: a list of account ids to find
        :type ids: list

        :param parent_id: a parent acocunt id
        :type parent_id: str

        :param name: a name for lowercase inter-word checking
        :type name: str

        :param limit: the max number of entrie to return
        :type limit: int

        :returns: a liist of accounts
        :rtype: list
        """
        params = {'ids': ids, 'parentId': parent_id, 'name': name, 'limit': limit}
        return self.__call__('get', '/accounts', params=params)

    @argument('account_id')
    def get(self, account_id):
        """Get an account by its id.

        \f
        :param str account_id: the account id
        :rtype: Account
        :raises: .exception.ClientHttpError
        """
        self.__call__('get', '/accounts/{}'.format(account_id))

    @argument('account', type=JSON)
    def create(self, account):
        """Create a new Pureport account

        \f
        :param account: Account object to be created
        :type account: dict

        :returns: the created Account object
        :rtype: dict
        """
        return self.__call__('post', '/accounts', json=account)

    @argument('account', type=JSON)
    def update(self, account):
        """Update an existing account.

        \f
        :param account: the Account object
        :type account: dict

        :returns: an updated Account object
        :rtype: dict
        """
        return self.__call__('put', '/accounts/{id}'.format(**account), json=account)

    @argument('account_id')
    def delete(self, account_id):
        """Delete an existing account.

        \f
        :param account_id: the id of the account to delete
        :type account_id: str

        :returns: None
        """
        self.__call__('delete', '/accounts/{}'.format(account_id))

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def api_keys(self, account_id):
        """Manage Pureport account API kyes

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.api_keys import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def audit_log(self, account_id):
        """Manage Pureport account audit logs

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.audit_log import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def billing(self, account_id):
        """Manage Pureport account billing details

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.billing import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def connections(self, account_id):
        """Manage Pureport account connections

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: accounts commands command
        :rtype: Command
        """
        from pureport_client.commands.accounts.connections import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def consent(self, account_id):
        """Manage Pureport account consent agreements

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.consent import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def invites(self, account_id):
        """Manage Pureport account invitations

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.invites import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def invoices(self, account_id):
        """Manage Pureport account invoices

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.invoices import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def members(self, account_id):
        """Manage Pureport account members

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.members import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def metrics(self, account_id):
        """Manage Pureport account metrics

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.metrics import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def networks(self, account_id):
        """Manage Pureport account networks

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.networks import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def permissions(self, account_id):
        """Manage Pureport account permissions

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.permissions import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def ports(self, account_id):
        """Manage Pureport account ports

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.ports import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def roles(self, account_id):
        """Manage Pureport account roles

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.roles import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def supported_connections(self, account_id):
        """Manage Pureport account supported connections

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.supported_connections import Command
        return Command(self.client, account_id)

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def supported_ports(self, account_id):
        """Manage Pureport account supported ports

        \f
        :param account_id: the id of the account to manage
        :type account_id: str

        :returns: a command instance
        :rtype: Command
        """
        from pureport_client.commands.accounts.supported_ports import Command
        return Command(self.client, account_id)
