# Cloud Utils

Cloud-Utils aims to provide a single interface for interacting with multiple cloud platforms.

## Getting Started

```commandline
pip3 install cloud-utils
```

```python
from cloud_utils.client import Cloud

many_clouds = Cloud(
    location='london',
    platform='all',
    aws_profile='dev-profile',
    gcp_project='dev-project'
)

all_instances = many_clouds.compute.instances()
for instance in all_instances:
    print(instance.platform)
    print(instance.private_ip)

aws_cloud = Cloud(
    location='ireland',
    platform='aws',
    aws_profile='production'
)

auto_scaling_groups = aws_cloud.compute.groups()
for asg in auto_scaling_groups:
    print(asg.name)
    print(asg.size)
```
