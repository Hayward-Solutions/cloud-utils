import botocore.exceptions

from cloud_utils.types.compute import Instance
from cloud_utils.types.compute import InstanceGroup
from cloud_utils.cloud_clients.aws import AWS
from cloud_utils.cloud_clients.gcp import GCP


class Compute:
    aws_client: AWS
    gcp_client: GCP

    def __init__(self,
                 aws_client: AWS = None,
                 gcp_client: GCP = None):
        self.aws_client = aws_client
        self.gcp_client = gcp_client

    def groups(self, group_name: str = None) -> list[InstanceGroup]:
        groups = []
        if self.aws_client:
            try:
                groups += self.aws_client.get_groups(group_name=group_name)
            except botocore.exceptions.ClientError:
                raise
        if self.gcp_client:
            try:
                groups += self.gcp_client.get_groups(group_name=group_name)
            except Exception:
                raise

        return groups

    def instances(self, group_name: str = None, identifier: str = None) -> list[Instance]:
        instances = []
        if self.aws_client:
            try:
                instances = instances + self.aws_client.get_instances(
                    group_name=group_name, identifier=identifier
                )
            except botocore.exceptions.ClientError:
                raise
        if self.gcp_client:
            try:
                instances = instances + self.gcp_client.get_instances(
                    group_name=group_name, identifier=identifier
                )
            except Exception:
                raise

        return instances

    def scale(self, group_name: str, size: int):
        pass
