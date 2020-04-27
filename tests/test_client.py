from click import group, pass_context, version_option
from click.testing import CliRunner
from requests_mock import Adapter
from re import compile, sub
from unittest import TestCase
from os import environ

from pureport.api.client import Client
from pureport.cli.cli import commands
from pureport.cli.util import construct_commands
from pureport.util.api import PureportSession


def __create_mock_client():
    """
    This creates a mock :class:`Client` instance.  It uses
    a real client to call out to the server for the OpenAPI data
    and constructs mock paths that can emulate the resources available
    on the server
    :rtype: Client
    """
    adapter = Adapter()
    # Loads all paths from OpenAPI as mock path matchers
    # The paths come in the form '/accounts/{account_id}', which we'll
    # instead convert to proper Regex path's /accounts/([^/]+)
    open_api = Client().open_api()
    for path, path_obj in open_api['paths'].items():
        url = compile('^mock://' + sub(r'{[^}]+}', '([^/]+)', path) + '$')
        for method, method_obj in path_obj.items():
            adapter.register_uri(method.upper(), url, json={})
    adapter.register_uri('POST',
                         'mock:///login',
                         json={
                             'access_token': '',
                             'refresh_token': '',
                             'expires_in': 2 ^ 31
                         })
    session = PureportSession(base_url='mock://')
    session.mount('mock', adapter)
    return Client(base_url='mock://', key='', secret='', session=session)


def __create_mock_cli(pureport_client):
    """
    This creates a mock CLI using a mock client.
    :param Client pureport_client:
    :rtype: click.Command
    """
    @group(context_settings={'auto_envvar_prefix': 'PUREPORT'})
    @version_option()
    @pass_context
    def cli(ctx):
        """
        \f
        :param click.Context ctx:
        """
        ctx.obj = pureport_client

    for command in construct_commands(commands):
        cli.add_command(command)
    return cli


client = __create_mock_client()
runner = CliRunner()
cli = __create_mock_cli(client)


def test_command(*args):
    result = runner.invoke(cli, args=args)
    assert result.exit_code == 0


class TestAccountsClient(TestCase):
    def test_list(self):
        client.accounts.list()
        test_command('accounts', 'list')

    def test_get(self):
        client.accounts.get('123')
        test_command('accounts', 'get', '123')

    def test_create(self):
        client.accounts.create({'id': '123'})
        test_command('accounts', 'create', '{"id": "123"}')

    def test_update(self):
        client.accounts.update({'id': '123'})
        test_command('accounts', 'update', '{"id": "123"}')

    def test_delete(self):
        client.accounts.delete('123')
        test_command('accounts', 'delete', '123')


class TestAccountApiKeysClient(TestCase):
    def test_list(self):
        client.accounts.api_keys('123').list()
        test_command('accounts', 'api-keys', '-a', '123', 'list')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'api-keys', 'list')

    def test_get(self):
        client.accounts.api_keys('123').get('123')
        test_command('accounts', 'api-keys', '-a', '123', 'get', '123')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'api-keys', 'get', '123')

    def test_create(self):
        client.accounts.api_keys('123').create({'key': '123'})
        test_command('accounts', 'api-keys', '-a', '123', 'create', '{"key": "123"}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'api-keys', 'create', '{"key": "123"}')

    def test_update(self):
        client.accounts.api_keys('123').update({'key': '123'})
        test_command('accounts', 'api-keys', '-a', '123', 'update', '{"key": "123"}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'api-keys', 'update', '{"key": "123"}')

    def test_delete(self):
        client.accounts.api_keys('123').delete('123')
        test_command('accounts', 'api-keys', '-a', '123', 'delete', '123')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'api-keys', 'delete', '123')


class TestAccountAuditLogClient(TestCase):
    def test_query(self):
        client.accounts.audit_log('123').query()
        test_command('accounts', 'audit-log', '-a', '123', 'query')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'audit-log', 'query')


