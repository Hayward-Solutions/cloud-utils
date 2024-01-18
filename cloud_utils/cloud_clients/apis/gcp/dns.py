from google.cloud import dns
from google.api_core.exceptions import NotFound
from cloud_utils.types.dns import Zone
from cloud_utils.types.dns import Record


class Dns:
    project: str
    region: str

    def __init__(self, project: str, region: str):
        self.project = project
        self.region = region

    def get_zones(self, zone_name: str = None) -> [Zone]:
        return []

    def get_records(self, zone_name: str) -> [Record]:
        return []

    def upsert_record(self, record: Record):
        pass

    def remove_record(self):
        pass
