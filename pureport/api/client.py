# -*- coding: utf-8 -*-
from click import Choice, argument, option
from enum import Enum
from logging import basicConfig, getLogger
from os.path import exists, expanduser
from os import getenv
from yaml import safe_load

from ..cli.util import JSON
from ..exception.api import (
    ClientHttpException,
    ConnectionOperationFailedException,
    ConnectionOperationTimeoutException,
    MissingAccessTokenException,
    NotFoundException
)
from ..util.api import PureportSession
from ..util.date import format_date
from ..util.decorators import retry

__docformat__ = 'reStructuredText'

basicConfig()
logger = getLogger('pureport.api.client')

API_URL = "https://api.pureport.com"
API_CONFIG_PATH = expanduser('~/.pureport/credentials.yml')
ENVIRONMENT_API_URL = 'PUREPORT_API_URL'
ENVIRONMENT_API_KEY = 'PUREPORT_API_KEY'
ENVIRONMENT_API_SECRET = 'PUREPORT_API_SECRET'
ENVIRONMENT_API_PROFILE = 'PUREPORT_API_PROFILE'

"""
TODO(mtraynham): These aliases are simply for documentation.  Maybe in the future we'll extend them
to be fully documented or somehow self documented.
"""
Link = dict
Account = dict
AccountBilling = dict
AccountConsent = dict
AccountInvite = dict
AccountMember = dict
AccountPermissions = dict
AccountRole = dict
AuditEntry = dict
APIKey = dict
BGPRoute = dict
CloudRegion = dict
CloudService = dict
Connection = dict
ConnectionTimeEgressIngress = dict
ConnectivityByGateway = dict
DateFilter = dict
Gateway = dict
Facility = dict
Location = dict
Network = dict
NetworkConnectionEgressIngress = dict
NetworkInvoice = dict
NetworkTimeUsage = dict
Page = dict
Port = dict
Option = dict
SupportedConnection = dict
SupportedPort = dict
Task = dict
UsageByConnectionAndTimeOptions = dict
UsageByConnectionOptions = dict
UsageByNetworkAndTimeOptions = dict


def paginate(client_fun, *args, **kwargs):
    """
    Given a client function that supports the page_size and page_number
    keyword arguments for pagination, this generator will yield all results
    from that function.
    :param function client_fun:
    :rtype: Iterator
    """
    resp = client_fun(*args, **kwargs)
    yield from resp['content']
    total_elements = resp['totalElements']
    page_size = resp['pageSize']
    page_number = resp['pageNumber'] + 1
    if 'page_number' in kwargs:
        kwargs.pop('page_number')
    while page_number * page_size < total_elements:
        resp = client_fun(*args, page_number=page_number, **kwargs)
        yield from resp['content']
        page_number = resp['pageNumber'] + 1


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