class TestAccountBillingClient(TestCase):
    def test_get(self):
        client.accounts.billing('123').get()
        test_command('accounts', 'billing', '-a', '123', 'get')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'billing', 'get')

    def test_get_configured(self):
        client.accounts.billing('123').get_configured()
        test_command('accounts', 'billing', '-a', '123', 'get-configured')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'billing', 'get-configured')

    def test_create(self):
        client.accounts.billing('123').create({})
        test_command('accounts', 'billing', '-a', '123', 'create', '{}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'billing', 'create', '{}')

    def test_update(self):
        client.accounts.billing('123').update({})
        test_command('accounts', 'billing', '-a', '123', 'update', '{}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'billing', 'update', '{}')

    def test_delete(self):
        client.accounts.billing('123').delete()
        test_command('accounts', 'billing', '-a', '123', 'delete')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'billing', 'delete')


class TestAccountConnectionsClient(TestCase):
    def test_list(self):
        client.accounts.connections('123').list()
        test_command('accounts', 'connections', '-a', '123', 'list')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'connections', 'list')


class TestAccountConsentClient(TestCase):
    def test_get(self):
        client.accounts.consent('123').get()
        test_command('accounts', 'consent', '-a', '123', 'get')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'consent', 'get')

    def test_accept(self):
        client.accounts.consent('123').accept()
        test_command('accounts', 'consent', '-a', '123', 'accept')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'consent', 'accept')


class TestAccountInvitesClient(TestCase):
    def test_list(self):
        client.accounts.invites('123').list()
        test_command('accounts', 'invites', '-a', '123', 'list')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'invites', 'list')

    def test_get(self):
        client.accounts.invites('123').get('123')
        test_command('accounts', 'invites', '-a', '123', 'get', '123')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'invites', 'get', '123')

    def test_create(self):
        client.accounts.invites('123').create({'id': '123'})
        test_command('accounts', 'invites', '-a', '123', 'create', '{"id": "123"}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'invites', 'create', '{"id": "123"}')

    def test_update(self):
        client.accounts.invites('123').update({'id': '123'})
        test_command('accounts', 'invites', '-a', '123', 'update', '{"id": "123"}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'invites', 'update', '{"id": "123"}')

    def test_delete(self):
        client.accounts.invites('123').delete('123')
        test_command('accounts', 'invites', '-a', '123', 'delete', '123')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'invites', 'delete', '123')


class TestAccountInvoicesClient(TestCase):
    def test_list(self):
        client.accounts.invoices('123').list({})
        test_command('accounts', 'invoices', '-a', '123', 'list', "{}")
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'invoices', 'list', "{}")

    def test_list_upcoming(self):
        client.accounts.invoices('123').list_upcoming()
        test_command('accounts', 'invoices', '-a', '123', 'list-upcoming')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'invoices', 'list-upcoming')


