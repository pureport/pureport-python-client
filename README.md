# Pureport Python Client
A thin Python 2/3 client for the Pureport ReST API, backed by [requests](http://docs.python-requests.org/en/master/).

## Install
```bash
pip install pureport-client
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
networks = client.accounts.networks(first_account).list()

### Create a Network for the Account
new_network = client.accounts.networks(first_account).create({
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
    new_connection = client.networks.connections(new_network).create(new_connection_data)
except ClientHttpException as e:
    print(e.response.text)
    
### Retrieve the new AWS Connection by the returned object
client.connections.get(new_connection)

### Retrieve the new AWS Connection by it's 'id'
client.connections.get_by_id(new_connection['id'])

### Delete the new AWS Connection
client.connections.delete(new_connection)

### Expect a 404 error for the deleted connection
try:
    client.connections.get(new_connection)
except NotFoundException as e:
    print(e.response.text)
    
### Delete the Network
client.networks.delete(new_network)
```
