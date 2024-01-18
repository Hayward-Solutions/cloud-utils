
from cloud_utils.static.locations import Locations
from cloud_utils.cloud_clients import aws
from cloud_utils.cloud_clients import gcp
from cloud_utils.interfaces import compute


class Client:
    """
    Describes a single client to interact with environments distributed across multiple cloud providers.
    """
    location: str
    platform: str

    aws = aws.AWS
    gcp = gcp.GCP

    compute: compute.Compute

    def __init__(self, location, platform,
                 aws_profile=None,
                 aws_role_arn=None,
                 aws_access_key_id=None,
                 aws_secret_access_key=None,
                 aws_session_token=None,
                 aws_load_default_credentials=False,
                 gcp_project=None):
        """
        Creates a cloud-agnostic CloudUtils Client
        @:parameter location
        @:parameter platform
        @:parameter aws_profile
        @:parameter gcp_project
        """
        self.location = location
        self.platform = platform

        if platform in ['aws', 'all']:
            self.aws = aws.AWS(
                profile=aws_profile,
                region=Locations.aws[location],
                role_arn=aws_role_arn,
                access_key=aws_access_key_id,
                secret_key=aws_secret_access_key,
                session_token=aws_session_token,
                load_host_credentials=aws_load_default_credentials
            )
        else:
            self.aws = None

        if platform in ['gcp', 'all']:
            self.gcp = gcp.GCP(project=gcp_project, region=Locations.gcp[location])
        else:
            self.gcp = None

        self.compute = compute.Compute(aws_client=self.aws, gcp_client=self.gcp)
