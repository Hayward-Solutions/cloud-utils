import botocore.exceptions

from cloud_utils.types.compute import Instance
from cloud_utils.types.compute import InstanceGroup
from cloud_utils.cloud_clients.gcp import GCP
from cloud_utils.cloud_clients.aws import AWS


class Compute:
    """
    Describes a cloud-agnostic interface to interact with Compute APIs across multiple cloud providers.
    """
    aws_client: AWS
    gcp_client: GCP

    def __init__(self,
                 aws_client: AWS = None,
                 gcp_client: GCP = None):
        """
        @:param aws_client
        @:param gcp_client
        """
        self.aws_client = aws_client
        self.gcp_client = gcp_client

    def groups(self, group_name: str = None) -> [InstanceGroup]:
        """
        :param group_name: Optional. Name of a specific group to return
        :return: List of cloud-agnostic InstanceGroups
        """
        groups = []
        if self.aws_client:
            try:
                groups += self.aws_client.compute.get_groups(group_name=group_name)
            except botocore.exceptions.ClientError:
                raise
        if self.gcp_client:
            try:
                groups += self.gcp_client.compute.get_groups(group_name=group_name)
            except Exception:
                raise

        return groups

    def instances(self, group_name: str = None, identifier: str = None) -> [Instance]:
        """
        :param group_name: Optional. Name of a specific group to return
        :param identifier: Optional. Name of a specific Instance to return
        :return: List of cloud-agnostic Instances
        """
        instances = []
        if self.aws_client:
            try:
                instances = instances + self.aws_client.compute.get_instances(
                    group_name=group_name, identifier=identifier
                )
            except botocore.exceptions.ClientError:
                raise
        if self.gcp_client:
            try:
                instances = instances + self.gcp_client.compute.get_instances(
                    group_name=group_name, identifier=identifier
                )
            except Exception:
                raise

        return instances

    def scale(self, group_name: str, size: int):
        """
        :param group_name: Name of the Group to scale
        :param size: Desired size of the InstanceGroup
        :return: None
        """
        if self.aws_client:
            try:
                self.aws_client.scale(group_name=group_name, size=size)
            except botocore.exceptions.ClientError:
                raise

        if self.gcp_client:
            try:
                self.gcp_client.scale(group_name=group_name, size=size)
            except Exception:
                raise
