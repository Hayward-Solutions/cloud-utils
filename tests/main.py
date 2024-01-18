from cloud_utils.client import Client

client = Client(
    location='london',
    platform='aws',
    aws_load_default_credentials=True
)


instances = client.compute.instances()
for instance in instances:
    print(instance.private_ip)

print(client.aws.__dict__)
