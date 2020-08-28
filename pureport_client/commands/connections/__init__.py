# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from enum import Enum

from click import option, argument

from pureport_client.util import JSON
from pureport_client.helpers import retry
from pureport_client.commands import CommandBase

from pureport_client.exceptions import (
    ClientHttpError,
    ConnectionOperationTimeoutError,
    ConnectionOperationFailedError
)


class ConnectionState(Enum):
    INITIALIZING = "INITIALIZING"
    WAITING_TO_PROVISION = "WAITING_TO_PROVISION"
    PROVISIONING = "PROVISIONING"
    FAILED_TO_PROVISION = "FAILED_TO_PROVISION"
    ACTIVE = "ACTIVE"
    DOWN = "DOWN"
    UPDATING = "UPDATING"
    FAILED_TO_UPDATE = "FAILED_TO_UPDATE"
    DELETING = "DELETING"
    FAILED_TO_DELETE = "FAILED_TO_DELETE"
    DELETED = "DELETED"


@retry(ConnectionOperationTimeoutError)
def get_connection_until_state(session, connection_id, expected_state, failed_states):
    """Retrieve a connection until it enters a certain state using an exponential backoff

    :param session: a pureport api session instance
    :rype: PureportSession

    :param connection_id: the id of the connection to retrieve
    :type connection_id: str

    :param expected_state: the execpted state of the connection
    :type: ConnectionState

    :param failed_states: list of states to be considered failed
    :type: ConnectionState

    :returns: a Connection object
    :rtype: dict

    :raises: ConnectionOperationFailedError

    :raises: ConnectionOperationTimeoutError
    """
    connection = session.get('/connections/%s' % connection_id).json()

    if ConnectionState[connection['state']] in failed_states:
        raise ConnectionOperationFailedError(connection=connection)
    elif ConnectionState[connection['state']] != expected_state:
        raise ConnectionOperationTimeoutError(connection=connection)

    return connection


@retry(ConnectionOperationTimeoutError)
def get_connection_until_not_found(session, connection_id, failed_states):
    """Retrieve a connection until it no longer exists using an exponential backoff

    :param session: a pureport api session instance
    :rype: PureportSession

    :param connection_id: the id of the connection to retrieve
    :type connection_id: str

    :param failed_states: list of states to be considered failed
    :type: ConnectionState

    :returns: a Connection object
    :rtype: dict

    :raises: ConnectionOperationFailedError

    :raises: ConnectionOperationTimeoutError
    """
    try:
        connection = session.get('/connections/%s' % connection_id).json()
    except ClientHttpError:
        return

    if ConnectionState[connection['state']] in failed_states:
        raise ConnectionOperationFailedError(connection=connection)

    raise ConnectionOperationTimeoutError(connection=connection)


class Command(CommandBase):
    """Manage Pureport connections
    """

    @argument('connection_id')
    def get(self, connection_id):
        """Display connection identified by connection id

        \f
        :param connection_id: the id of the connection to retrieve
        :type connection_id: str

        :returns: a Connection object
        :rtype: dict
        """
        return self.__call__('get', '/connections/{}'.format(connection_id))

    @argument('connection', type=JSON)
    @option('-w', '--wait_until_active', is_flag=True,
            help='Wait until the connection is active.')
    def update(self, connection, wait_until_active=False):
        """Update a connection configuration

        \f
        :param connection: the updated Connection object
        :type connection: dict

        :param wait_until_action: block until connection is updated
        :type: wait_until_action: bool

        :returns: an updated Connection object
        :rtype: dict
        """
        connection = self.__call__(
            'put', '/connections/{id}'.format(**connection), json=connection
        )

        if wait_until_active:
            connection = get_connection_until_state(
                self.session,
                connection['id'],
                ConnectionState.ACTIVE,
                (ConnectionState.FAILED_TO_UPDATE,)
            )

        return connection

    @argument('connection_id')
    @option('-w', '--wait_until_deleted', is_flag=True,
            help='Wait until the connection is deleted.')
    def delete(self, connection_id, wait_until_deleted=False):
        """Delete an existing connection

        \f
        :param connection_id: the id of the connection to retrieve
        :type connection_id: str

        :param wait_until_deleted: block until connection is updated
        :type: wait_until_deleted: bool

        :returns: None
        """
        self.__call__('delete', '/connections/{}'.format(connection_id))

        if wait_until_deleted:
            get_connection_until_not_found(
                self.session,
                connection_id,
                [ConnectionState.FAILED_TO_DELETE]
            )

    @argument('connection_id')
    def get_tasks(self, connection_id):
        """Display the tasks for a connection

        \f
        :param connection_id: the id of the connection to retrieve
        :type connection_id: str

        :returns: a list of Task objects
        :rtype: list
        """
        return self.__call__('get', '/connections/{}/tasks'.format(connection_id))

    @argument('connection_id')
    @argument('task', type=JSON)
    def create_task(self, connection_id, task):
        """Create a task for a connection

        \f
        :param connection_id: the id of the connection to retrieve
        :type connection_id: str

        :param task: a Task object
        :type: dict

        :returns: a Task object
        :rtype: dict
        """
        return self.__call__(
            'post', '/connections/{}/tasks'.format(connection_id), json=task
        )
