
from cloud_utils.client import Cloud
from cloud_utils.types.dns import Record

client = Cloud(
    location='london',
    platform='all',
    gcp_project='hs-nonprod',
    aws_profile='hs-nonprod'
)

for zone in client.dns.zones():
    records = client.dns.records(zone_name=zone.name)
    for record in records:
        print(record.__dict__)

for group in client.compute.groups():
    print(group.__dict__)

print('Done')
