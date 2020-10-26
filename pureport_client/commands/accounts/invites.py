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
    """Manage Pureport account invites
    """

    def list(self):
        """Get all invites for the provided account.

        \f
        :returns: a list of AccountInvite objects
        :rtype: list
        """
        return self.client.find_account_invites()

    @argument('invite_id')
    def get(self, invite_id):
        """Get an account's invite with the provided account invite id.

        \f
        :param invite_id: the ID of the invite to retrieve
        :type invite_id: str

        :returns: an AccountInvite object
        :rtype: models.AccountInvite
        """
        return self.client.get_account_invite(invite_id)

    @argument('invite', type=JSON)
    def create(self, invite):
        """Create an account invite using the provided account.

        \f
        :param invite: an AccountInvite object
        :type invit: dict

        :returns: an AccountInvite object
        :rtype: models.AccountInvite
        """
        model_invite = models.load('AccountInvite', invite)
        model_invite.account_id = self.account_id
        return self.client.invite_account(model_invite)

    @argument('invite', type=JSON)
    def update(self, invite):
        """Update an account invite using the provided account.

        \f
        :param invite: an AccountInvite object
        :type invite: dict

        :returns: an AccountInvite object
        :rtype: models.AccountInvite
        """
        model_invite = models.load('AccountInvite', invite)
        model_invite.account_id = self.account_id
        return self.client.update_account_invite(model_invite)

    @argument('invite_id')
    def delete(self, invite_id):
        """Delete an account invite using the provided account.

        \f
        :param invite_id: the ID of the invite to retrieve
        :type invite_id: str

        :returns: None
        """
        self.client.delete_account_invite(invite_id)
