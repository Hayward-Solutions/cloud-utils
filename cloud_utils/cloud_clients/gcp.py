from cloud_utils.types.compute import InstanceGroup
from cloud_utils.types.compute import Instance
from cloud_utils.types.dns import Zone
from cloud_utils.types.dns import Record

from cloud_utils.cloud_clients.apis.gcp.compute import Compute
from cloud_utils.cloud_clients.apis.gcp.dns import Dns


class GCP:
    project: str
    region: str
    compute: Compute
    dns: Dns

    def __init__(self, project: str, region: str):
        self.project = project
        self.region = region

        self.compute = Compute(project=project, region=region)
        self.dns = Dns(project=project, region=region)
