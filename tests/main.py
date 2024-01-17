from cloud_utils.client import Client

client = Client(
    location='london',
    platform='all',
    aws_profile='hs-transit',
    gcp_project='hs-transit'
)
