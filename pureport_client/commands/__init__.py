# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import urllib

from logging import getLogger

log = getLogger(__name__)


class CommandBase(object):

    def __init__(self, session=None):
        self._client = session

    client = property(lambda self: self._client)
    session = property(lambda self: self._client.session)

    def __call__(self, method, url, *args, **kwargs):
        log.debug('{} {}'.format(method.upper(), url))
        return getattr(self.session, method.lower())(url, *args, **kwargs).json()

    def _request(self, method, url, *args, **kwargs):
        return self.__call__(method, url, *args, **kwargs)


class AccountsMixin(object):

    def __init__(self, session, account_id):
        super(AccountsMixin, self).__init__(session)
        self._account_id = account_id

    account_id = property(lambda self: self._account_id)

    def __call__(self, method, url, *args, **kwargs):
        url = urllib.parse.urljoin('/accounts/{}/'.format(self.account_id), url)
        return super(AccountsMixin, self).__call__(method, url, *args, **kwargs)


class NetworksMixin(object):

    def __init__(self, session, account_id):
        super(NetworksMixin, self).__init__(session)
        self._network_id = account_id

    network_id = property(lambda self: self._network_id)

    def __call__(self, method, url, *args, **kwargs):
        url = urllib.parse.urljoin('/networks/{}/'.format(self.network_id), url)
        return super(NetworksMixin, self).__call__(method, url, *args, **kwargs)
