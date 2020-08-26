# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import (
    option,
    Choice
)

from pureport_client.helpers import format_date
from pureport_client.commands import (
    CommandBase,
    AccountsMixin
)


EVENT_TYPES = ('USER_LOGIN', 'USER_FORGOT_PASSWORD', 'API_LOGIN',
               'ACCOUNT_CREATE', 'ACCOUNT_UPDATE', 'ACCOUNT_DELETE',
               'ACCOUNT_BILLING_CREATE', 'ACCOUNT_BILLING_UPDATE',
               'ACCOUNT_BILLING_DELETE', 'NETWORK_CREATE',
               'NETWORK_UPDATE', 'NETWORK_DELETE', 'CONNECTION_CREATE',
               'CONNECTION_UPDATE', 'CONNECTION_DELETE',
               'GATEWAY_CREATE', 'GATEWAY_UPDATE', 'GATEWAY_DELETE',
               'API_KEY_CREATE', 'API_KEY_UPDATE', 'API_KEY_DELETE',
               'ROLE_CREATE', 'ROLE_UPDATE', 'ROLE_DELETE', 'USER_CREATE',
               'USER_UPDATE', 'USER_DELETE', 'USER_DOMAIN_CREATE',
               'USER_DOMAIN_UPDATE', 'USER_DOMAIN_DELETE', 'PORT_CREATE',
               'PORT_UPDATE', 'PORT_DELETE', 'MEMBER_INVITE_CREATE',
               'MEMBER_INVITE_ACCEPT', 'MEMBER_INVITE_UPDATE',
               'MEMBER_INVITE_DELETE', 'ACCOUNT_MEMBER_CREATE',
               'ACCOUNT_MEMBER_UPDATE', 'ACCOUNT_MEMBER_DELETE',
               'CONNECTION_STATE_CHANGE', 'GATEWAY_STATE_CHANGE',
               'GATEWAY_BGP_STATUS_CHANGE', 'GATEWAY_IPSEC_STATUS_CHANGE',
               'NOTIFICATION_CREATE', 'NOTIFICATION_UPDATE',
               'NOTIFICATION_DELETE', 'TASK_CREATE',
               'TASK_UPDATE', 'TASK_DELETE')


SUBJECT_TYPES = ('ACCOUNT', 'CONNECTION', 'NETWORK', 'USER',
                 'USER_DOMAIN', 'ROLE', 'API_KEY', 'GATEWAY',
                 'NOTIFICATION', 'ACCOUNT_INVITE', 'ACCOUNT_BILLING',
                 'PORT', 'ACCOUNT_MEMBER', 'TASK')


SORT_CHOICES = ('timestamp', 'eventType', 'subjectType', 'ipAddress',
                'userAgent', 'source', 'result')


class Command(AccountsMixin, CommandBase):
    """Display Pureport account audit log details
    """

    @option('-pn', '--page_number', type=int, help='The page number for pagination.')
    @option('-ps', '--page_size', type=int, help='The page size for pagination.')
    @option('-s', '--sort', type=Choice(SORT_CHOICES),
            help='How should the data be sorted.')
    @option('-sd', '--sort_direction', type=Choice(['ASC', 'DESC']),
            help='The direction the results will be sorted.')
    @option('-st', '--start_time',
            help='The start time for selecting results between a time range.')
    @option('-et', '--end_time',
            help='The end time for selecting results between a time range.')
    @option('-i', '--include_child_accounts', is_flag=True,
            help='If the results should include entries from child accounts.')
    @option('-ev', '--event_types', type=Choice(EVENT_TYPES),
            help='Limit the results to particular event types.')
    @option('-r', '--result', type=Choice(('SUCCESS', 'FAILURE')),
            help='If the result was successful or not.')
    @option('-pi', '--principal_id',
            help='The principal id, e.g. user or api key id.')
    @option('-ci', '--correlation_id',
            help='The correlation id, e.g. id of audit event to surface related events.')
    @option('-si', '--subject_id',
            help='The subject id, e.g. id of audit subject '
                 '(connection, network, etc.) to surface related events.')
    @option('-su', '--subject_type', type=Choice(SUBJECT_TYPES),
            help='The subject type')
    @option('-ics', '--include_child_subjects', is_flag=True,
            help='If the results should include entries from child subjects from the subject id.')
    def query(self, page_number=None, page_size=None, sort=None, sort_direction=None,
              start_time=None, end_time=None, include_child_accounts=None, event_types=None,
              result=None, principal_id=None, ip_address=None, correlation_id=None, subject_id=None,
              subject_type=None, include_child_subjects=None):
        """
        Query the audit log for this account.

        \f
        :param int page_number:
        :param int page_size:
        :param str sort:
        :param str sort_direction:
        :param str start_time: formatted as 'YYYY-MM-DDT00:00:00.000Z'
        :param str end_time: formatted as 'YYYY-MM-DDT00:00:00.000Z'
        :param bool include_child_accounts:
        :param list[str] event_types:
        :param str result:
        :param str principal_id:
        :param str ip_address:
        :param str correlation_id:
        :param str subject_id:
        :param str subject_type:
        :param bool include_child_subjects:
        :rtype: Page[AuditEntry]
        :raises: .exception.ClientHttpError
        """
        params = {
            'pageNumber': page_number,
            'pageSize': page_size,
            'sort': sort,
            'sortDirection': sort_direction,
            'startTime': format_date(start_time),
            'endTime': format_date(end_time),
            'includeChildAccounts': include_child_accounts,
            'eventTypes': event_types,
            'result': result,
            'principalId': principal_id,
            'ipAddress': ip_address,
            'correlationId': correlation_id,
            'subjectId': subject_id,
            'subjectType': subject_type,
            'includeChildSubjects': include_child_subjects
        }
        return self.__call__('get', 'auditLog', params=params)
