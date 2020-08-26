# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import (
   option,
   argument,
   Choice
)

from pureport_client.commands import CommandBase


STATE_CHOICES = ('CREATED', 'RUNNING', 'COMPLETED', 'FAILED', 'DELETED')


class Command(CommandBase):
    """Display Pureport task information
    """

    @option('-s', '--state', type=Choice(STATE_CHOICES),
            help='The task state.')
    @option('-pn', '--page_number', type=int, help='The page number for pagination.')
    @option('-ps', '--page_size', type=int, help='The page size for pagination.')
    def list(self, state=None, page_number=None, page_size=None):
        """Display list of all tasks

        \f
        :param state: Filter results based on state
        :type state: str

        :param page_number: page number to display
        :type page_number: int

        :param page_size: number of results per page
        :type page_size: int

        :returns: a list of Task objects
        :rtype: list
        """
        params = {'state': state, 'pageNumber': page_number,
                  'pageSize': page_size}
        return self.__call__('get', '/tasks', params=params)

    @argument('task_id')
    def get(self, task_id):
        """Get a task by it's id.

        \f
        :param task_id: the ide of the task to retrieve
        :type task_id: string

        :returns: a Task object
        :rtype: dict
        """
        return self.__call__('get', '/tasks/{}'.format(task_id))
