import boto3
import botocore.exceptions
from cloud_utils.types.dns import Zone
from cloud_utils.types.dns import Record
from cloud_utils.cloud_clients.apis.aws.boto import boto_client


class Dns:
    session = boto3.session.Session

    def __init__(self, session: boto3.session.Session):
        self.session = session

    def get_zones(self, zone_name: str = None) -> [Zone]:
        route53 = boto_client(self.session, 'route53')
        return []

    def get_records(self, zone_name: str) -> [Record]:
        route53 = boto_client(self.session, 'route53')
        return []

    def upsert_record(self, record: Record):
        route53 = boto_client(self.session, 'route53')
        pass

    def remove_record(self):
        route53 = boto_client(self.session, 'route53')
        pass
