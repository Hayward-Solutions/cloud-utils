
from cloud_utils.client import Cloud
from cloud_utils.metadata import Metadata

metadata = Metadata()
client = Cloud(
    location=metadata.location,
    platform=metadata.platform,
    gcp_project=None if metadata.project_id == '' else metadata.project_id,
    aws_load_default_credentials=True if metadata.platform == 'aws' else False
)

environment = metadata.tags['Environment']

for zone in client.dns.zones():
    records = client.dns.records(zone_name=zone.name)
    for record in records:
        print(record.__dict__)

for group in client.compute.groups():
    print(group.__dict__)

print('Done')
