# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from functools import update_wrapper

from json import dumps as json_dumps
from json import loads as json_loads
from json import JSONDecodeError

from inspect import (
    getfullargspec,
    isroutine
)

from click import (
    command,
    group,
    echo,
    pass_context,
    pass_obj,
    Choice,
    Option,
    ParamType
)

from yaml import dump as yaml_dumps


class JsonParamType(ParamType):
    """Backports the click json param type to python 3.5

    This is simplified and copied from
    [click-params](https://click-params.readthedocs.io/en/latest/usage/miscellaneous/#json).
    This was done because click-params doesn't support Python 3.5, but it's not currently EOL.

    """
    name = 'json'

    def __init__(self, **kwargs):
        """Initialize the instance

        :param ParamType: the base click paramtype object
        :type ParamType: `click.ParamType`
        """
        self._kwargs = kwargs

    def convert(self, value, param, ctx):
        try:
            return json_loads(value, **self._kwargs)
        except JSONDecodeError:
            self.fail('%s is not a valid json string' % value, param, ctx)

    def __repr__(self):
        return self.name.upper()


JSON = JsonParamType()


def insert_click_param(f, param):
    """Appends the params on a command

    Much like :func:`click.decorators._param_memo`, this updates
    the params on a command, but instead of append, it prepends
    the parameter

    :param f: the function to decorate
    :type f: function

    :param param: an instance of Parameter
    :type param: `click.Paramter

    :returns: None
    """
    if not hasattr(f, "__click_params__"):
        f.__click_params__ = []
    f.__click_params__.insert(0, param)


def create_print_wrapper(f):
    """Creates a print wrapper for commands

    This adds the necessary options for formatting results as well
    as wrapping the command to handle those formatting options.

    :param f: the function to wrap
    :type f: function

    :returns: the wrapped function
    :rtype: function
    """
    def new_func(*args, **kwargs):
        response_format = kwargs.pop('format')
        response = f(*args, **kwargs)
        # if the function returns a response, we'll just echo it as JSON
        if response is not None:
            if response_format == 'json_pp':
                echo(json_dumps(response, indent=2, sort_keys=True))
            elif response_format == 'json':
                echo(json_dumps(response))
            elif response_format == 'yaml':
                echo(yaml_dumps(response))
        return response

    new_func = update_wrapper(new_func, f)
    insert_click_param(new_func,
                       Option(['--format'],
                              type=Choice(['json_pp', 'json', 'yaml']),
                              default='json_pp',
                              help='Specify how responses should be formatted and echoed to the terminal.'))
    return new_func


def create_client_group(f, name=None):
    """Constructs a Client Group command.

    Given a reference to the Client class function, e.g. the @property Client.accounts or
    instance function Client.AccountsClient.networks(account_id), this constructs a click.Group.

    It passes the parent context and parent obj (e.g. the parent Client class instance), then
    sets a new ctx.obj that is the invocation of this command.  We simply pass along any of
    *args and **kwargs down into the function.

    The `update_wrapper` is responsible for copying all the actual functions @option/@argument
    properties to the new function.

    Finally calling `group()(new_func)` creates the Group object and correctly parses all
    the parameters off the function.

    :param f: the class object to introspect
    :type f: `pureport_client.commands.CommandBase`

    :param name: the name of the group
    :type: name: str

    :returns: an instance of click Group
    :rtype: `click.core.Group`
    """
    actual_f = f.fget if isinstance(f, property) else f

    @pass_obj
    @pass_context
    def new_func(ctx, obj, *args, **kwargs):
        ctx.obj = actual_f(obj, *args, **kwargs)

    new_func = update_wrapper(new_func, actual_f)
    return group(name)(new_func)


def create_client_command(f):
    """Constructs a Client Command.

    Given a reference to the Client class function, e.g. the Client.AccountClient.list,
    this constructs a click.Command.

    It passes the parent Group (see create_client_group) obj (e.g. the Client class instance), then
    sets invokes the function reference using the parent context `obj` as the `self` argument
    of the command.

    The `update_wrapper` is responsible for copying all the actual functions @option/@argument
    properties to the new function.

    Finally calling `command()(new_func)` creates the Command object and correctly parses all
    the parameters off the function.

    :param f: the class object to introspect
    :type f: `pureport_client.commands.CommandBase`

    :returns: an instance of click Command
    :rtype: `click.core.Command`
    """
    actual_f = f.fget if isinstance(f, property) else f
    actual_f = create_print_wrapper(f)

    @pass_obj
    def new_func(obj, *args, **kwargs):
        return actual_f(obj, *args, **kwargs)

    new_func = update_wrapper(new_func, actual_f)
    return command()(new_func)


def is_regular_method(klass_or_instance, attr):
    """Test if a value of a class is regular method.

    https://github.com/MacHu-GWU/inspect_mate-project/blob/master/inspect_mate/tester.py#L88-L114
    example::
        class MyClass(object):
            def execute(self, input_data):
                ...

    :param klass_or_instance: the base object that contains the method
    :type klass_or_instance: object

    :param attr: the name of the attribute to evaluate
    :type attr: str

    :returns: a boolean value indicating whether or not the attribute
        is a reqular method or not
    :rtype: bool
    """
    value = getattr(klass_or_instance, attr, None)
    result = False
    if isroutine(value) and not isinstance(value, property):
        args = getfullargspec(value).args
        try:
            if args[0] == "self":
                result = True
        except Exception:
            result = False
    return result


def find_client_commands(obj):
    """Introspects the object to find commands

    Given an object, this finds a list of potential commands by
    listing all public instance methods of an object.

    :param obj: the object to introspect
    :type obj: object

    :returns: a list of commands
    :rtype: list
    """
    commands = []
    for name in dir(obj):
        if not name.startswith('_'):
            if is_regular_method(obj, name):
                attr = getattr(obj, name)
                commands.append(attr)
    return commands


def construct_commands(commands):
    """Recursively build a list of commands and groups

    Recursively construct a list of click.Command or click.Group and
    attach them to parent groups if necessary.

    :param commands: a list of dictionaries
    :type commands: list

    :returns: a list of commands
    :rtype: list
    """
    for cmd in commands:
        if isinstance(cmd, dict) and 'context' in cmd:
            grp = create_client_group(cmd['context'], cmd['name'])
            for child_cmd in construct_commands(cmd['commands']):
                grp.add_command(child_cmd)
            yield grp
        else:
            yield create_client_command(cmd)
