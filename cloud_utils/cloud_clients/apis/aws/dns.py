
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
                    platform='AWS',
                    name=zone['Name'],
                    zone_id=zone['Id'].split('/')[-1],
                    record_count=zone['ResourceRecordSetCount']
                ))

        return zones

    def get_records(self, zone_name: str) -> [Record]:
        route53 = boto_client(self.session, 'route53')
        zones = self.get_zones(zone_name=zone_name)
        if len(zones) == 0:
            # This is allowed to fail, as we might look up a Zone in GCP using the AWS API
            return []
        else:
            zone_id = zones[0].zone_id

        response = route53.list_resource_record_sets(
            HostedZoneId=zone_id
        )

        records = []
        for record in response['ResourceRecordSets']:
            records.append(Record(
                platform='AWS',
                name=record['Name'],
                zone_id=zone_id,
                record_type=record['Type'],
                ttl=record['TTL'],
                records=[target['Value'] for target in record['ResourceRecords']]
            ))

        return records

    def upsert_record(self, record: Record):
        route53 = boto_client(self.session, 'route53')
        route53.change_resource_record_sets(
            HostedZoneId=record.zone_id,
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
            HostedZoneId=record.zone_id,
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
