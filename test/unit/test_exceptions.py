# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from unittest.mock import MagicMock

import pureport_client.exceptions as exceptions

from ..utils import utils


def test_pureport_client_error():
    message = utils.random_string()
    obj = MagicMock()

    exc = exceptions.PureportClientError(message, exc=obj)

    assert exc.message == message
    assert exc.exc == obj


def test_pureport_client_connection_error():
    message = utils.random_string()
    obj = MagicMock()
    conn = MagicMock()

    exc = exceptions.PureportConnectionError(message, obj, connection=conn)

    assert isinstance(exc, exceptions.PureportClientError)
    assert exc.message == message
    assert exc.connection == conn
    assert exc.exc == obj


def test_missing_action_token_exceptiion():
    message = utils.random_string()
    exc = exceptions.MissingAccessTokenError(message)
    assert isinstance(exc, exceptions.PureportClientError)
    assert exc.message == message


def test_connection_operation_timeout_exception():
    message = utils.random_string()
    exc = exceptions.ConnectionOperationTimeoutError(message)
    assert isinstance(exc, exceptions.PureportClientError)
    assert isinstance(exc, exceptions.PureportConnectionError)
    assert exc.message == message


def test_connection_operation_failed_exception():
    message = utils.random_string()
    exc = exceptions.ConnectionOperationFailedError(message)
    assert isinstance(exc, exceptions.PureportClientError)
    assert isinstance(exc, exceptions.PureportConnectionError)
    assert exc.message == message


def test_client_http_exception():
    message = utils.random_string()
    status_code = utils.random_int()
    reason = utils.random_string()
    exc = exceptions.ClientHttpError(status_code, reason, message)
    assert isinstance(exc, exceptions.PureportClientError)
    assert exc.message == message
    assert exc.status_code == status_code
    assert exc.reason == reason
