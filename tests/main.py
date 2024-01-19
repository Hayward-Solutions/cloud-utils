from cloud_utils.client import Client
from cloud_utils.types.dns import Record

client = Client(
    location='london',
    platform='all',
    aws_profile='hs-nonprod',
    gcp_project='hs-nonprod'
)

for zone in client.dns.zones():
    print(zone.__dict__)
