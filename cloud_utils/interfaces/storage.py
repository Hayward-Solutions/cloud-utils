from cloud_utils.types.storage import Bucket
from cloud_utils.types.storage import Blob
from cloud_utils.cloud_clients.gcp import GCP
from cloud_utils.cloud_clients.aws import AWS


class Storage:
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

    def buckets(self, bucket_name: str = None) -> [Bucket]:
        buckets = []
        if self.aws_client:
            buckets += self.aws_client.storage.get_buckets(bucket_name=bucket_name)
        if self.gcp_client:
            buckets += self.gcp_client.storage.get_buckets(bucket_name=bucket_name)

        return buckets

    def blobs(self, bucket_name: str, path: str = '') -> [Blob]:
        blobs = []
        if self.aws_client:
            blobs += self.aws_client.storage.get_blobs(bucket_name=bucket_name, path=path)
        if self.gcp_client:
            blobs += self.gcp_client.storage.get_blobs(bucket_name=bucket_name, path=path)

        return blobs

    def upload(self, blob: Blob):
        if blob.platform.lower() == 'aws':
            self.aws_client.storage.upload(blob)
        if blob.platform.lower() == 'gcp':
            self.gcp_client.storage.upload(blob)

    def download(self, blob: Blob):
        if blob.platform.lower() == 'aws':
            self.aws_client.storage.download(blob)
        if blob.platform.lower() == 'gcp':
            self.gcp_client.storage.download(blob)

    def delete(self, blob: Blob):
        if blob.platform.lower() == 'aws':
            self.aws_client.storage.delete(blob)
        if blob.platform.lower() == 'gcp':
            self.gcp_client.storage.delete(blob)
