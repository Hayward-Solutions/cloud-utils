from cloud_utils.client import Client

client = Client(
    location='london',
    platform='aws',
    aws_profile='hs-core'
)


instances = client.compute.instances()
for instance in instances:
    print(instance.private_ip)

