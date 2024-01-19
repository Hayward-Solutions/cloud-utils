import os.path

import boto3
import botocore.exceptions
from cloud_utils.cloud_clients.apis.aws.boto import boto_client
from cloud_utils.types.storage import Bucket
from cloud_utils.types.storage import Blob


class Storage:
    session = boto3.session.Session

    def __init__(self, session: boto3.session.Session):
        self.session = session

    def get_buckets(self, bucket_name: str = None) -> [Bucket]:
        s3 = boto_client(self.session, 's3')
        buckets = []
        for bucket in s3.list_buckets()['Buckets']:
            if bucket_name is None or bucket_name == bucket['Name']:
                buckets.append(Bucket(
                    platform='AWS',
                    name=bucket['Name']
                ))

        return buckets

    def get_blobs(self, bucket_name: str, path: str = None) -> [Blob]:
        s3 = boto_client(self.session, 's3')
        blobs = []
        try:
            for blob in s3.list_objects_v2(Bucket=bucket_name, Prefix=path)['Contents']:
                blobs.append(Blob(
                    platform='AWS',
                    key=blob['Key'],
                    bucket=bucket_name
                ))
        except botocore.exceptions.ClientError:
            return []
        return blobs

    def upload(self, blob: Blob):
        s3 = boto_client(self.session, 's3')
        if os.path.exists(blob.local_path) and blob.local_path != '':
            s3.upload_file(
                Filename=blob.local_path,
                Bucket=blob.bucket,
                Key=blob.key,
            )
        else:
            raise FileNotFoundError

    def download(self, blob: Blob):
        s3 = boto_client(self.session, 's3')
        try:
            s3.download_file(
                Bucket=blob.bucket,
                Key=blob.key,
                Filename=blob.local_path
            )
        except botocore.exceptions.ClientError:
            raise

    def delete(self, blob: Blob):
        s3 = boto_client(self.session, 's3')
        try:
            s3.delete_object(
                Bucket=blob.bucket,
                Key=blob.key
            )
        except botocore.exceptions.ClientError:
            raise
