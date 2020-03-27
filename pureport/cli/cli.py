from click import group, option, pass_context, version_option

from ..api.client import Client
from .util import construct_commands, find_client_commands


@group(context_settings={'auto_envvar_prefix': 'PUREPORT'})
@option('-u', '--api_url', help='The api url for this client.')
@option('-k', '--api_key', help='The API Key.')
@option('-s', '--api_secret', help='The API Key secret.')
@option('-p', '--api_profile', help='The API Profile if using file-based configuration.')
@option('-t', '--access_token', help='The API Key access token.')
@version_option()
@pass_context
def cli(ctx, api_url, api_key, api_secret, api_profile, access_token):
    """
    \f
    :param click.Context ctx:
    :param str api_url:
    :param str api_key:
    :param str api_secret:
    :param str api_profile:
    :param str access_token:
    """
    ctx.obj = Client(base_url=api_url,
                     key=api_key,
                     secret=api_secret,
                     profile=api_profile,
                     access_token=access_token)


commands = [
    {
        'context': Client.accounts,
        'commands': [
            Client.AccountsClient.list,
            Client.AccountsClient.get,
            Client.AccountsClient.create,
            Client.AccountsClient.update,
            Client.AccountsClient.delete,
            {
                'context': Client.AccountsClient.api_keys,
                'commands': find_client_commands(Client.AccountAPIKeysClient)
            },
            {
                'context': Client.AccountsClient.audit_log,
                'commands': find_client_commands(Client.AccountAuditLogClient)
            },
            {
                'context': Client.AccountsClient.billing,
                'commands': find_client_commands(Client.AccountBillingClient)
            },
            {
                'context': Client.AccountsClient.connections,
                'commands': find_client_commands(Client.AccountConnectionsClient)
            },
            {
                'context': Client.AccountsClient.consent,
                'commands': find_client_commands(Client.AccountConsentClient)
            },
            {
                'context': Client.AccountsClient.invites,
                'commands': find_client_commands(Client.AccountInvitesClient)
            },
            {
                'context': Client.AccountsClient.invoices,
                'commands': find_client_commands(Client.AccountInvoicesClient)
            },
            {
                'context': Client.AccountsClient.members,
                'commands': find_client_commands(Client.AccountMembersClient)
            },
            {
                'context': Client.AccountsClient.metrics,
                'commands': find_client_commands(Client.AccountMetricsClient)
            },
            {
                'context': Client.AccountsClient.networks,
                'commands': find_client_commands(Client.AccountNetworksClient)
            },
            {
                'context': Client.AccountsClient.permissions,
                'commands': find_client_commands(Client.AccountPermissionsClient)
            },
            {
                'context': Client.AccountsClient.ports,
                'commands': find_client_commands(Client.AccountPortsClient)
            },
            {
                'context': Client.AccountsClient.roles,
                'commands': find_client_commands(Client.AccountRolesClient)
            },
            {
                'context': Client.AccountsClient.supported_connections,
                'commands': find_client_commands(Client.AccountSupportedConnectionsClient)
            },
            {
                'context': Client.AccountsClient.supported_ports,
                'commands': find_client_commands(Client.AccountSupportedPortsClient)
            }
        ]
    },
    {
        'context': Client.cloud_regions,
        'commands': find_client_commands(Client.CloudRegionsClient)
    },
    {
        'context': Client.cloud_services,
        'commands': find_client_commands(Client.CloudServicesClient)
    },
    {
        'context': Client.connections,
        'commands': find_client_commands(Client.ConnectionsClient)
    },
    {
        'context': Client.facilities,
        'commands': find_client_commands(Client.FacilitiesClient)
    },
    {
        'context': Client.gateways,
        'commands': find_client_commands(Client.GatewaysClient)
    },
    {
        'context': Client.locations,
        'commands': find_client_commands(Client.LocationsClient)
    },
    {
        'context': Client.networks,
        'commands': [
            Client.NetworksClient.get,
            Client.NetworksClient.update,
            Client.NetworksClient.delete,
            {
                'context': Client.NetworksClient.connections,
                'commands': find_client_commands(Client.NetworkConnectionsClient)
            }
        ]
    },
    {
        'context': Client.options,
        'commands': find_client_commands(Client.OptionsClient)
    },
    {
        'context': Client.ports,
        'commands': find_client_commands(Client.PortsClient)
    },
    {
        'context': Client.supported_connections,
        'commands': find_client_commands(Client.SupportedConnectionsClient)
    },
    {
        'context': Client.tasks,
        'commands': find_client_commands(Client.TasksClient)
    }
]

for command in construct_commands(commands):
    cli.add_command(command)
