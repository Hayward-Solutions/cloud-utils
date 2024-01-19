from cloud_utils.types.dns import Zone
from cloud_utils.types.dns import Record
from cloud_utils.cloud_clients.gcp import GCP
from cloud_utils.cloud_clients.aws import AWS


class DNS:
    """
    Describes a cloud-agnostic interface to interact with Compute APIs across multiple cloud providers.
    """
    aws_client: AWS
    gcp_client: GCP

    def __init__(self,
                 aws_client: AWS = None,
                 gcp_client: GCP = None):
        """
        @:param aws_client
        @:param gcp_client
        """
        self.aws_client = aws_client
        self.gcp_client = gcp_client

    def zones(self, zone_name: str = None) -> [Zone]:
        zones = []
        if self.aws_client:
            zones += self.aws_client.dns.get_zones(zone_name=zone_name)

        if self.gcp_client:
            zones += self.gcp_client.dns.get_zones(zone_name=zone_name)

        return zones

    def records(self, zone_name: str) -> [Record]:
        records = []
        if self.aws_client:
            records += self.aws_client.dns.get_records(zone_name=zone_name)

        if self.gcp_client:
            records += self.gcp_client.dns.get_records(zone_name=zone_name)

        return records

    def upsert(self, record: Record):
        if record.platform == 'AWS' and self.aws_client:
            self.aws_client.dns.upsert_record(record)
        elif record.platform == 'GCP' and self.gcp_client:
            self.gcp_client.dns.upsert_record(record)
        else:
            print(f'ERROR: Invalid Platform.')
            raise Exception

    def remove(self, record: Record):
        if record.platform == 'AWS' and self.aws_client:
            self.aws_client.dns.remove_record(record)
        elif record.platform == 'GCP' and self.gcp_client:
            self.gcp_client.dns.remove_record(record)
        else:
            print(f'ERROR: Invalid Platform')
            raise Exception
