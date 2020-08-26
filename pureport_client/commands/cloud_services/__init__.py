# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import argument

from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Display Pureport cloud services information
    """

    def list(self):
        """Display a list of all cloud services

        \f
        :returns: a list of cloud services
        :rtype: list
        """
        return self.__call__('get', '/cloudServices')

    @argument('cloud_service_id')
    def get(self, cloud_service_id):
        """Display cloud service identified by ID

        \f
        :param cloud_service_id: the id of the cloud service to retrieve
        :type cloud_service_id: str

        :returns: a cloud service object
        :rtype: dict
        """
        return self.__call__('get', '/cloudServices/{}'.format(cloud_service_id))
