
from cloud_utils.cloud_clients.apis.gcp.compute import Compute
from cloud_utils.cloud_clients.apis.gcp.dns import Dns
from cloud_utils.cloud_clients.apis.gcp.storage import Storage


class GCP:
    project: str
    region: str
    compute: Compute
    dns: Dns
    storage: Storage

    def __init__(self, project: str, region: str):
        self.project = project
        self.region = region

        self.compute = Compute(project=project, region=region)
        self.dns = Dns(project=project, region=region)
        self.storage = Storage(project=project)
