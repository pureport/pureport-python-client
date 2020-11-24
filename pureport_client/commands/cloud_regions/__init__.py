# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import argument

from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Display Pureport cloud region information
    """

    def list(self):
        """Display list of cloud regions

        \f
        :returns: a list of cloud region objects
        :rtype: list
        """
        return self.client.get_cloud_regions()

    @argument('cloud_region_id')
    def get(self, cloud_region_id):
        """Display cloud region identifed by ID

        \f
        :param cloud_region_id: the cloud region id to retrieve
        :type cloud_region_id: str

        :returns: a cloud region object
        :rtype: CloudRegion
        """
        return self.client.get_cloud_region(cloud_region_id)
