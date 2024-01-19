
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
        response = route53.list_hosted_zones()
        zones = []
        for zone in response['HostedZones']:
            if zone_name is None or zone['Name'] == zone_name:
                zones.append(Zone(
                    platform='aws',
                    name=zone['Name'],
                    id=zone['Id'].split('/')[-1],
                    record_count=zone['ResourceRecordSetCount']
                ))

        return zones

    def get_records(self, zone_name: str) -> [Record]:
        route53 = boto_client(self.session, 'route53')
        try:
            zone_id = self.get_zones(zone_name=zone_name)[0].id
        except IndexError:
            print(f'ERROR: Zone {zone_name} not found.')
            raise

        response = route53.list_resource_record_sets(
            HostedZoneId=zone_id
        )

        records = []
        for record in response['ResourceRecordSets']:
            records.append(Record(
                platform='aws',
                name=record['Name'],
                zone=zone_id,
                record_type=record['Type'],
                ttl=None if 'TTL' not in record else record['TTL'],
                records=[target['Value'] for target in record['ResourceRecords']]
            ))

        return records

    def upsert_record(self, record: Record):
        route53 = boto_client(self.session, 'route53')
        route53.change_resource_record_sets(
            HostedZoneId=record.zone,
            ChangeBatch={
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record.name,
                        'Type': record.record_type,
                        'TTL': record.ttl,
                        'ResourceRecords': [{'Value': target} for target in record.records]
                    }
                }]
            }
        )

    def remove_record(self, record: Record):
        route53 = boto_client(self.session, 'route53')
        route53.change_resource_record_sets(
            HostedZoneId=record.zone,
            ChangeBatch={
                'Changes': [{
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': record.name,
                        'Type': record.record_type,
                        'TTL': record.ttl,
                        'ResourceRecords': [{'Value': target} for target in record.records]
                    }
                }]
            }
        )
