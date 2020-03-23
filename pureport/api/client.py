# -*- coding: utf-8 -*-
from enum import Enum
from ..exception.api import \
    ConnectionOperationFailedException, \
    ConnectionOperationTimeoutException, \
    MissingAccessTokenException, \
    NotFoundException
from ..util.api import PureportSession
from ..util.decorators import retry

__docformat__ = 'reStructuredText'

API_URL = "https://api.pureport.com"

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
    def __init__(self, base_url=API_URL):
        """
        Client for the Pureport ReST API
        This client is a thin wrapper around :module:`requests`.
        All API methods return a :class:`requests.Response` object.  It's up to the user
        to handle exceptions thrown by the API in the form of bad error codes.
        :param str base_url: a base url for the client
        """
        self.__session = PureportSession(base_url)

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

    def login(self, key=None, secret=None, access_token=None):
        """
        Login to Pureport ReST API with the specified key and secret or
        pass in a previously obtained access_token.
        This stores the access token on this client instance's session for usage.
        :param str key: the key to use for login
        :param str secret: the secret to user for login
        :param str access_token: the access token obtained externally for an API key
        :returns: the obtained access_token
        :rtype: str
        :raises: .exception.ClientHttpException
        :raises: .exception.MissingAccessTokenException
        """
        if key is not None and secret is not None:
            return self.__session.login(key, secret)
        elif access_token is not None:
            self.__session.set_access_token(access_token)
            return access_token
        else:
            raise MissingAccessTokenException()

    @property
    def accounts(self):
        """
        The accounts client
        :rtype: Client.AccountsClient
        """
        return self.AccountsClient(self.__session)

    @property
    def cloud_regions(self):
        """
        The cloud regions client
        :rtype: Client.CloudRegionsClient
        """
        return Client.CloudRegionsClient(self.__session)

    @property
    def cloud_services(self):
        """
        The cloud services client
        :rtype: Client.CloudServicesClient
        """
        return Client.CloudServicesClient(self.__session)

    @property
    def connections(self):
        """
        The connections client
        :rtype: Client.ConnectionsClient
        """
        return Client.ConnectionsClient(self.__session)

    @property
    def facilities(self):
        """
        The facilities client
        :rtype: Client.FacilitiesClient
        """
        return Client.FacilitiesClient(self.__session)

    @property
    def gateways(self):
        """
        The gateways client
        :rtype: Client.GatewaysClient
        """
        return Client.GatewaysClient(self.__session)

    @property
    def locations(self):
        """
        The locations client
        :rtype: Client.LocationsClient
        """
        return Client.LocationsClient(self.__session)

    @property
    def networks(self):
        """
        The networks client
        :rtype: Client.NetworksClient
        """
        return Client.NetworksClient(self.__session)

    @property
    def options(self):
        """
        The options client
        :rtype: Client.OptionsClient
        """
        return Client.OptionsClient(self.__session)

    @property
    def ports(self):
        """
        The ports client
        :rtype: Client.PortsClient
        """
        return Client.PortsClient(self.__session)

    @property
    def supported_connections(self):
        """
        The supported connections client
        :rtype: Client.SupportedConnectionsClient
        """
        return Client.SupportedConnectionsClient(self.__session)

    @property
    def tasks(self):
        """
        The tasks client
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

        def list(self, ids=None, parent_id=None, name=None, limit=None):
            """
            Get a list of all accounts.
            :rtype: list[Account]
            :param list[str] ids: a list of account ids to find
            :param str parent_id: a parent account id
            :param str name: a name for lowercase inter-word checking
            :param int limit: the max number to return
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

        def get(self, account_id):
            """
            Get an account by its id.
            :param str account_id: the account id
            :rtype: Account
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s' % account_id).json()

        def create(self, account):
            """
            Create an account.
            :param Account account: the account object
            :rtype: Account
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts', json=account).json()

        def update(self, account):
            """
            Update an account.
            :param Account account: the account object
            :rtype: Account
            :raises: .exception.HttpClientException
            """
            return self.__session.put('/accounts/%s' % account['id'], json=account).json()

        def delete(self, account_id):
            """
            Delete an account.
            :param str account_id: the account id
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/accounts/%s' % account_id)

        def api_keys(self, account_id):
            """
            Get the account api keys client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountAPIKeysClient
            """
            return Client.AccountAPIKeysClient(self.__session, account_id)

        def audit_log(self, account_id):
            """
            Get the account audit log client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountAuditLogClient
            """
            return Client.AccountAuditLogClient(self.__session, account_id)

        def billing(self, account_id):
            """
            Get the account billing client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountBillingClient
            """
            return Client.AccountBillingClient(self.__session, account_id)

        def connections(self, account_id):
            """
            Get the account connections client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountConnectionsClient
            """
            return Client.AccountConnectionsClient(self.__session, account_id)

        def consent(self, account_id):
            """
            Get the account consent client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountConsentClient
            """
            return Client.AccountConsentClient(self.__session, account_id)

        def invites(self, account_id):
            """
            Get the account invites client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountInvitesClient
            """
            return Client.AccountInvitesClient(self.__session, account_id)

        def invoices(self, account_id):
            """
            Get the account invoices client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountInvoicesClient
            """
            return Client.AccountInvoicesClient(self.__session, account_id)

        def members(self, account_id):
            """
            Get the account members client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountMembersClient
            """
            return Client.AccountMembersClient(self.__session, account_id)

        def metrics(self, account_id):
            """
            Get the account metrics client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountMetricsClient
            """
            return Client.AccountMetricsClient(self.__session, account_id)

        def networks(self, account_id):
            """
            Get the account networks client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountNetworksClient
            """
            return Client.AccountNetworksClient(self.__session, account_id)

        def permissions(self, account_id):
            """
            Get the account permissions client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountPermissionsClient
            """
            return Client.AccountPermissionsClient(self.__session, account_id)

        def ports(self, account_id):
            """
            Get the account ports client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountPortsClient
            """
            return Client.AccountPortsClient(self.__session, account_id)

        def roles(self, account_id):
            """
            Get the account roles client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountRolesClient
            """
            return Client.AccountRolesClient(self.__session, account_id)

        def supported_connections(self, account_id):
            """
            Get the account supported connections client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountSupportedConnectionsClient
            """
            return Client.AccountSupportedConnectionsClient(self.__session, account_id)

        def supported_ports(self, account_id):
            """
            Get the account supported ports client using the provided account.
            :param str account_id: the account id
            :rtype: Client.AccountSupportedConnectionsClient
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
            :rtype: list[APIKey]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/apikeys' % self.__account_id).json()

        def get(self, api_key_key):
            """
            Get an account's API Key with the provided API Key key.
            :param str api_key_key: the key of an API Key
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/apikeys/%s' % (self.__account_id, api_key_key)).json()

        def create(self, api_key):
            """
            Create an API Key for the provided account.
            :param APIKey api_key: the APIKey object
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/apikeys' % self.__account_id, json=api_key).json()

        def update(self, api_key):
            """
            Update an API Key for the provided account.
            :param APIKey api_key: the APIKey object
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.put(
                '/accounts/%s/apikeys/%s' % (self.__account_id, api_key['key']),
                json=api_key
            ).json()

        def delete(self, api_key_key):
            """
            Delete an API Key from the provided account.
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

        def query(self, page_number=None, page_size=None, sort=None, sort_direction=None,
                  start_time=None, end_time=None, include_child_accounts=None, event_types=None,
                  result=None, principal_id=None, ip_address=None, correlation_id=None, subject_id=None,
                  subject_type=None):
            """
            Query the audit log for this account.
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
                    'startTime': start_time,
                    'endTime': end_time,
                    'includeChildAccounts': include_child_accounts,
                    'eventTypes': event_types,
                    'result': result,
                    'principalId': principal_id,
                    'ipAddress': ip_address,
                    'correlationId': correlation_id,
                    'subjectId': subject_id,
                    'subjectType': subject_type
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
            accounts.  If you want to find if any billing is configured, instead use
            :func:`Client.AccountBillingClient.get_configured`.
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/billing' % self.__account_id).json()

        def get_configured(self):
            """
            Get the billing information for the provided account.  This returns the billing info of the
            account or any parent account.
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/billing/configured' % self.__account_id).json()

        def create(self, account_billing):
            """
            Add a payment method to provided account.
            :param AccountBilling account_billing: the AccountBilling object
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/billing' % self.__account_id, json=account_billing).json()

        def update(self, account_billing):
            """
            Update the payment method for the provided account.
            :param AccountBilling account_billing: the AccountBilling object
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.put('/accounts/%s/billing' % self.__account_id, json=account_billing).json()

        def delete(self):
            """
            Delete the current AccountBilling object from the account if it exists.
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
            :rtype: AccountConsent
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/consent' % self.__account_id).json()

        def accept(self):
            """
            Accept consent for the provided account.
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
            :rtype: list[AccountInvite]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/invites' % self.__account_id).json()

        def get(self, invite_id):
            """
            Get an account's invite with the provided account invite id.
            :param str invite_id: the account invite id
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/invites/%s' % (self.__account_id, invite_id)).json()

        def create(self, invite):
            """
            Create an account invite using the provided account.
            :param AccountInvite invite: the account invite object
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/invites' % self.__account_id, json=invite).json()

        def update(self, invite):
            """
            Update an account invite using the provided account.
            :param AccountInvite invite: the account invite object
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.put(
                '/accounts/%s/invites/%s' % (self.__account_id, invite['id']),
                json=invite
            ).json()

        def delete(self, invite_id):
            """
            Delete an account invite using the provided account.
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

        def list(self, invoice_filter):
            """
            List all invoices for an account.
            :param dict invoice_filter: a filter object that matches Stripe's invoice filter
                https://stripe.com/docs/api/invoices/list
            :rtype: list[NetworkInvoice]
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/invoices' % self.__account_id, json=invoice_filter).json()

        def list_upcoming(self):
            """
            List all upcoming invoices for an account.
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
            :rtype: list[AccountMember]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/members' % self.__account_id).json()

        def get(self, user_id):
            """
            Get a member by their user id for the provided account.
            :param str user_id: a user id
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/members/%s' % (self.__account_id, user_id)).json()

        def create(self, member):
            """
            Create an member for the provided account.  It may be better to use the
            :func:`Client.AccountInvite.post` if the user does or does not exist.
            :param AccountMember member:  the account member object
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/members' % self.__account_id, json=member).json()

        def update(self, member):
            """
            Update a member for the provided account.
            :param AccountMember member:  the account member object
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.put(
                '/accounts/%s/members/%s' % (self.__account_id, member['user']['id']),
                json=member
            ).json()

        def delete(self, user_id):
            """
            Delete a member from the provided account.
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

        def usage_by_connection(self, options):
            """
            Retrieve egress/ingress total usage by connections
            :param UsageByConnectionOptions options:
            :rtype: list[NetworkConnectionEgressIngress]
            :raises: .exception.HttpClientException
            """
            return self.__session.post(
                '/accounts/%s/metrics/usageByConnection' % self.__account_id,
                json=options
            ).json()

        def usage_by_connection_and_time(self, options):
            """
            Retrieve usage by a single connection over time
            :param UsageByConnectionAndTimeOptions options:
            :rtype: list[ConnectionTimeEgressIngress]
            :raises: .exception.HttpClientException
            """
            return self.__session.post(
                '/accounts/%s/metrics/usageByConnectionAndTime' % self.__account_id,
                json=options
            ).json()

        def usage_by_network_and_time(self, options):
            """
            Retrieve usage of networks over time
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
            :rtype: list[Network]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/networks' % self.__account_id).json()

        def create(self, network):
            """
            Create a network for the provided account.
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
            :rtype: list[Port]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/ports' % self.__account_id).json()

        def create(self, port):
            """
            Create a port for the provided account.
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
            :rtype: list[AccountRole]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/roles' % self.__account_id).json()

        def get(self, role_id):
            """
            Get a role by its id for the provided account.
            :param str role_id: the role id
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s/roles/%s' % (self.__account_id, role_id)).json()

        def create(self, role):
            """
            Create a role for the provided account.
            :param AccountRole role: the account role object
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/accounts/%s/roles' % self.__account_id, json=role).json()

        def update(self, role):
            """
            Update a role for the provided account.
            :param AccountRole role: the account role object
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.put('%s/roles/%s' % (self.__account_id, role['id']), json=role).json()

        def delete(self, role_id):
            """
            Update a role for the provided account.
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

        def list(self, facility):
            """
            Get the supported ports for the provided account.
            :param Facility facility: the facility to list supported ports for
            :rtype: list[SupportedPort]
            :raises: .exception.HttpClientException
            """
            return self.__session.get(
                '/accounts/%s/supportedPorts' % self.__account_id,
                params={'facility': facility['id']}
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
            :rtype: list[CloudRegion]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/cloudRegions').json()

        def get(self, cloud_region_id):
            """
            Get the cloud region with the provided cloud region id.
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
            :rtype: list[CloudRegion]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/cloudServices').json()

        def get(self, cloud_service_id):
            """
            Get the cloud service with the provided cloud service id.
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

        def get(self, connection_id):
            """
            Get a connection with the provided connection id.
            :param str connection_id: the connection id
            :rtype: Connection
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/connections/%s' % connection_id).json()

        def update(self, connection, wait_until_active=False):
            """
            Updated a connection.
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

        def delete(self, connection_id, wait_until_deleted=False):
            """
            Delete a connection.
            :param str connection_id: the connection id
            :param bool wait_until_deleted: wait until the connection is deleted using a backoff retry
            :raises: .exception.HttpClientException
            :raises: .exception.ConnectionOperationTimeoutException
            :raises: .exception.ConnectionOperationFailedException
            """
            self.__session.delete(connection_id)
            if wait_until_deleted:
                Client.ConnectionsClient.__get_connection_until_not_found(
                    self.__session,
                    connection_id,
                    [ConnectionState.FAILED_TO_DELETE]
                )

        def get_tasks(self, connection_id):
            """
            Get the tasks for a connection.
            :param str connection_id: the connection id
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/connections/%s/tasks' % connection_id).json()

        def create_task(self, connection_id, task):
            """
            Create a task for a connection.
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
            :rtype: list[Facility]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/facilities').json()

        def get(self, facility_id):
            """
            Get a facility with the provided facility id.
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

        def get(self, gateway_id):
            """
            Get a gateway by its id
            :param str gateway_id: the gateway id
            :rtype: Gateway
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s' % gateway_id).json()

        def get_bgp_routes(self, gateway_id):
            """
            Get the bgp routes for a gateway.
            :param str gateway_id: the gateway id
            :rtype: list[BGPRoute]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/bgpRoutes' % gateway_id).json()

        def get_connectivity_over_time(self, gateway_id, date_filter):
            """
            Get the connectivity details for a gateway by id over time.
            :param str gateway_id: the gateway id
            :param DateFilter date_filter: a date filter consisting of 'gt', 'lt', 'gte', 'lte' properties
            :rtype: list[ConnectivityByGateway]
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/gateways/%s/metrics/connectivity' % gateway_id, json=date_filter).json()

        def get_latest_connectivity(self, gateway_id):
            """
            Get the current connectivity details for a gateway by id.
            :param str gateway_id: the gateway id
            :rtype: ConnectivityByGateway
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/metrics/connectivity/current' % gateway_id).json()

        def get_tasks(self, gateway_id):
            """
            Get the tasks for a gateway.
            :param str gateway_id: the gateway id
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/tasks' % gateway_id).json()

        def create_task(self, gateway_id, task):
            """
            Create a task for a gateway.
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
            :rtype: list[Location]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/locations').json()

        def get(self, location_id):
            """
            Get a location with the provided location id.
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

        def get(self, network_id):
            """
            Get a network with the provided network id.
            :param str network_id: the network id
            :rtype: Network
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/networks/%s' % network_id).json()

        def update(self, network):
            """
            Update a network.
            :param Network network: the network object
            :rtype: Network
            :raises: .exception.HttpClientException
            """
            return self.__session.put('/networks/%s' % network['id'], json=network).json()

        def delete(self, network_id):
            """
            Delete a network.
            :param str network_id: the network id
            :raises: .exception.HttpClientException
            """
            self.__session.delete('/networks/%s' % network_id)

        def connections(self, network_id):
            """
            Get the account network connections client using the provided account.
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
            :rtype: list[Connection]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/networks/%s/connections' % self.__network_id).json()

        def create(self, connection, wait_until_active=False):
            """
            Create a connection for the provided network.
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

        def list(self, *types):
            """
            List all option objects provided by the API.  These are constant enumerations that are
            used for various parts of the API.  A optional set of **types** may be passed in
            to filter the response.
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

        def get(self, port_id):
            """
            Get the port with the provided port id.
            :param str port_id: the port id
            :rtype: Port
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/ports/%s' % port_id).json()

        def get_accounts_using_port(self, port_id):
            """
            Get the accounts using the port with the provided port id.
            :param str port_id: the port id
            :rtype: list[Link]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/ports/%s/accounts' % port_id).json()

        def update(self, port):
            """
            Update a port.
            :param Port port: the port object
            :rtype: Port
            :raises: .exception.HttpClientException
            """
            return self.__session.put('/ports/%s' % port['id'], json=port).json()

        def delete(self, port_id):
            """
            Delete a port.
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

        def get(self, supported_connection_id):
            """
            Get the supported connection with the provided supported connection id.
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

        def list(self, state=None):
            """
            List all tasks.
            :param str state: find all tasks for a particular state
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/tasks', params={'state': state}).json()

        def get(self, task_id):
            """
            Get a task by it's id.
            :param str task_id: the task id
            :rtype: Task
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/tasks/%s' % task_id).json()
