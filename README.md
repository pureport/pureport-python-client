# Pureport Python Client
A thin Python 2/3 client for the Pureport ReST API, backed by [requests](http://docs.python-requests.org/en/master/).

## Install
```bash
pip install pureport-client
```

## Usage
```python
from pureport.api.client import Client

client = Client()
client.login("MY_API_KEY", "MY_API_SECRET")

### List Accounts
accounts = client.accounts.list()
first_account = accounts[0]

### Get all Members or Roles for an Account
members = client.accounts.members(first_account).list()
roles = client.accounts.roles(first_account).list()

### Update a Member with all the Roles on an Account
first_member = members[0]
first_member['roles'] = [Client.to_link(role, role['name']) for role in roles]
client.accounts.members(first_account).update(first_member)
```