class Client(object):
    def __init__(self, base_url=None,
                 key=None, secret=None,
                 access_token=None, profile=None,
                 session=None):
        """
        Client for the Pureport ReST API
        This client is a thin wrapper around :module:`requests`.
        All API methods return a :class:`requests.Response` object.  It's up to the user
        to handle exceptions thrown by the API in the form of bad error codes.
        :param str base_url: a base url for the client
        :param str key: the key to use for login
        :param str secret: the secret to user for login
        :param str access_token: the access token obtained externally for an API key
        :param str profile: the pureport profile to use when using credentials from a file
        :param PureportSession session: a session variable for testing
        """
        # Storing the base_url for compatibility, for usage in `login`.
        # We used to create the client with the base_url and then login with
        # credentials.  This `base_url` would have been "forgotten" and reverted
        # back to using the PROD API_URL, but if we store it and use this as the default,
        # then it works exactly as it did before.
        self.__base_url = base_url if base_url is not None else API_URL
        self.__session = session if session else PureportSession(self.__base_url)
        try:
            # Attempt login with the parameters provided.  Unlike above,
            # we are passing None for base_url by default to prevent cases
            # where environment credentials are different from the passed in base_url.
            self.login(key, secret, access_token, profile, base_url)
        except MissingAccessTokenException:
            pass
        except ClientHttpException as e:
            logger.exception('There was an attempt to authenticate with '
                             'Pureport, but it failed.', e)

    @staticmethod
    def to_link(standard_object, title):
        """
        Many objects from the ReST API have reference to other objects that can
        also be retrieved from the ReST API.  That reference is typically a Link object.
        This function converts a standard API object to a Link.
        :param dict standard_object: the object to be converted to a link
        :param str title: an optional title value to give this object
        :rtype: Link
        """
        return {
            'id': standard_object['id'],
            'href': standard_object['href'],
            'title': title,
        }

    @staticmethod
    def __get_file_based_credentials(profile=None):
        if exists(API_CONFIG_PATH):
            with open(API_CONFIG_PATH) as f:
                config = safe_load(f)
                if 'profiles' in config:
                    profiles = config['profiles']
                    potential_profiles = [
                        profile,
                        getenv(ENVIRONMENT_API_PROFILE),
                        config['current_profile'] if 'current_profile' in config else None,
                        'default'
                    ]
                    for potential_profile in potential_profiles:
                        if potential_profile is not None and potential_profile in profiles:
                            return profiles[potential_profile]
        return None

    def login(self, key=None, secret=None, access_token=None, profile=None, api_url=None):
        """
        Login to Pureport ReST API with the specified key and secret or
        pass in a previously obtained access_token.
        This stores the access token on this client instance's session for usage.
        :param str key: the key to use for login
        :param str secret: the secret to user for login
        :param str access_token: the access token obtained externally for an API key
        :param str profile: the pureport profile to use when using credentials from a file
        :param str api_url: the api base url
        :returns: the obtained access_token
        :rtype: str
        :raises: .exception.ClientHttpException
        :raises: .exception.MissingAccessTokenException
        """
        file_credentials = Client.__get_file_based_credentials(profile)
        # Update api base_url
        base_url = self.__base_url
        if api_url is not None:
            base_url = api_url
        elif getenv(ENVIRONMENT_API_URL) is not None:
            base_url = getenv(ENVIRONMENT_API_URL)
        elif file_credentials is not None and 'api_url' in file_credentials:
            base_url = file_credentials['api_url']
        self.__base_url = base_url
        self.__session._base_url = base_url
        # Update auth token
        if access_token is not None:
            self.__session.set_access_token(access_token)
            return access_token
        elif key is not None and secret is not None:
            return self.__session.login(key, secret)
        elif getenv(ENVIRONMENT_API_KEY) is not None and getenv(ENVIRONMENT_API_SECRET) is not None:
            return self.__session.login(getenv(ENVIRONMENT_API_KEY), getenv(ENVIRONMENT_API_SECRET))
        elif file_credentials is not None and 'api_key' in file_credentials and 'api_secret' in file_credentials:
            return self.__session.login(file_credentials['api_key'],
                                        file_credentials['api_secret'])
        raise MissingAccessTokenException()

    def open_api(self):
        """
        Get's the open api documentation
        :rtype: dict
        """
        return self.__session.get('/openapi.json').json()

    @property
    def accounts(self):
        """
        The accounts client
        \f
        :rtype: Client.AccountsClient
        """
        return self.AccountsClient(self.__session)

    @property
    def cloud_regions(self):
        """
        The cloud regions client
        \f
        :rtype: Client.CloudRegionsClient
        """
        return Client.CloudRegionsClient(self.__session)

    @property
    def cloud_services(self):
        """
        The cloud services client
        \f
        :rtype: Client.CloudServicesClient
        """
        return Client.CloudServicesClient(self.__session)

    @property
    def connections(self):
        """
        The connections client
        \f
        :rtype: Client.ConnectionsClient
        """
        return Client.ConnectionsClient(self.__session)

    @property
    def facilities(self):
        """
        The facilities client
        \f
        :rtype: Client.FacilitiesClient
        """
        return Client.FacilitiesClient(self.__session)

    @property
    def gateways(self):
        """
        The gateways client
        \f
        :rtype: Client.GatewaysClient
        """
        return Client.GatewaysClient(self.__session)

    @property
    def locations(self):
        """
        The locations client
        \f
        :rtype: Client.LocationsClient
        """
        return Client.LocationsClient(self.__session)

    @property
    def networks(self):
        """
        The networks client
        \f
        :rtype: Client.NetworksClient
        """
        return Client.NetworksClient(self.__session)

    @property
    def options(self):
        """
        The options client
        \f
        :rtype: Client.OptionsClient
        """
        return Client.OptionsClient(self.__session)

    @property
    def ports(self):
        """
        The ports client
        \f
        :rtype: Client.PortsClient
        """
        return Client.PortsClient(self.__session)

    @property
    def supported_connections(self):
        """
        The supported connections client
        \f
        :rtype: Client.SupportedConnectionsClient
        """
        return Client.SupportedConnectionsClient(self.__session)

    @property
    def tasks(self):
        """
        The tasks client
        \f
        :rtype: Client.TasksClient
        """
        return Client.TasksClient(self.__session)

    class AccountsClient(object):
        def __init__(self, session):
            """
            The Accounts client
            :param RelativeSession session:
            """
            self.__session = session

        @option('-i', '--ids', multiple=True,
                help='Find a particular set of accounts by their ids.')
        @option('-p', '--parent_id', help='Find all children accounts of a single parent account.')
        @option('-n', '--name', help='Search for accounts by their name.')
        @option('-l', '--limit', type=int, help='Limit the number of results.')
        def list(self, ids=None, parent_id=None, name=None, limit=None):
            """
            Get a list of all accounts.
            \f
            :param list[str] ids: a list of account ids to find
            :param str parent_id: a parent account id
            :param str name: a name for lowercase inter-word checking
            :param int limit: the max number to return
            :rtype: list[Account]
            :raises: .exception.HttpClientException
            """
            return self.__session.get(
                '/accounts',
                params={
                    'ids': ids,
                    'parentId': parent_id,
                    'name': name,
                    'limit': limit
                }).json()

        @argument('account_id')
        def get(self, account_id):
            """
            Get an account by its id.
            \f
            :param str account_id: the account id
            :rtype: Account
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s' % account_id).json()

        @argument('account', type=JSON)
        def create(self, account):
            """
            Create an account.
            \f
            :param Account account: the account object
            :rtype: Account
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts', json=account).json()

        @argument('account', type=JSON)
        def update(self, account):
            """
            Update an account.
            \f
            :param Account account: the account object
            :rtype: Account
            :raises: .exception.HttpClientException
            """
            return self.__session.put('/accounts/%s' % account['id'], json=account).json()

        @argument('account_id')
        def delete(self, account_id):
            """
            Delete an account.
            \f
            :param str account_id: the account id
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/accounts/%s' % account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def api_keys(self, account_id):
            """
            The account api keys client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountAPIKeysClient
            """
            return Client.AccountAPIKeysClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def audit_log(self, account_id):
            """
            The account audit log client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountAuditLogClient
            """
            return Client.AccountAuditLogClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def billing(self, account_id):
            """
            The account billing client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountBillingClient
            """
            return Client.AccountBillingClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def connections(self, account_id):
            """
            The account connections client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountConnectionsClient
            """
            return Client.AccountConnectionsClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def consent(self, account_id):
            """
            The account consent client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountConsentClient
            """
            return Client.AccountConsentClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def invites(self, account_id):
            """
            The account invites client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountInvitesClient
            """
            return Client.AccountInvitesClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def invoices(self, account_id):
            """
            The account invoices client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountInvoicesClient
            """
            return Client.AccountInvoicesClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def members(self, account_id):
            """
            The account members client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountMembersClient
            """
            return Client.AccountMembersClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def metrics(self, account_id):
            """
            The account metrics client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountMetricsClient
            """
            return Client.AccountMetricsClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def networks(self, account_id):
            """
            The account networks client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountNetworksClient
            """
            return Client.AccountNetworksClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def permissions(self, account_id):
            """
            The account permissions client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountPermissionsClient
            """
            return Client.AccountPermissionsClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def ports(self, account_id):
            """
            The account ports client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountPortsClient
            """
            return Client.AccountPortsClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def roles(self, account_id):
            """
            The account roles client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountRolesClient
            """
            return Client.AccountRolesClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def supported_connections(self, account_id):
            """
            The account supported connections client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountSupportedConnectionsClient
            """
            return Client.AccountSupportedConnectionsClient(self.__session, account_id)

        @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
        def supported_ports(self, account_id):
            """
            The account supported ports client
            \f
            :param str account_id: the account id
            :rtype: Client.AccountSupportedPortsClient
            """
            return Client.AccountSupportedPortsClient(self.__session, account_id)

    class AccountAPIKeysClient(object):
        def __init__(self, session, account_id):
            """
            The Account API Keys client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def list(self):
            """
            Get a list of all API keys for an account.
            \f
            :rtype: list[APIKey]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/apikeys' % self.__account_id).json()

        @argument('api_key_key')
        def get(self, api_key_key):
            """
            Get an account's API Key with the provided API Key key.
            \f
            :param str api_key_key: the key of an API Key
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/apikeys/%s' % (self.__account_id, api_key_key)).json()

        @argument('api_key', type=JSON)
        def create(self, api_key):
            """
            Create an API Key for the provided account.
            \f
            :param APIKey api_key: the APIKey object
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/apikeys' % self.__account_id, json=api_key).json()

        @argument('api_key', type=JSON)
        def update(self, api_key):
            """
            Update an API Key for the provided account.
            \f
            :param APIKey api_key: the APIKey object
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.put(
                '/accounts/%s/apikeys/%s' % (self.__account_id, api_key['key']),
                json=api_key
            ).json()

        @argument('api_key_key')
        def delete(self, api_key_key):
            """
            Delete an API Key from the provided account.
            \f
            :param str api_key_key: the APIKey key name
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/accounts/%s/apikeys/%s' % (self.__account_id, api_key_key))

    class AccountAuditLogClient(object):
        def __init__(self, session, account_id):
            """
            The Account Audit Log client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        @option('-pn', '--page_number', type=int, help='The page number for pagination.')
        @option('-ps', '--page_size', type=int, help='The page size for pagination.')
        @option('-s', '--sort', type=Choice(['timestamp', 'eventType', 'subjectType',
                                             'ipAddress', 'userAgent', 'source', 'result']),
                help='How should the data be sorted.')
        @option('-sd', '--sort_direction', type=Choice(['ASC', 'DESC']),
                help='The direction the results will be sorted.')
        @option('-st', '--start_time',
                help='The start time for selecting results between a time range.')
        @option('-et', '--end_time',
                help='The end time for selecting results between a time range.')
        @option('-i', '--include_child_accounts', is_flag=True,
                help='If the results should include entries from child accounts.')
        @option('-ev', '--event_types', type=Choice(['USER_LOGIN', 'USER_FORGOT_PASSWORD', 'API_LOGIN',
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
                                                     'TASK_UPDATE', 'TASK_DELETE']),
                help='Limit the results to particular event types.')
        @option('-r', '--result', type=Choice(['SUCCESS', 'FAILURE']),
                help='If the result was successful or not.')
        @option('-pi', '--principal_id',
                help='The principal id, e.g. user or api key id.')
        @option('-ci', '--correlation_id',
                help='The correlation id, e.g. id of audit event to surface related events.')
        @option('-si', '--subject_id',
                help='The subject id, e.g. id of audit subject '
                     '(connection, network, etc.) to surface related events.')
        @option('-su', '--subject_type', type=Choice(['ACCOUNT', 'CONNECTION', 'NETWORK', 'USER',
                                                      'USER_DOMAIN', 'ROLE', 'API_KEY', 'GATEWAY',
                                                      'NOTIFICATION', 'ACCOUNT_INVITE', 'ACCOUNT_BILLING',
                                                      'PORT', 'ACCOUNT_MEMBER', 'TASK']),
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
            :raises: .exception.HttpClientException
            """
            return self.__session.get(
                '/accounts/%s/auditLog' % self.__account_id,
                params={
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
            ).json()

    class AccountBillingClient(object):
        def __init__(self, session, account_id):
            """
            The Account Billing client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def get(self):
            """
            Get the billing information for the provided account.  This does not check parent
            accounts.
            \f
            If you want to find if any billing is configured, instead use
            :func:`Client.AccountBillingClient.get_configured`.
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/billing' % self.__account_id).json()

        def get_configured(self):
            """
            Get the billing information for the provided account.  This returns the billing info of the
            account or any parent account.
            \f
            :rtype: bool
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/billing/configured' % self.__account_id).json()

        @argument('account_billing', type=JSON)
        def create(self, account_billing):
            """
            Add a payment method to provided account.
            \f
            :param AccountBilling account_billing: the AccountBilling object
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/billing' % self.__account_id, json=account_billing).json()

        @argument('account_billing', type=JSON)
        def update(self, account_billing):
            """
            Update the payment method for the provided account.
            \f
            :param AccountBilling account_billing: the AccountBilling object
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.put('/accounts/%s/billing' % self.__account_id, json=account_billing).json()

        def delete(self):
            """
            Delete the current AccountBilling object from the account if it exists.
            \f
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/accounts/%s/billing' % self.__account_id)

    class AccountConnectionsClient(object):
        def __init__(self, session, account_id):
            """
            The Account Connections client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def list(self):
            """
            Get all connections for the provided account.
            \f
            :rtype: list[Connection]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/connections' % self.__account_id).json()

    class AccountConsentClient(object):
        def __init__(self, session, account_id):
            """
            The Account Consent Client client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def get(self):
            """
            Get the consent information for the provided account.
            \f
            :rtype: AccountConsent
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/consent' % self.__account_id).json()

        def accept(self):
            """
            Accept consent for the provided account.
            \f
            :rtype: AccountConsent
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/consent' % self.__account_id).json()

    class AccountInvitesClient(object):
        def __init__(self, session, account_id):
            """
            The Account Invites client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def list(self):
            """
            Get all invites for the provided account.
            \f
            :rtype: list[AccountInvite]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/invites' % self.__account_id).json()

        @argument('invite_id')
        def get(self, invite_id):
            """
            Get an account's invite with the provided account invite id.
            \f
            :param str invite_id: the account invite id
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/invites/%s' % (self.__account_id, invite_id)).json()

        @argument('invite', type=JSON)
        def create(self, invite):
            """
            Create an account invite using the provided account.
            \f
            :param AccountInvite invite: the account invite object
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/invites' % self.__account_id, json=invite).json()

        @argument('invite', type=JSON)
        def update(self, invite):
            """
            Update an account invite using the provided account.
            \f
            :param AccountInvite invite: the account invite object
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.put(
                '/accounts/%s/invites/%s' % (self.__account_id, invite['id']),
                json=invite
            ).json()

        @argument('invite_id')
        def delete(self, invite_id):
            """
            Delete an account invite using the provided account.
            \f
            :param str invite_id: the account invite id
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/accounts/%s/invites/%s' % (self.__account_id, invite_id))

    class AccountInvoicesClient(object):
        def __init__(self, session, account_id):
            """
            The Account Invoices client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        @argument('invoice_filter', type=JSON)
        def list(self, invoice_filter):
            """
            List all invoices for an account.
            \f
            :param dict invoice_filter: a filter object that matches Stripe's invoice filter
                https://stripe.com/docs/api/invoices/list
            :rtype: list[NetworkInvoice]
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/invoices' % self.__account_id, json=invoice_filter).json()

        def list_upcoming(self):
            """
            List all upcoming invoices for an account.
            \f
            :rtype: list[NetworkInvoice]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/invoices/upcoming' % self.__account_id).json()

    class AccountMembersClient(object):
        def __init__(self, session, account_id):
            """
            The Account Members client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def list(self):
            """
            List all members for the provided account.
            \f
            :rtype: list[AccountMember]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/members' % self.__account_id).json()

        @argument('user_id')
        def get(self, user_id):
            """
            Get a member by their user id for the provided account.
            \f
            :param str user_id: a user id
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/members/%s' % (self.__account_id, user_id)).json()

        @argument('member', type=JSON)
        def create(self, member):
            """
            Create an member for the provided account.
            \f
            It may be better to use the :func:`Client.AccountInvite.post` if the
            user does or does not exist.
            :param AccountMember member:  the account member object
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/members' % self.__account_id, json=member).json()

        @argument('member', type=JSON)
        def update(self, member):
            """
            Update a member for the provided account.
            \f
            :param AccountMember member:  the account member object
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.put(
                '/accounts/%s/members/%s' % (self.__account_id, member['user']['id']),
                json=member
            ).json()

        @argument('user_id')
        def delete(self, user_id):
            """
            Delete a member from the provided account.
            \f
            :param str user_id: a user id
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/accounts/%s/members/%s' % (self.__account_id, user_id))

    class AccountMetricsClient(object):
        def __init__(self, session, account_id):
            """
            The Account Networks client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        @argument('options', type=JSON)
        def usage_by_connection(self, options):
            """
            Retrieve egress/ingress total usage by connections
            \f
            :param UsageByConnectionOptions options:
            :rtype: list[NetworkConnectionEgressIngress]
            :raises: .exception.HttpClientException
            """
            return self.__session.post(
                '/accounts/%s/metrics/usageByConnection' % self.__account_id,
                json=options
            ).json()

        @argument('options', type=JSON)
        def usage_by_connection_and_time(self, options):
            """
            Retrieve usage by a single connection over time
            \f
            :param UsageByConnectionAndTimeOptions options:
            :rtype: list[ConnectionTimeEgressIngress]
            :raises: .exception.HttpClientException
            """
            return self.__session.post(
                '/accounts/%s/metrics/usageByConnectionAndTime' % self.__account_id,
                json=options
            ).json()

        @argument('options', type=JSON)
        def usage_by_network_and_time(self, options):
            """
            Retrieve usage of networks over time
            \f
            :param UsageByNetworkAndTimeOptions options:
            :rtype: list[NetworkTimeUsage]
            :raises: .exception.HttpClientException
            """
            return self.__session.post(
                '/accounts/%s/metrics/usageByNetworkAndTime' % self.__account_id,
                json=options
            ).json()

    class AccountNetworksClient(object):
        def __init__(self, session, account_id):
            """
            The Account Networks client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def list(self):
            """
            Get all networks for the provided account.
            \f
            :rtype: list[Network]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/networks' % self.__account_id).json()

        @argument('network', type=JSON)
        def create(self, network):
            """
            Create a network for the provided account.
            \f
            :param Network network:  the network object
            :rtype: Network
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/networks' % self.__account_id, json=network).json()

    class AccountPermissionsClient(object):
        def __init__(self, session, account_id):
            """
            The Account Permissions client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def get(self):
            """
            Get all permissions for the provided account.  This returns the effect permission set for the
            currently logged in API Key.
            \f
            :rtype: AccountPermissions
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/permissions' % self.__account_id).json()

    class AccountPortsClient(object):
        def __init__(self, session, account_id):
            """
            The Account Ports client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def list(self):
            """
            Get all ports for the provided account.
            \f
            :rtype: list[Port]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/ports' % self.__account_id).json()

        @argument('port', type=JSON)
        def create(self, port):
            """
            Create a port for the provided account.
            \f
            :param Port port:  the port object
            :rtype: Port
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/ports' % self.__account_id, json=port).json()

    class AccountRolesClient(object):
        def __init__(self, session, account_id):
            """
            The Account Roles client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def list(self):
            """
            List all roles for the provided account.
            \f
            :rtype: list[AccountRole]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/roles' % self.__account_id).json()

        @argument('role_id')
        def get(self, role_id):
            """
            Get a role by its id for the provided account.
            \f
            :param str role_id: the role id
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/roles/%s' % (self.__account_id, role_id)).json()

        @argument('role', type=JSON)
        def create(self, role):
            """
            Create a role for the provided account.
            \f
            :param AccountRole role: the account role object
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/roles' % self.__account_id, json=role).json()

        @argument('role', type=JSON)
        def update(self, role):
            """
            Update a role for the provided account.
            \f
            :param AccountRole role: the account role object
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.put('/accounts/%s/roles/%s' % (self.__account_id, role['id']), json=role).json()

        @argument('role_id')
        def delete(self, role_id):
            """
            Update a role for the provided account.
            \f
            :param str role_id: the role id
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/accounts/%s/roles/%s' % (self.__account_id, role_id))

    class AccountSupportedConnectionsClient(object):
        def __init__(self, session, account_id):
            """
            The Account Supported Connections client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        def list(self):
            """
            Get the supported connections for the provided account.
            \f
            :rtype: list[SupportedConnection]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/supportedConnections' % self.__account_id).json()

    class AccountSupportedPortsClient(object):
        def __init__(self, session, account_id):
            """
            The Account Supported Ports client
            :param RelativeSession session:
            :param str account_id:
            """
            self.__session = session
            self.__account_id = account_id

        @argument('facility_id')
        def list(self, facility_id):
            """
            Get the supported ports for the provided account.
            \f
            :param str facility_id: the facility id to list supported ports for
            :rtype: list[SupportedPort]
            :raises: .exception.HttpClientException
            """
            return self.__session.get(
                '/accounts/%s/supportedPorts' % self.__account_id,
                params={'facility': facility_id}
            ).json()

    class CloudRegionsClient(object):
        def __init__(self, session):
            """
            The Cloud Regions client
            :param RelativeSession session:
            """
            self.__session = session

        def list(self):
            """
            Get all available cloud regions.
            \f
            :rtype: list[CloudRegion]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/cloudRegions').json()

        @argument('cloud_region_id')
        def get(self, cloud_region_id):
            """
            Get the cloud region with the provided cloud region id.
            \f
            :param str cloud_region_id: the cloud region id
            :rtype: CloudRegion
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/cloudRegions/%s' % cloud_region_id).json()

    class CloudServicesClient(object):
        def __init__(self, session):
            """
            The Cloud Services client
            :param RelativeSession session:
            """
            self.__session = session

        def list(self):
            """
            Get all available cloud services.
            \f
            :rtype: list[CloudRegion]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/cloudServices').json()

        @argument('cloud_service_id')
        def get(self, cloud_service_id):
            """
            Get the cloud service with the provided cloud service id.
            \f
            :param str cloud_service_id: the cloud service id
            :rtype: CloudRegion
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/cloudServices/%s' % cloud_service_id).json()

    class ConnectionsClient(object):
        def __init__(self, session):
            """
            The Connections client
            :param RelativeSession session:
            """
            self.__session = session

        @staticmethod
        @retry(ConnectionOperationTimeoutException)
        def get_connection_until_state(session, connection_id, expected_state, failed_states):
            """
            Retrieve a connection until it enters a certain state using an exponential backoff
            :param RelativeSession session: a :class:`Client`'s relative session
            :param str connection_id: the connection id
            :param ConnectionState|str expected_state: the expected state
            :param list[ConnectionState|str] failed_states: a list of failed states that instead
            :rtype: Connection
            :raises: .exception.ConnectionOperationTimeoutException
            :raises: .exception.ConnectionOperationFailedException
            """
            connection = session.get('/connections/%s' % connection_id).json()
            if ConnectionState[connection['state']] in failed_states:
                raise ConnectionOperationFailedException(connection=connection)
            if ConnectionState[connection['state']] != expected_state:
                raise ConnectionOperationTimeoutException(connection=connection)
            return connection

        @staticmethod
        @retry(ConnectionOperationTimeoutException)
        def __get_connection_until_not_found(session, connection_id, failed_states):
            """
            Retrieve a connection until it no longer exists using an exponential backoff
            :param RelativeSession session: a :class:`Client`'s relative session
            :param str connection_id: the connection id
            :param list[ConnectionState|str] failed_states: a list of failed states that instead
            :raises: .exception.ConnectionOperationTimeoutException
            :raises: .exception.ConnectionOperationFailedException
            """
            try:
                connection = session.get('/connections/%s' % connection_id).json()
            except NotFoundException:
                return
            if ConnectionState[connection['state']] in failed_states:
                raise ConnectionOperationFailedException(connection=connection)
            raise ConnectionOperationTimeoutException(connection=connection)

        @argument('connection_id')
        def get(self, connection_id):
            """
            Get a connection with the provided connection id.
            \f
            :param str connection_id: the connection id
            :rtype: Connection
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/connections/%s' % connection_id).json()

        @argument('connection', type=JSON)
        @option('-w', '--wait_until_active', is_flag=True,
                help='Wait until the connection is active.')
        def update(self, connection, wait_until_active=False):
            """
            Updated a connection.
            \f
            :param Connection connection: the connection object
            :param bool wait_until_active: wait until the connection is active using a backoff retry
            :rtype: Connection
            :raises: .exception.HttpClientException
            :raises: .exception.ConnectionOperationTimeoutException
            :raises: .exception.ConnectionOperationFailedException
            """
            connection = self.__session.put('/connections/%s' % connection['id'], json=connection).json()
            if wait_until_active:
                return Client.ConnectionsClient.get_connection_until_state(
                    self.__session,
                    connection['id'],
                    ConnectionState.ACTIVE,
                    [ConnectionState.FAILED_TO_UPDATE]
                )
            else:
                return connection

        @argument('connection_id')
        @option('-w', '--wait_until_deleted', is_flag=True,
                help='Wait until the connection is deleted.')
        def delete(self, connection_id, wait_until_deleted=False):
            """
            Delete a connection.
            \f
            :param str connection_id: the connection id
            :param bool wait_until_deleted: wait until the connection is deleted using a backoff retry
            :raises: .exception.HttpClientException
            :raises: .exception.ConnectionOperationTimeoutException
            :raises: .exception.ConnectionOperationFailedException
            """
            self.__session.delete('/connections/%s' % connection_id)
            if wait_until_deleted:
                Client.ConnectionsClient.__get_connection_until_not_found(
                    self.__session,
                    connection_id,
                    [ConnectionState.FAILED_TO_DELETE]
                )

        @argument('connection_id')
        def get_tasks(self, connection_id):
            """
            Get the tasks for a connection.
            \f
            :param str connection_id: the connection id
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/connections/%s/tasks' % connection_id).json()

        @argument('connection_id')
        @argument('task', type=JSON)
        def create_task(self, connection_id, task):
            """
            Create a task for a connection.
            \f
            :param str connection_id: the connection id
            :param Task task: the task
            :rtype: Task
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/connections/%s/tasks' % connection_id, json=task).json()

    class FacilitiesClient(object):
        def __init__(self, session):
            """
            The FacilitiesClient client
            :param RelativeSession session:
            """
            self.__session = session

        def list(self):
            """
            Get all available facilities.
            \f
            :rtype: list[Facility]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/facilities').json()

        @argument('facility_id')
        def get(self, facility_id):
            """
            Get a facility with the provided facility id.
            \f
            :param str facility_id: the facility id
            :rtype: Facility
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/facilities/%s' % facility_id).json()

    class GatewaysClient(object):
        def __init__(self, session):
            """
            The GatewaysClient client
            :param RelativeSession session:
            """
            self.__session = session

        @argument('gateway_id')
        def get(self, gateway_id):
            """
            Get a gateway by its id
            \f
            :param str gateway_id: the gateway id
            :rtype: Gateway
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s' % gateway_id).json()

        @argument('gateway_id')
        def get_bgp_routes(self, gateway_id):
            """
            Get the bgp routes for a gateway.
            \f
            :param str gateway_id: the gateway id
            :rtype: list[BGPRoute]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/bgpRoutes' % gateway_id).json()

        @argument('gateway_id')
        @argument('date_filter', type=JSON)
        def get_connectivity_over_time(self, gateway_id, date_filter):
            """
            Get the connectivity details for a gateway by id over time.
            \f
            :param str gateway_id: the gateway id
            :param DateFilter date_filter: a date filter consisting of 'gt', 'lt', 'gte', 'lte' properties
            :rtype: list[ConnectivityByGateway]
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/gateways/%s/metrics/connectivity' % gateway_id, json=date_filter).json()

        @argument('gateway_id')
        def get_latest_connectivity(self, gateway_id):
            """
            Get the current connectivity details for a gateway by id.
            \f
            :param str gateway_id: the gateway id
            :rtype: ConnectivityByGateway
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/metrics/connectivity/current' % gateway_id).json()

        @argument('gateway_id')
        def get_tasks(self, gateway_id):
            """
            Get the tasks for a gateway.
            \f
            :param str gateway_id: the gateway id
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/tasks' % gateway_id).json()

        @argument('gateway_id')
        @argument('task', type=JSON)
        def create_task(self, gateway_id, task):
            """
            Create a task for a gateway.
            \f
            :param str gateway_id: the gateway id
            :param Task task: the task
            :rtype: Task
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/gateways/%s/tasks' % gateway_id, json=task).json()

    class LocationsClient(object):
        def __init__(self, session):
            """
            The Locations client
            :param RelativeSession session:
            """
            self.__session = session

        def list(self):
            """
            Get all available locations.
            \f
            :rtype: list[Location]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/locations').json()

        @argument('location_id')
        def get(self, location_id):
            """
            Get a location with the provided location id.
            \f
            :param str location_id: the location id
            :rtype: Location
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/locations/%s' % location_id).json()

    class NetworksClient(object):
        def __init__(self, session):
            """
            The Networks client
            :param RelativeSession session:
            """
            self.__session = session

        @argument('network_id')
        def get(self, network_id):
            """
            Get a network with the provided network id.
            \f
            :param str network_id: the network id
            :rtype: Network
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/networks/%s' % network_id).json()

        @argument('network', type=JSON)
        def update(self, network):
            """
            Update a network.
            \f
            :param Network network: the network object
            :rtype: Network
            :raises: .exception.HttpClientException
            """
            return self.__session.put('/networks/%s' % network['id'], json=network).json()

        @argument('network_id')
        def delete(self, network_id):
            """
            Delete a network.
            \f
            :param str network_id: the network id
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/networks/%s' % network_id)

        @option('-n', '--network_id', envvar='PUREPORT_NETWORK_ID', required=True)
        def connections(self, network_id):
            """
            Get the account network connections client using the provided account.
            \f
            :param str network_id: the network id
            :rtype: Client.NetworkConnectionsClient
            """
            return Client.NetworkConnectionsClient(self.__session, network_id)

    class NetworkConnectionsClient(object):
        def __init__(self, session, network_id):
            """
            The Network Connections client
            :param RelativeSession session:
            :param str network_id:
            """
            self.__session = session
            self.__network_id = network_id

        def list(self):
            """
            Get all connections for the provided network.
            \f
            :rtype: list[Connection]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/networks/%s/connections' % self.__network_id).json()

        @argument('connection', type=JSON)
        @option('-w', '--wait_until_active', is_flag=True,
                help='Wait until the connection is active.')
        def create(self, connection, wait_until_active=False):
            """
            Create a connection for the provided network.
            \f
            :param Connection connection: the connect object
            :param bool wait_until_active: wait until the connection is active using a backoff retry
            :rtype: Connection
            :raises: .exception.HttpClientException
            :raises: .exception.ConnectionOperationTimeoutException
            :raises: .exception.ConnectionOperationFailedException
            """
            connection = self.__session.post('/networks/%s/connections' % self.__network_id, json=connection).json()
            if wait_until_active:
                return Client.ConnectionsClient.get_connection_until_state(
                    self.__session,
                    connection['id'],
                    ConnectionState.ACTIVE,
                    [ConnectionState.FAILED_TO_PROVISION]
                )
            else:
                return connection

    class OptionsClient(object):
        def __init__(self, session):
            """
            The Options client
            :param RelativeSession session:
            """
            self.__session = session

        @option('-t', '--types', multiple=True,
                help='A filter for the list of enumeration types')
        def list(self, types=None):
            """
            List all option objects provided by the API.  These are constant enumerations that are
            used for various parts of the API.  A optional set of **types** may be passed in
            to filter the response.
            \f
            :param list[str] types: a filter for the list of enumeration types
            :rtype: dict[str, list[Option]]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/options', params={'type': types}).json()

    class PortsClient(object):
        def __init__(self, session):
            """
            The Ports client
            :param RelativeSession session:
            """
            self.__session = session

        @argument('port_id')
        def get(self, port_id):
            """
            Get the port with the provided port id.
            \f
            :param str port_id: the port id
            :rtype: Port
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/ports/%s' % port_id).json()

        @argument('port_id')
        def get_accounts_using_port(self, port_id):
            """
            Get the accounts using the port with the provided port id.
            \f
            :param str port_id: the port id
            :rtype: list[Link]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/ports/%s/accounts' % port_id).json()

        @argument('port', type=JSON)
        def update(self, port):
            """
            Update a port.
            \f
            :param Port port: the port object
            :rtype: Port
            :raises: .exception.HttpClientException
            """
            return self.__session.put('/ports/%s' % port['id'], json=port).json()

        @argument('port_id')
        def delete(self, port_id):
            """
            Delete a port.
            \f
            :param str port_id: the port id
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/ports/%s' % port_id)

    class SupportedConnectionsClient(object):
        def __init__(self, session):
            """
            The Supported Connections client
            :param RelativeSession session:
            """
            self.__session = session

        @argument('supported_connection_id')
        def get(self, supported_connection_id):
            """
            Get the supported connection with the provided supported connection id.
            \f
            :param str supported_connection_id: the supported connection id
            :rtype: SupportedConnection
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/supportedConnections/%s' % supported_connection_id).json()

    class TasksClient(object):
        def __init__(self, session):
            """
            The Tasks client
            :param RelativeSession session:
            """
            self.__session = session

        @option('-s', '--state',
                type=Choice(['CREATED', 'RUNNING', 'COMPLETED', 'FAILED', 'DELETED']),
                help='The task state.')
        @option('-pn', '--page_number', type=int, help='The page number for pagination.')
        @option('-ps', '--page_size', type=int, help='The page size for pagination.')
        def list(self, state=None, page_number=None, page_size=None):
            """
            List all tasks.
            \f
            :param str state: find all tasks for a particular state
            :param int page_number: page number for pagination
            :param int page_size: page size for pagination
            :rtype: Page[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/tasks',
                                      params={
                                          'state': state,
                                          'pageNumber': page_number,
                                          'pageSize': page_size
                                      }).json()

        @argument('task_id')
        def get(self, task_id):
            """
            Get a task by it's id.
            \f
            :param str task_id: the task id
            :rtype: Task
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/tasks/%s' % task_id).json()
