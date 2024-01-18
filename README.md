# Cloud Utils

Cloud-Utils aims to provide a single interface for interacting with multiple cloud platforms.

## Getting Started

```commandline
pip3 install --trusted-host gitlab.devmagic.cloud --index-url https://gitlab.devmagic.cloud/api/v4/projects/6/packages/pypi/simple cloud-utils
```

```python
from cloud_utils.client import Client

many_clouds = Client(
    location='london',
    platform='all',
    aws_profile='dev-profile',
    gcp_project='dev-project'
)

all_instances = many_clouds.compute.instances()
for instance in all_instances:
    print(instance.platform)
    print(instance.private_ip)

aws_cloud = Client(
    location='ireland',
    platform='aws',
    aws_profile='production'
)

auto_scaling_groups = aws_cloud.compute.groups()
for asg in auto_scaling_groups:
    print(asg.name)
    print(asg.size)
```

# Build

## Locally

```commandline
pip3 install poetry
poetry install
poetry build

pip3 install .dist/cloud_utils-0.0.0.tar.gz
```

## Publish To Private registry

```commandline
git tag 0.0.0
git push origin 0.0.0
```

## Use Cloud-Utils in another Poetry Project

```commandline
poetry source add cloud-utils --priority explicit --repository https://gitlab.devmagic.cloud/api/v4/projects/6/packages/pypi/simple
poetry config certificates.cloud-utils.cert false
poetry add cloud-utils --source cloud-utils
```
