from cloud_utils.client import Cloud
from cloud_utils.metadata import Metadata

print('Starting AWS Test')

metadata = Metadata()
cloud = Cloud(
    location=metadata.location,
    platform=metadata.platform,
    gcp_project=None if metadata.project_id == '' else metadata.project_id,
    aws_load_default_credentials=True if metadata.platform == 'aws' else False
)

print(f'Metadata!')
print(metadata.__dict__)