class TestAccountMembersClient(TestCase):
    def test_list(self):
        client.accounts.members('123').list()
        test_command('accounts', 'members', '-a', '123', 'list')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'members', 'list')

    def test_get(self):
        client.accounts.members('123').get('123')
        test_command('accounts', 'members', '-a', '123', 'get', '123')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'members', 'get', '123')

    def test_create(self):
        client.accounts.members('123').create({'user': {'id': '123'}})
        test_command('accounts', 'members', '-a', '123', 'create', '{"id": "123"}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'members', 'create', '{"id": "123"}')

    def test_update(self):
        client.accounts.members('123').update({'user': {'id': '123'}})
        test_command('accounts', 'members', '-a', '123', 'get', '{"id": "123"}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'members', 'get', '{"id": "123"}')

    def test_delete(self):
        client.accounts.members('123').delete('123')
        test_command('accounts', 'members', '-a', '123', 'delete', '123')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'members', 'delete', '123')


class TestAccountMetricsClient(TestCase):
    def test_usage_by_connection(self):
        client.accounts.metrics('123').usage_by_connection({})
        test_command('accounts', 'metrics', '-a', '123', 'usage-by-connection', '{}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'metrics', 'usage-by-connection', '{}')

    def test_usage_by_connection_and_time(self):
        client.accounts.metrics('123').usage_by_connection_and_time({})
        test_command('accounts', 'metrics', '-a', '123', 'usage-by-connection-and-time', '{}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'metrics', 'usage-by-connection-and-time', '{}')

    def test_usage_by_network_and_time(self):
        client.accounts.metrics('123').usage_by_network_and_time({})
        test_command('accounts', 'metrics', '-a', '123', 'usage-by-network-and-time', '{}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'metrics', 'usage-by-network-and-time', '{}')


class TestAccountNetworksClient(TestCase):
    def test_list(self):
        client.accounts.networks('123').list()
        test_command('accounts', 'networks', '-a', '123', 'list')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'networks', 'list')

    def test_create(self):
        client.accounts.networks('123').create({})
        test_command('accounts', 'networks', '-a', '123', 'create', '{}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'networks', 'create', '{}')


class TestAccountPermissionsClient(TestCase):
    def test_get(self):
        client.accounts.permissions('123').get()
        test_command('accounts', 'permissions', '-a', '123', 'get')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'permissions', 'get')


class TestAccountPortsClient(TestCase):
    def test_list(self):
        client.accounts.ports('123').list()
        test_command('accounts', 'ports', '-a', '123', 'list')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'ports', 'list')

    def test_create(self):
        client.accounts.ports('123').create({})
        test_command('accounts', 'ports', '-a', '123', 'create', '{}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'ports', 'create', '{}')


class TestAccountRolesClient(TestCase):
    def test_list(self):
        client.accounts.roles('123').list()
        test_command('accounts', 'roles', '-a', '123', 'list')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'roles', 'list')

    def test_get(self):
        client.accounts.roles('123').get('123')
        test_command('accounts', 'roles', '-a', '123', 'get', '123')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'roles', 'get', '123')

    def test_create(self):
        client.accounts.roles('123').create({'id': '123'})
        test_command('accounts', 'roles', '-a', '123', 'create', '{"id": "123"}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'roles', 'create', '{"id": "123"}')

    def test_update(self):
        client.accounts.roles('123').update({'id': '123'})
        test_command('accounts', 'roles', '-a', '123', 'update', '{"id": "123"}')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'roles', 'update', '{"id": "123"}')

    def test_delete(self):
        client.accounts.roles('123').delete('123')
        test_command('accounts', 'roles', '-a', '123', 'get', '123')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'roles', 'get', '123')


class TestAccountSupportedConnectionsClient(TestCase):
    def test_list(self):
        client.accounts.supported_connections('123').list()
        test_command('accounts', 'supported-connections', '-a', '123', 'list')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'supported-connections', 'list')


class TestAccountSupportedPortsClient(TestCase):
    def test_list(self):
        client.accounts.supported_ports('123').list('123')
        test_command('accounts', 'supported-ports', '-a', '123', 'list', '123')
        environ['PUREPORT_ACCOUNT_ID'] = '123'
        test_command('accounts', 'supported-ports', 'list', '123')


class TestCloudRegionsClient(TestCase):
    def test_list(self):
        client.cloud_regions.list()
        test_command('cloud-regions', 'list')

    def test_get(self):
        client.cloud_regions.get('123')
        test_command('cloud-regions', 'get', '123')


class TestCloudServicesClient(TestCase):
    def test_list(self):
        client.cloud_services.list()
        test_command('cloud-services', 'list')

    def test_get(self):
        client.cloud_services.get('123')
        test_command('cloud-services', 'get', '123')


