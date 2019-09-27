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
APIKey = dict
BGPRoute = dict
CloudRegion = dict
CloudService = dict
Connection = dict
ConnectionTimeEgressIngress = dict
Gateway = dict
Facility = dict
Location = dict
Network = dict
NetworkConnectionEgressIngress = dict
NetworkInvoice = dict
NetworkTimeUsage = dict
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

        def list(self):
            """
            Get a list of all accounts.
            :rtype: list[Account]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts').json()

        def get_by_id(self, account_id):
            """
            Get an account by its id.
            :param str account_id: the account id
            :rtype: Account
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/accounts/%s' % account_id).json()

        def get(self, account):
            """
            Get an account using the provided account object.
            :param Account account: the account object
            :rtype: Account
            :raises: .exception.HttpClientException
            """
            return self.__session.get(account['href']).json()

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
            return self.__session.put(account['href'], json=account).json()

        def delete(self, account):
            """
            Delete an account.
            :param Account account: the account object
            :raises: .exception.HttpClientException
            """
            self.__session.delete(account['href'])

        def api_keys(self, account):
            """
            Get the account api keys client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountAPIKeysClient
            """
            return Client.AccountAPIKeysClient(self.__session, account)

        def billing(self, account):
            """
            Get the account billing client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountBillingClient
            """
            return Client.AccountBillingClient(self.__session, account)

        def connections(self, account):
            """
            Get the account connections client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountConnectionsClient
            """
            return Client.AccountConnectionsClient(self.__session, account)

        def consent(self, account):
            """
            Get the account consent client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountConsentClient
            """
            return Client.AccountConsentClient(self.__session, account)

        def invites(self, account):
            """
            Get the account invites client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountInvitesClient
            """
            return Client.AccountInvitesClient(self.__session, account)

        def invoices(self, account):
            """
            Get the account invoices client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountInvoicesClient
            """
            return Client.AccountInvoicesClient(self.__session, account)

        def members(self, account):
            """
            Get the account members client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountMembersClient
            """
            return Client.AccountMembersClient(self.__session, account)

        def metrics(self, account):
            """
            Get the account metrics client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountMetricsClient
            """
            return Client.AccountMetricsClient(self.__session, account)

        def networks(self, account):
            """
            Get the account networks client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountNetworksClient
            """
            return Client.AccountNetworksClient(self.__session, account)

        def permissions(self, account):
            """
            Get the account permissions client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountPermissionsClient
            """
            return Client.AccountPermissionsClient(self.__session, account)

        def ports(self, account):
            """
            Get the account ports client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountPortsClient
            """
            return Client.AccountPortsClient(self.__session, account)

        def roles(self, account):
            """
            Get the account roles client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountRolesClient
            """
            return Client.AccountRolesClient(self.__session, account)

        def supported_connections(self, account):
            """
            Get the account supported connections client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountSupportedConnectionsClient
            """
            return Client.AccountSupportedConnectionsClient(self.__session, account)

        def supported_ports(self, account):
            """
            Get the account supported ports client using the provided account.
            :param Account account: the account object
            :rtype: Client.AccountSupportedConnectionsClient
            """
            return Client.AccountSupportedPortsClient(self.__session, account)

    class AccountAPIKeysClient(object):
        def __init__(self, session, account):
            """
            The Account API Keys client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self):
            """
            Get a list of all API keys for an account.
            :rtype: list[APIKey]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/apikeys' % self.__account['href']).json()

        def get_by_id(self, api_key_key):
            """
            Get an account's API Key with the provided API Key key.
            :param str api_key_key: the key of an API Key
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/apikeys/%s' % (self.__account['href'], api_key_key)).json()

        def get(self, api_key):
            """
            Get an account's API Key with the provided API Key object.
            :param APIKey api_key: the APIKey object
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/apikeys/%s' % (self.__account['href'], api_key['key'])).json()

        def create(self, api_key):
            """
            Create an API Key for the provided account.
            :param APIKey api_key: the APIKey object
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/apikeys' % self.__account['href'], json=api_key).json()

        def update(self, api_key):
            """
            Update an API Key for the provided account.
            :param APIKey api_key: the APIKey object
            :rtype: APIKey
            :raises: .exception.HttpClientException
            """
            return self.__session.put('%s/apikeys/%s' % (self.__account['href'], api_key['key']), json=api_key).json()

        def delete(self, api_key):
            """
            Delete an API Key from the provided account.
            :param APIKey api_key: the APIKey object
            :raises: .exception.HttpClientException
            """
            self.__session.delete('%s/apikeys/%s' % (self.__account['href'], api_key['key']))

    class AccountBillingClient(object):
        def __init__(self, session, account):
            """
            The Account Billing client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def get(self):
            """
            Get the billing information for the provided account.  This does not check parent
            accounts.  If you want to find if any billing is configured, instead use
            :func:`Client.AccountBillingClient.get_configured`.
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/billing' % self.__account['href']).json()

        def get_configured(self):
            """
            Get the billing information for the provided account.  This returns the billing info of the
            account or any parent account.
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/billing/configured' % self.__account['href']).json()

        def create(self, account_billing):
            """
            Add a payment method to provided account.
            :param AccountBilling account_billing: the AccountBilling object
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/billing' % self.__account['href'], json=account_billing).json()

        def update(self, account_billing):
            """
            Update the payment method for the provided account.
            :param AccountBilling account_billing: the AccountBilling object
            :rtype: AccountBilling
            :raises: .exception.HttpClientException
            """
            return self.__session.put('%s/billing' % self.__account['href'], json=account_billing).json()

        def delete(self):
            """
            Delete the current AccountBilling object from the account if it exists.
            :raises: .exception.HttpClientException
            """
            self.__session.delete('%s/billing' % self.__account['href'])

    class AccountConnectionsClient(object):
        def __init__(self, session, account):
            """
            The Account Connections client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self):
            """
            Get all connections for the provided account.
            :rtype: list[Connection]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/connections' % self.__account['href']).json()

    class AccountConsentClient(object):
        def __init__(self, session, account):
            """
            The Account Consent Client client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def get(self):
            """
            Get the consent information for the provided account.
            :rtype: AccountConsent
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/consent' % self.__account['href']).json()

        def accept(self):
            """
            Accept consent for the provided account.
            :rtype: AccountConsent
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/consent' % self.__account['href']).json()

    class AccountInvitesClient(object):
        def __init__(self, session, account):
            """
            The Account Invites client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self):
            """
            Get all invites for the provided account.
            :rtype: list[AccountInvite]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/invites' % self.__account['href']).json()

        def get_by_id(self, invite_id):
            """
            Get an account's invite with the provided account invite id.
            :param str invite_id: the account invite id
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/invites/%s' % (self.__account['href'], invite_id)).json()

        def get(self, invite):
            """
            Get an account's invite using the provided account invite.
            :param AccountInvite invite: the account invite object
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/invites/%s' % (self.__account['href'], invite['id'])).json()

        def create(self, invite):
            """
            Create an account invite using the provided account.
            :param AccountInvite invite: the account invite object
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/invites' % self.__account['href'], json=invite).json()

        def update(self, invite):
            """
            Update an account invite using the provided account.
            :param AccountInvite invite: the account invite object
            :rtype: AccountInvite
            :raises: .exception.HttpClientException
            """
            return self.__session.put('%s/invites/%s' % (self.__account['href'], invite['id']), json=invite).json()

        def delete(self, invite):
            """
            Delete an account invite using the provided account.
            :param AccountInvite invite: the account invite object
            :raises: .exception.HttpClientException
            """
            self.__session.delete('%s/invites/%s' % (self.__account['href'], invite['id']))

    class AccountInvoicesClient(object):
        def __init__(self, session, account):
            """
            The Account Invoices client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self, invoice_filter):
            """
            List all invoices for an account.
            :param dict invoice_filter: a filter object that matches Stripe's invoice filter
                https://stripe.com/docs/api/invoices/list
            :rtype: list[NetworkInvoice]
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/invoices' % self.__account['href'], json=invoice_filter).json()

        def list_upcoming(self):
            """
            List all upcoming invoices for an account.
            :rtype: list[NetworkInvoice]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/invoices/upcoming' % self.__account['href']).json()

    class AccountMembersClient(object):
        def __init__(self, session, account):
            """
            The Account Members client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self):
            """
            List all members for the provided account.
            :rtype: list[AccountMember]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/members' % self.__account['href']).json()

        def get_by_id(self, user_id):
            """
            Get a member by their user id for the provided account.
            :param str user_id: a user id
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/members/%s' % (self.__account['href'], user_id)).json()

        def get(self, member):
            """
            Get a member using a member object for the provided account.
            :param AccountMember member: the account member object
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/members/%s' % (self.__account['href'], member['user']['id'])).json()

        def create(self, member):
            """
            Create an member for the provided account.  It may be better to use the
            :func:`Client.AccountInvite.post` if the user does or does not exist.
            :param AccountMember member:  the account member object
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/members' % self.__account['href'], json=member).json()

        def update(self, member):
            """
            Update a member for the provided account.
            :param AccountMember member:  the account member object
            :rtype: AccountMember
            :raises: .exception.HttpClientException
            """
            return self.__session.put('%s/members/%s' % (self.__account['href'], member['user']['id']), json=member).json()

        def delete(self, member):
            """
            Delete a member from the provided account.
            :param AccountMember member:  the account member object
            :raises: .exception.HttpClientException
            """
            self.__session.delete('%s/members/%s' % (self.__account['href'], member['user']['id']))

    class AccountMetricsClient(object):
        def __init__(self, session, account):
            """
            The Account Networks client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def usage_by_connection(self, options):
            """
            Retrieve egress/ingress total usage by connections
            :param UsageByConnectionOptions options:
            :rtype: list[NetworkConnectionEgressIngress]
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/metrics/usageByConnection' % self.__account['href'], json=options).json()

        def usage_by_connection_and_time(self, options):
            """
            Retrieve usage by a single connection over time
            :param UsageByConnectionAndTimeOptions options:
            :rtype: list[ConnectionTimeEgressIngress]
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/metrics/usageByConnectionAndTime' % self.__account['href'], json=options).json()

        def usage_by_network_and_time(self, options):
            """
            Retrieve usage of networks over time
            :param UsageByNetworkAndTimeOptions options:
            :rtype: list[NetworkTimeUsage]
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/metrics/usageByNetworkAndTime' % self.__account['href'], json=options).json()

    class AccountNetworksClient(object):
        def __init__(self, session, account):
            """
            The Account Networks client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self):
            """
            Get all networks for the provided account.
            :rtype: list[Network]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/networks' % self.__account['href']).json()

        def create(self, network):
            """
            Create a network for the provided account.
            :param Network network:  the network object
            :rtype: Network
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/networks' % self.__account['href'], json=network).json()

    class AccountPermissionsClient(object):
        def __init__(self, session, account):
            """
            The Account Permissions client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def get(self):
            """
            Get all permissions for the provided account.  This returns the effect permission set for the
            currently logged in API Key.
            :rtype: AccountPermissions
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/permissions' % self.__account['href']).json()

    class AccountPortsClient(object):
        def __init__(self, session, account):
            """
            The Account Ports client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self):
            """
            Get all ports for the provided account.
            :rtype: list[Port]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/ports' % self.__account['href']).json()

        def create(self, port):
            """
            Create a port for the provided account.
            :param Port port:  the port object
            :rtype: Port
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/ports' % self.__account['href'], json=port).json()

    class AccountRolesClient(object):
        def __init__(self, session, account):
            """
            The Account Roles client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self):
            """
            List all roles for the provided account.
            :rtype: list[AccountRole]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/roles' % self.__account['href']).json()

        def get_by_id(self, role_id):
            """
            Get a role by its id for the provided account.
            :param str role_id: the role id
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/roles/%s' % (self.__account['href'], role_id)).json()

        def get(self, role):
            """
            Get a role using a role object for the provided account.
            :param AccountRole role: the account role object
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/roles/%s' % (self.__account['href'], role['id'])).json()

        def create(self, role):
            """
            Create a role for the provided account.
            :param AccountRole role: the account role object
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/roles' % self.__account['href'], json=role).json()

        def update(self, role):
            """
            Update a role for the provided account.
            :param AccountRole role: the account role object
            :rtype: AccountRole
            :raises: .exception.HttpClientException
            """
            return self.__session.put('%s/roles/%s' % (self.__account['href'], role['id']), json=role).json()

        def delete(self, role):
            """
            Update a role for the provided account.
            :param AccountRole role: the account role object
            :raises: .exception.HttpClientException
            """
            self.__session.delete('%s/roles/%s' % (self.__account['href'], role['id']))

    class AccountSupportedConnectionsClient(object):
        def __init__(self, session, account):
            """
            The Account Supported Connections client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self):
            """
            Get the supported connections for the provided account.
            :rtype: list[SupportedConnection]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/supportedConnections' % self.__account['href']).json()

    class AccountSupportedPortsClient(object):
        def __init__(self, session, account):
            """
            The Account Supported Ports client
            :param RelativeSession session:
            :param Account account:
            """
            self.__session = session
            self.__account = account

        def list(self, facility):
            """
            Get the supported ports for the provided account.
            :param Facility facility: the facility to list supported ports for
            :rtype: list[SupportedPort]
            :raises: .exception.HttpClientException
            """
            return self.__session.get(
                '%s/supportedPorts' % self.__account['href'],
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

        def get_by_id(self, cloud_region_id):
            """
            Get the cloud region with the provided cloud region id.
            :param str cloud_region_id: the cloud region id
            :rtype: CloudRegion
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/cloudRegions/%s' % cloud_region_id).json()

        def get(self, cloud_region):
            """
            Get the cloud region using the provided cloud region object.
            :param CloudRegion cloud_region: the cloud region object
            :rtype: CloudRegion
            :raises: .exception.HttpClientException
            """
            return self.__session.get(cloud_region['href']).json()

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

        def get_by_id(self, cloud_service_id):
            """
            Get the cloud service with the provided cloud service id.
            :param str cloud_service_id: the cloud service id
            :rtype: CloudRegion
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/cloudServices/%s' % cloud_service_id).json()

        def get(self, cloud_service):
            """
            Get the cloud service using the provided cloud service object.
            :param CloudService cloud_service: the cloud service object
            :rtype: CloudService
            :raises: .exception.HttpClientException
            """
            return self.__session.get(cloud_service['href']).json()

    class ConnectionsClient(object):
        def __init__(self, session):
            """
            The Connections client
            :param RelativeSession session:
            """
            self.__session = session

        @staticmethod
        @retry(ConnectionOperationTimeoutException)
        def get_connection_until_state(session, connection, expected_state, failed_states=[]):
            """
            Retrieve a connection until it enters a certain state using an exponential backoff
            :param RelativeSession session: a :class:`Client`'s relative session
            :param Connection connection: the connection
            :param ConnectionState expected_state: the expected state
            :param list[ConnectionState] failed_states: a list of failed states that instead
                raise ConnectionOperationFailedException
            :rtype: Connection
            :raises: .exception.ConnectionOperationTimeoutException
            :raises: .exception.ConnectionOperationFailedException
            """
            connection = session.get(connection['href']).json()
            if ConnectionState[connection['state']] in failed_states:
                raise ConnectionOperationFailedException(connection=connection)
            if ConnectionState[connection['state']] != expected_state:
                raise ConnectionOperationTimeoutException(connection=connection)
            return connection

        @staticmethod
        @retry(ConnectionOperationTimeoutException)
        def __get_connection_until_not_found(session, connection, failed_states=[]):
            """
            Retrieve a connection until it no longer exists using an exponential backoff
            :param RelativeSession session: a :class:`Client`'s relative session
            :param Connection connection: the connection
            :param list[ConnectionState] failed_states: a list of failed states that instead
                raise ConnectionOperationFailedException
            :raises: .exception.ConnectionOperationTimeoutException
            :raises: .exception.ConnectionOperationFailedException
            """
            try:
                connection = session.get(connection['href']).json()
            except NotFoundException:
                return
            if ConnectionState[connection['state']] in failed_states:
                raise ConnectionOperationFailedException(connection=connection)
            raise ConnectionOperationTimeoutException(connection=connection)

        def get_by_id(self, connection_id):
            """
            Get a connection with the provided connection id.
            :param str connection_id: the connection id
            :rtype: Connection
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/connections/%s' % connection_id).json()

        def get(self, connection):
            """
            Get a connection using the provided connection object.
            :param Connection connection: the connection object
            :rtype: Connection
            :raises: .exception.HttpClientException
            """
            return self.__session.get(connection['href']).json()

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
            connection = self.__session.put(connection['href'], json=connection).json()
            if wait_until_active:
                return Client.ConnectionsClient.get_connection_until_state(
                    self.__session,
                    connection,
                    ConnectionState.ACTIVE,
                    [ConnectionState.FAILED_TO_UPDATE]
                )
            else:
                return connection

        def delete(self, connection, wait_until_deleted=False):
            """
            Delete a connection.
            :param Connection connection: the connection object
            :param bool wait_until_deleted: wait until the connection is deleted using a backoff retry
            :raises: .exception.HttpClientException
            :raises: .exception.ConnectionOperationTimeoutException
            :raises: .exception.ConnectionOperationFailedException
            """
            self.__session.delete(connection['href'])
            if wait_until_deleted:
                Client.ConnectionsClient.__get_connection_until_not_found(
                    self.__session,
                    connection,
                    [ConnectionState.FAILED_TO_DELETE]
                )

        def get_tasks_by_id(self, connection_id):
            """
            Get the tasks for a connection.
            :param str connection_id: the connection id
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/connections/%s/tasks' % connection_id).json()

        def get_tasks(self, connection):
            """
            Get the tasks for a connection.
            :param Connection connection: the connection
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/tasks' % connection['href']).json()

        def create_task(self, connection, task):
            """
            Create a task for a connection.
            :param Connection connection: the connection
            :param Task task: the task
            :rtype: Task
            :raises: .exception.HttpClientException
            """
            return self.__session.post('%s/tasks' % connection['href'], json=task).json()

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

        def get_by_id(self, facility_id):
            """
            Get a facility with the provided facility id.
            :param str facility_id: the facility id
            :rtype: Facility
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/facilities/%s' % facility_id).json()

        def get(self, facility):
            """
            Get a facility using the provided facility object.
            :param Facility facility: the location object
            :rtype: Facility
            :raises: .exception.HttpClientException
            """
            return self.__session.get(facility['href']).json()

    class GatewaysClient(object):
        def __init__(self, session):
            """
            The GatewaysClient client
            :param RelativeSession session:
            """
            self.__session = session

        def get_bgp_routes(self, gateway):
            """
            Get the bgp routes for a gateway.
            :param Gateway gateway: the gateway
            :rtype: list[BGPRoute]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/bgpRoutes' % gateway['id']).json()

        def get_bgp_routes_by_id(self, gateway_id):
            """
            Get the bgp routes for a gateway.
            :param str gateway_id: the gateway id
            :rtype: list[BGPRoute]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/bgpRoutes' % gateway_id).json()

        def get_tasks_by_id(self, gateway_id):
            """
            Get the tasks for a gateway.
            :param str gateway_id: the gateway id
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/tasks' % gateway_id).json()

        def get_tasks(self, gateway):
            """
            Get the tasks for a gateway.
            :param Gateway gateway: the gateway
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/gateways/%s/tasks' % gateway['id']).json()

        def create_task_by_id(self, gateway_id, task):
            """
            Create a task for a gateway.
            :param str gateway_id: the gateway id
            :param Task task: the task
            :rtype: Task
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/gateways/%s/tasks' % gateway_id, json=task).json()

        def create_task(self, gateway, task):
            """
            Create a task for a gateway.
            :param Gateway gateway: the gateway
            :param Task task: the task
            :rtype: Task
            :raises: .exception.HttpClientException
            """
            return self.__session.post('/gateways/%s/tasks' % gateway['id'], json=task).json()

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

        def get_by_id(self, location_id):
            """
            Get a location with the provided location id.
            :param str location_id: the location id
            :rtype: Location
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/locations/%s' % location_id).json()

        def get(self, location):
            """
            Get a location using the provided location object.
            :param Location location: the location object
            :rtype: Location
            :raises: .exception.HttpClientException
            """
            return self.__session.get(location['href']).json()

    class NetworksClient(object):
        def __init__(self, session):
            """
            The Networks client
            :param RelativeSession session:
            """
            self.__session = session

        def get_by_id(self, network_id):
            """
            Get a network with the provided network id.
            :param str network_id: the network id
            :rtype: Network
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/networks/%s' % network_id).json()

        def get(self, network):
            """
            Get a network with the provided network object.
            :param Network network: the network object
            :rtype: Network
            :raises: .exception.HttpClientException
            """
            return self.__session.get(network['href']).json()

        def update(self, network):
            """
            Update a network.
            :param Network network: the network object
            :rtype: Network
            :raises: .exception.HttpClientException
            """
            return self.__session.put(network['href'], json=network).json()

        def delete(self, network):
            """
            Delete a network.
            :param Network network: the network object
            :raises: .exception.HttpClientException
            """
            self.__session.delete(network['href'])

        def connections(self, network):
            """
            Get the account network connections client using the provided account.
            :param Network network:
            :rtype: Client.NetworkConnectionsClient
            """
            return Client.NetworkConnectionsClient(self.__session, network)

    class NetworkConnectionsClient(object):
        def __init__(self, session, network):
            """
            The Network Connections client
            :param RelativeSession session:
            :param Network network:
            """
            self.__session = session
            self.__network = network

        def list(self):
            """
            Get all connections for the provided network.
            :rtype: list[Connection]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('%s/connections' % self.__network['href']).json()

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
            connection = self.__session.post('%s/connections' % self.__network['href'], json=connection).json()
            if wait_until_active:
                return Client.ConnectionsClient.get_connection_until_state(
                    self.__session,
                    connection,
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

        def get_by_id(self, port_id):
            """
            Get the port with the provided port id.
            :param str port_id: the port id
            :rtype: Port
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/ports/%s' % port_id).json()

        def get_accounts_using_port_by_id(self, port_id):
            """
            Get the accounts using the port with the provided port id.
            :param str port_id: the port id
            :rtype: list[Link]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/ports/%s/accounts' % port_id).json()

        def get(self, port):
            """
            Get the port using the provided port.
            :param Port port: the port object
            :rtype: Port
            :raises: .exception.HttpClientException
            """
            return self.__session.get(port['href']).json()

        def update(self, port):
            """
            Update a port.
            :param Port port: the port object
            :rtype: Port
            :raises: .exception.HttpClientException
            """
            return self.__session.put(port['href'], json=port).json()

        def delete(self, port):
            """
            Delete a port.
            :param Port port: the port object
            :raises: .exception.HttpClientException
            """
            self.__session.delete(port['href'])

    class SupportedConnectionsClient(object):
        def __init__(self, session):
            """
            The Supported Connections client
            :param RelativeSession session:
            """
            self.__session = session

        def get_by_id(self, supported_connection_id):
            """
            Get the supported connection with the provided supported connection id.
            :param str supported_connection_id: the supported connection id
            :rtype: SupportedConnection
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/supportedConnections/%s' % supported_connection_id).json()

        def get(self, supported_connection):
            """
            Get the supported connection using the provided supported connection.
            :param SupportedConnection supported_connection: the supported connection object
            :rtype: SupportedConnection
            :raises: .exception.HttpClientException
            """
            return self.__session.get(supported_connection['href']).json()

    class TasksClient(object):
        def __init__(self, session):
            """
            The Tasks client
            :param RelativeSession session:
            """
            self.__session = session

        def list(self):
            """
            List all tasks.
            :rtype: list[Task]
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/tasks').json()

        def get_by_id(self, task_id):
            """
            Get a task by it's id.
            :param str task_id: the task id
            :rtype: Task
            :raises: .exception.HttpClientException
            """
            return self.__session.get('/tasks/%s' % task_id).json()

        def get(self, task):
            """
            Get the task using the provided task.
            :param Task task: the task object
            :rtype: SupportedConnection
            :raises: .exception.HttpClientException
            """
            return self.__session.get(task['href']).json()
