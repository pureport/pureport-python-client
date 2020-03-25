# Pureport Python Client
A thin Python 3 client for the Pureport ReST API, backed by [requests](http://docs.python-requests.org/en/master/).

## Install
```bash
pip install pureport-client
```

For Python2, you can use any version prior to 1.0.0.
```bash
pip install pureport-client<1
```

## Usage
```python
from pureport.api.client import Client
from pureport.exception.api import ClientHttpException, NotFoundException

### Create the Client and login with your API Key
client = Client()
client.login("MY_API_KEY", "MY_API_SECRET")

### List Accounts
accounts = client.accounts.list()
first_account = accounts[0]

### List all Networks for the first Account
networks = client.accounts.networks(first_account['id']).list()

### Create a Network for the Account
new_network = client.accounts.networks(first_account['id']).create({
    'name': 'My First Network'
})

### Obtain a Pureport location link for a new Connection
location = client.locations.list()[0]
location_link = Client.to_link(location, location['name'])

### Create an AWS Connection
new_connection_data = {
    'name': 'My First AWS Connection',
    'type': 'AWS_DIRECT_CONNECT',
    'speed': 50,
    'highAvailability': True,
    'peering': {
        'type': 'PRIVATE'
    },
    'location': location_link,
    'billingTerm': 'HOURLY',
    'awsAccountId': 'YOUR_AWS_ACCOUNT_ID',
    'awsRegion': 'YOUR_AWS_REGION' # e.g. 'us-west-2'
}

new_connection = None
try:
    new_connection = client.networks.connections(new_network['id']).create(new_connection_data)
except ClientHttpException as e:
    print(e.response.text)
    
### Retrieve the new AWS Connection by the returned object
client.connections.get(new_connection['id'])

### Delete the new AWS Connection
client.connections.delete(new_connection['id'])

### Expect a 404 error for the deleted connection
try:
    client.connections.get(new_connection['id'])
except NotFoundException as e:
    print(e.response.text)
    
### Delete the Network
client.networks.delete(new_network['id'])
```

## CLI Usage
This uses [jq](https://stedolan.github.io/jq/) to help parse the JSON output from the Pureport client.

```shell script
export PUREPORT_API_KEY="MY_API_KEY"
export PUREPORT_API_SECRET="MY_API_SECRET"

### List accounts
pureport accounts list | jq

### List all networks for the first account
first_account_id=$(pureport accounts list --name traynham | jq -r '.[0].id')
pureport accounts networks $first_account_id list

### Create a Network for the Account and persist it's id
new_network_id=$(pureport accounts networks $first_account_id create '{"name": "My First Network"}' | jq -r '.id')

### List all pureport locations
pureport locations list | jq

### Create a link object with the first location
location_link=$(pureport locations list | jq -r '.[0] | {id: .id, href: .href, title: .name}')

### Create an AWS Connection
new_connection_id=$(pureport networks connections $new_network_id create --wait_until_active '{
    "name": "My First AWS Connection",
    "type": "AWS_DIRECT_CONNECT",
    "speed": 50,
    "highAvailability": true,
    "peering": {
        "type": "PRIVATE"
    },
    "location": '$location_link',
    "billingTerm": "HOURLY",
    "awsAccountId": "YOUR_AWS_ACCOUNT_ID",
    "awsRegion": "YOUR_AWS_REGION"
}' | jq -r '.id')

### Retrieve the new AWS Connection with the returned id
pureport connections get $new_connection_id | jq

### Delete the new AWS Connection
pureport connections delete --wait_until_deleted $new_connection_id

### Delete the Network
pureport networks delete $new_network_id
```
