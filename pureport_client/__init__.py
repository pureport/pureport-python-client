# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import logging

from logging import NullHandler

__version__ = "1.0.12"

__author__ = "Pureport, Inc"
__license__ = "MIT"


logging.disable_existing_loggers = False

logging.getLogger(__name__).addHandler(NullHandler())
logging.getLogger(__name__).setLevel(logging.NOTSET)


def set_logging(level):
    """Convenience function to enable logging for pureport-client

    :param level: logging level to emit
    :type level: int
    """
    log = logging.getLogger(__name__)
    log.setLevel(level)

    for handler in log.handlers:
        if handler.get_name() == __name__:
            log.debug("logging handler {} is already configured".format(handler.get_name()))
            break
    else:
        handler = logging.StreamHandler()
        handler.set_name(__name__)
        handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s: %(message)s"))
        log.addHandler(handler)
        log.debug("Added stderr logging handler to logger: %s", __name__)