class TestConnectionsClient(TestCase):
    def test_get(self):
        client.connections.get('123')
        test_command('connections', 'get', '123')

    def test_update(self):
        client.connections.update({'id': '123'})
        test_command('connections', 'update', '{"id": "123"}')

    def test_delete(self):
        client.connections.delete('123')
        test_command('connections', 'delete', '123')

    def test_get_tasks(self):
        client.connections.get_tasks('123')
        test_command('connections', 'get-tasks', '123')

    def test_create_task(self):
        client.connections.create_task('123', {})
        test_command('connections', 'create-task', '123', '{}')


class TestFacilitiesClient(TestCase):
    def test_list(self):
        client.facilities.list()
        test_command('facilities', 'list')

    def test_get(self):
        client.facilities.get('123')
        test_command('facilities', 'get', '123')


class TestGatewaysClient(TestCase):
    def test_get(self):
        client.gateways.get('123')
        test_command('gateways', 'get', '123')

    def test_get_bgp_routes(self):
        client.gateways.get_bgp_routes('123')
        test_command('gateways', 'get-bgp-routes', '123')

    def test_get_connectivity_over_time(self):
        client.gateways.get_connectivity_over_time('123', {'gt': '0'})
        test_command('gateways', 'get-connectivity-over-time', '123', '{"gt": "0"}')

    def test_get_latest_connectivity(self):
        client.gateways.get_latest_connectivity('123')
        test_command('gateways', 'get-latest-connectivity', '123')

    def test_get_tasks(self):
        client.gateways.get_tasks('123')
        test_command('gateways', 'get-tasks', '123')

    def test_create_task(self):
        client.gateways.create_task('123', {})
        test_command('gateways', 'create-task', '123', '{}')


class TestLocationsClient(TestCase):
    def test_list(self):
        client.locations.list()
        test_command('locations', 'list')

    def test_get(self):
        client.locations.get('123')
        test_command('locations', 'get', '123')


class TestNetworksClient(TestCase):
    def test_get(self):
        client.networks.get('123')
        test_command('networks', 'get', '123')

    def test_update(self):
        client.networks.update({'id': '123'})
        test_command('networks', 'update', '{"id": "123"}')

    def test_delete(self):
        client.networks.delete('123')
        test_command('networks', 'delete', '123')


class TestNetworkConnectionsClient(TestCase):
    def test_get(self):
        client.networks.connections('123').list()
        test_command('networks', 'connections', '-n', '123', 'list')
        environ['PUREPORT_NETWORK_ID'] = '123'
        test_command('networks', 'connections', 'list')

    def test_create(self):
        client.networks.connections('123').create({})
        test_command('networks', 'connections', '-n', '123', 'create', '{}')
        environ['PUREPORT_NETWORK_ID'] = '123'
        test_command('networks', 'connections', 'create', '{}')


class TestOptionsClient(TestCase):
    def test_list(self):
        client.options.list()
        test_command('options', 'list')

    def test_list_with_types(self):
        client.options.list(['IKEV1IKEEncryption'])
        test_command('options', 'list', '-t', 'IKEV1IKEEncryption')


class TestPortsClient(TestCase):
    def test_get(self):
        client.ports.get('123')
        test_command('ports', 'get', '123')

    def test_get_accounts_using_port(self):
        client.ports.get_accounts_using_port('123')
        test_command('ports', 'get-accounts-using-port', '123')

    def test_update(self):
        client.ports.update({'id': '123'})
        test_command('ports', 'update', '{"id": "123"}')

    def test_delete(self):
        client.ports.delete('123')
        test_command('ports', 'delete', '123')


class TestSupportedConnectionsClient(TestCase):
    def test_get(self):
        client.supported_connections.get('123')
        test_command('supported-connections', 'get', '123')


class TestTasksClient(TestCase):
    def test_list(self):
        client.tasks.list()
        test_command('tasks', 'list')

    def test_get(self):
        client.tasks.get('123')
        test_command('tasks', 'get', '123')
