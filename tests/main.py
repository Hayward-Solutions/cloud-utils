
from cloud_utils.client import Cloud
from cloud_utils.types.storage import Blob


cloud = Cloud(
    location='london',
    platform='aws',
    gcp_project='hs-nonprod',
    aws_profile='hs-nonprod'
)

bucket = cloud.storage.buckets('hs-nonprod-terraform')[0]
new_blob = Blob(
    platform=bucket.platform,
    bucket=bucket.name,
    key='test'
)

cloud.storage.delete(new_blob)

for blob in cloud.storage.blobs(bucket.name):
    print(blob.key)

print('Done')
