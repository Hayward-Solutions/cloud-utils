import os.path

import google.api_core.exceptions
from google.cloud import storage
from cloud_utils.types.storage import Bucket
from cloud_utils.types.storage import Blob


class Storage:
    project: str

    def __init__(self, project: str):
        self.project = project

    def get_buckets(self, bucket_name: str = None) -> [Bucket]:
        client = storage.Client(project=self.project)
        buckets = []
        for bucket in client.list_buckets():
            if bucket_name is None or bucket_name == bucket.name:
                buckets.append(Bucket(
                    platform='GCP',
                    name=bucket.name
                ))

        return buckets

    def get_blobs(self, bucket_name: str, path: str = None) -> [Blob]:
        client = storage.Client(project=self.project)
        blobs = []
        try:
            for blob in client.list_blobs(bucket_or_name=bucket_name, prefix=path):
                blobs.append(Blob(
                    platform='GCP',
                    key=blob.name,
                    bucket=bucket_name
                ))
        except google.api_core.exceptions.NotFound:
            return []
        return blobs

    def upload(self, blob: Blob):
        client = storage.Client(project=self.project)
        if os.path.exists(blob.local_path) and blob.local_path != '':
            print(f'uploading {blob.key}')
            bucket = client.bucket(blob.bucket)
            bucket.blob(blob.key).upload_from_filename(blob.local_path)
        else:
            raise FileNotFoundError

    def download(self, blob: Blob):
        client = storage.Client(project=self.project)
        bucket = client.bucket(blob.bucket)
        bucket.blob(blob.key).download_to_filename(blob.local_path)

    def delete(self, blob: Blob):
        client = storage.Client(project=self.project)
        bucket = client.bucket(blob.bucket)
        bucket.blob(blob.key).delete()
