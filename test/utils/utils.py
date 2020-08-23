# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import random
import string
import tempfile
import shutil

from contextlib import contextmanager


@contextmanager
def tempdir():
    try:
        tmpdir = tempfile.mkdtemp()
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def random_string(nodigits=False):
    if nodigits is True:
        return ''.join(
            random.choice(string.ascii_uppercase) for _ in range(random.randint(3, 20))
        )
    else:
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(3, 20))
        )


def random_int():
    return random.randrange(0, 101)


def random_float():
    return random.uniform(1.0, 100.0)
