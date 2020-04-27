
1.0.6 / 2020-04-27
==================

  * Removes unnecessary enum34 dependency
  * Moves all sub-group arguments to options with envvar.

1.0.5 / 2020-04-02
==================

  * Check if instance method instead of static method
  * Add cli to the namespace packages
  * Filter static methods from the CLI
  * Add unit testing

1.0.4 / 2020-04-01
==================

  * Support Python 3.5 by removing click-params dependency
  * Correct docstring rtype

1.0.3 / 2020-03-30
==================

  * Correct compatibility with 2-step login

1.0.2 / 2020-03-27
==================

  * Remove api_url default to prevent issues with credential loading
  * Load credentials from a variety of sources
  * Add different formatting options for the CLI
  * Add common --format/--no-format option to all CLI commands for pretty-printing
  * Add documentation for CLI and correct 2 CLI calls
  * Add a cli to expose all commands in the terminal.

1.0.1 / 2020-03-25
==================

  * Minor corrections to client

1.0.0 / 2020-03-23
==================

  * Update README for API and new version
  * Correcting some pydoc
  * Remove unnecessary API functions
  * Flake8 at 120 character max length
  * Update gitignore (.tox/, venv/)
  * Add tox for building
  * Use newer namespace packaging (requires Python >= 3.5)
  * Syncing latest API changes
  * Add /accounts/x/auditLog endpoint

0.0.8 / 2019-09-27
==================

  * Add task endpoints
  * Add metric endpoints
  * Adding ports/id/accounts endpoint

0.0.7 / 2019-06-13
==================

  * Add supported ports endpoint
  * Add ports api

0.0.6 / 2019-05-30
==================

  * Use refresh_token to auto refresh the access_token if/when it's expired.

0.0.5 / 2019-05-24
==================

  * Add facilities endpoint

0.0.4 / 2019-05-03
==================

  * Correct options type filter

0.0.3 / 2019-05-01
==================

  * Don't call .json for delete calls

0.0.2 / 2019-04-30
==================

  * Add ConnectionState enum and address code review feedback
  * Updating connection create/update/delete to throw errors on bad states
  * Add retry handling to update/delete
  * Use exponential backoff to wait until connection is active
  * Update documentation on how to interact with API client

0.0.1 / 2019-04-29
==================

  * Add the MIT license
  * Throw a subclasses of HttpClientException for easier error handling
  * Initial commit of the Pureport Python Client
