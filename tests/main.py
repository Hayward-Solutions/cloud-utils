
from cloud_utils.client import Client
from cloud_utils.types.dns import Record

client = Client(
    location='london',
    platform='all',
    gcp_project='hs-nonprod',
    aws_profile='hs-nonprod'
)

for zone in client.dns.zones():
    records = client.dns.records(zone_name=zone.name)
    for record in records:
        print(record.__dict__)

print('Done')
