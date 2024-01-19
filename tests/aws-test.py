from cloud_utils.client import Cloud
from cloud_utils.metadata import Metadata

print('Starting Test')

metadata = Metadata()
cloud = Cloud(
    location=metadata.location,
    platform=metadata.platform,
    gcp_project=None if metadata.project_id == '' else metadata.project_id,
    aws_load_default_credentials=True if metadata.platform == 'aws' else False
)

print(f'Metadata!')
print(metadata.__dict__)

print('Instance Groups')
groups = cloud.compute.groups()
for group in groups:
    print(group.__dict__)

print('Instances')
instances = cloud.compute.instances()
for instance in instances:
    print(instance.__dict__)
