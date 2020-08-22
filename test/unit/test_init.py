# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import logging

from logging import NullHandler, StreamHandler

import pureport_client


def test_descriptors_are_present():

    assert pureport_client.__version__ is not None
    assert pureport_client.__author__ == 'Pureport, Inc'
    assert pureport_client.__license__ == 'MIT'


def test_global_logging_settings():
    assert pureport_client.logging.disable_existing_loggers is False

    log = logging.getLogger('pureport_client')
    assert log.level == 0

    for handler in log.handlers:
        if isinstance(handler, NullHandler):
            break
    else:
        raise Exception("log 'pureport_client' is missing NullHandler")


def test_set_logging():
    log = logging.getLogger('pureport_client')

    assert log.level == 0

    pureport_client.set_logging(10)

    for handler in log.handlers:
        if isinstance(handler, StreamHandler):
            break
    else:
        raise Exception("log 'pureport_client' is missing StreamHandler")

    assert log.level == 10

    pureport_client.set_logging(0)

    assert log.level == 0
