We use [click](https://click.palletsprojects.com/en/7.x/commands/) to drive the CLI and
this is a description of our CLIs implementation.

Click has many annotations and is largely annotation driven.  

The `@option` & `@argument` annotations store a set of `click.Parameters` on function references
under the hidden attribute `__click_params__`.  This is done via the `click.decorators._param_memo` function.
This keeps the function working without any change in functionality.  Therefore, throughout 
our API client (`pureport.api.client.Client`), we can attach `@option` & `@argument` annotations without any 
consequential change in functionality.

An `@option` or `@argument` parameter directly maps to the function signature, and the two should map 1-to-1, in order.
For example:

```python
from click import argument, option

@option('--a')
@argument('b')
def foo(a, b):
    pass
```

Click also exposes two other important annotations, `@command` & `@group`.  These annotations
take the wrapped function and create a `click.Command` or `click.Group` class instance.  These classes look for the
`__click_params__` hidden attribute and construct a proper CLI command with options and arguments.

The `@group` command constructs a no-command holder for listing out sub-commands.  It can however accept its
own `@option` & `@argument` annotations.  An example of this would be:

```python
from click import group, option

@group()
@option('--account_id')
def account(account_id):
    pass
``` 

A click `@command` on the other hand, is typically a function that does something.

```python
from click import command, echo, option

@command()
@option('--account_id')
def echo_account_id(account_id):
    echo(account_id)
``` 

Sub-commands (and sub-groups) can be attached to `@group` functions by prefixing the annotation 
with the parent function reference.

```python
from click import group, echo, option

@group()
def cli():
    pass

@cli.command()  # cli.command attaches this command to the parent 'cli' group above
@option('--account_id')
def echo_account_id(account_id):
    echo(account_id)
```

Unfortunately, using `@command` & `@group` annotations rewrite a function reference to be a class instance of 
`click.Command` or `click.Group` and if we were to do this within our Client classes, it would break the client
as the functions would no longer be callable via a Python REPL.  Instead, we can create commands/groups by
creating a new function that wraps the Client function references.

Take for instance the function `Client.AccountsClient.networks(self, account_id)`. The function is actually not 
callable without a `self` argument that represents an instance of `Client.AccountsClient`.

When we create the initial CLI, we construct an instance of the `Client` class and pass it on as the `context.obj` for
sub-groups/sub-commands.  A sub-group would then use this `context.obj` as the `self` argument for invocation.  A breakdown
of that would look like:

```python
from click import group, pass_context, pass_obj
from functools import update_wrapper
from pureport.api.client import Client

@group()
@pass_context
def cli(ctx, base_url, api_key, api_secret, access_token):
    client = Client(base_url=base_url)
    client.login(api_key, api_secret, access_token)
    ctx.obj = client.accounts

@pass_obj
@pass_context
def networks(ctx, obj, *args, **kwargs):
    ctx.obj = Client.AccountsClient.networks(obj, *args, **kwargs) # obj here is `client.accounts` passed as `self`
    # ^ setting new context obj for subcommands

networks = update_wrapper(networks, Client.AccountsClient.networks)
networks_grp = group()(networks)

cli.add_command(networks_grp)
```

We can further make this functionality reusable for both groups and commands, by consistently creating groups
that construct new sub-Client contexts and commands that invoke functions on those sub-clients.

```python
from click import command, group, pass_context, pass_obj
from functools import update_wrapper
from pureport.api.client import Client

def create_client_group(f):
    @pass_obj
    @pass_context
    def new_func(ctx, obj_client_as_self, *args, **kwargs):
        ctx.obj = f(obj_client_as_self, *args, **kwargs)

    new_func = update_wrapper(new_func, f)
    return group()(new_func)

def create_client_command(f):
    @pass_obj
    def new_func(obj_client_as_self, *args, **kwargs):
        return f(obj_client_as_self, *args, **kwargs)

    new_func = update_wrapper(new_func, f)
    return command()(new_func)

account_networks_grp = create_client_group(Client.AccountsClient.networks)
account_networks_grp.add_command(create_client_command(Client.AccountNetworksClient.list))
```

In the actual implementation, we recursively loop our client classes and add the commands dynamically, 
as well as `click.echo` responses when commands execute to dump JSON to the CLI.
