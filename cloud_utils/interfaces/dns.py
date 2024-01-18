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
            zones.append(self.aws_client.dns.get_zones(zone_name=zone_name))

        if self.gcp_client:
            zones.append(self.gcp_client.dns.get_zones(zone_name=zone_name))

        return zones

    def records(self, zone_name: str) -> [Record]:
        records = []
        if self.aws_client:
            records.append(self.aws_client.dns.get_records(zone_name=zone_name))

        if self.gcp_client:
            records.append(self.gcp_client.dns.get_records(zone_name=zone_name))

        return records

    def upsert(self, record: Record):
        if record.platform == 'aws' and self.aws_client:
            print(f'INFO: Upsert record {record.__dict__}')
        elif record.platform == 'gcp' and self.gcp_client:
            print(f'INFO: Upsert record {record.__dict__}')
        else:
            print(f'ERROR: Problem processing record {record.__dict__}')
            raise Exception

    def remove(self, record: Record):
        if record.platform == 'aws' and self.aws_client:
            print(f'INFO: Remove record {record.__dict__}')
        elif record.platform == 'gcp' and self.gcp_client:
            print(f'INFO: Remove record {record.__dict__}')
        else:
            print(f'ERROR: Problem processing record {record.__dict__}')
            raise Exception
