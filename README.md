# Pureport CLI

This project provides a command line interface for the Pureport REST API.

## Install

```bash
  $ pip install pureport-client
```

### Supported Pyton Versions

The Pureport CLi supports Python 3.5+ and later

## Getting Started

In order to use the Pureport CLI, you must first have a valid Pureport acccount 
and have created and downloaded API keys.  Once you have obtained your
Pureport API keys, simply create environment variables for the API
key and API secret.

To get started, either sign up or login to your existing Pureport account at 
https://console.pureport.com and generate your API keys.

Once the keys are generated, set the required environment variables.


```
   export PUREPORT_API_KEY="<your api key here>"
   export PUREPORT_API_SECRET="<your api secret here>"
```

### Usage

The following examples uses [jq](https://stedolan.github.io/jq/) to help 
parse the JSON output from the Pureport client.

```shell script

  ### List accounts
  pureport accounts list | jq

  ### List all networks for the first account
  first_account_id=$(pureport accounts list --name traynham | jq -r '.[0].id')
  pureport accounts networks -a $first_account_id list

  ### Create a Network for the Account and persist it's id
  new_network_id=$(pureport accounts networks -a $first_account_id create '{"name": "My First Network"}' | jq -r '.id')

  ### List all pureport locations
  pureport locations list | jq

  ### Create a link object with the first location
  location_link=$(pureport locations list | jq -r '.[0] | {id: .id, href: .href, title: .name}')

  ### Create an AWS Connection
  new_connection_id=$(pureport networks connections -n $new_network_id create --wait_until_active '{
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

## Contributing

This project provides an easy to use implementation for consuming the 
Pureport Fabric API for building and managing multicloud networks.  We 
gladly accept contributions to this project from open source community
contributors. 

There are many ways to contribute to this project from opening issues, 
providing documentation updates and, of course, providing code.  If you 
are considering contributing to this project, please review the 
guidlines for contributing to this project found [here](CONTRIBUTING.md).

Also please be sure to review our open source community Code of Conduct
found [here](CODE_OF_CONDUCT.md).

## License

This project is licenses under the MIT open source license.
