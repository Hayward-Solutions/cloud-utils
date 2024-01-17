
from cloud_utils.static.locations import Locations
from cloud_utils.cloud_clients import aws
from cloud_utils.cloud_clients import gcp
from cloud_utils.interfaces import compute


class Client:
    location: str
    platform: str

    aws = aws.AWS
    gcp = gcp.GCP

    compute: compute.Compute

    def __init__(self, location, platform, aws_profile=None, gcp_project=None):
        self.location = location
        self.platform = platform

        if platform in ['aws', 'all']:
            self.aws = aws.AWS(profile=aws_profile, region=Locations.aws[location])
        else:
            self.aws = None

        if platform in ['gcp', 'all']:
            self.gcp = gcp.GCP(project=gcp_project, region=Locations.gcp[location])
        else:
            self.gcp = None

        self.compute = compute.Compute(aws_client=self.aws, gcp_client=self.gcp)
