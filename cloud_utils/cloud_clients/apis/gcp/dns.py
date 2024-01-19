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
        client = dns.Client(project=self.project)
        zones = []
        for zone in client.list_zones():
            if zone_name is None or zone_name == zone.dns_name:
                zones.append(Zone(
                    platform='GCP',
                    name=zone.dns_name,
                    zone_id=zone.name,
                    record_count=len([record for record in zone.list_resource_record_sets()])
                ))
        return zones

    def get_records(self, zone_name: str) -> [Record]:
        client = dns.Client(project=self.project)
        zones = self.get_zones(zone_name=zone_name)

        if len(zones) == 0:
            # This is allowed to fail, as we might look up a Zone in AWS using the GCP API
            return []
        else:
            zone = zones[0]

        records = []
        for record in client.zone(name=zone.zone_id, dns_name=zone_name).list_resource_record_sets():
            records.append(Record(
                platform='GCP',
                name=record.name,
                record_type=record.record_type,
                ttl=record.ttl,
                records=record.rrdatas,
                zone_id=record.zone.name
            ))

        return records

    def upsert_record(self, record: Record):
        """
        Updates or Creates an existing DNS Record Set.
        Searches the Zone for existing records, if one is found, it is removed during the same change batch.
        @:param record: Record to upsert.
        """

        client = dns.Client(project=self.project)
        zone = client.zone(record.zone_id)
        change_batch = zone.changes()

        existing_records = zone.list_resource_record_sets()
        new_record = zone.resource_record_set(
            name=record.name,
            ttl=record.ttl,
            record_type=record.record_type,
            rrdatas=record.records
        )
        for existing_record in existing_records:
            if existing_record.name == record.name and existing_record.record_type == record.record_type:
                print('Existing record found')
                change_batch.delete_record_set(existing_record)

        change_batch.add_record_set(new_record)
        change_batch.create()
        while change_batch.status != 'done':
            change_batch.reload()

    def remove_record(self, record: Record):
        client = dns.Client(project=self.project)
        zone = client.zone(record.zone_id)
        change_batch = zone.changes()

        old_record = zone.resource_record_set(
            name=record.name,
            ttl=record.ttl,
            record_type=record.record_type,
            rrdatas=record.records
        )

        change_batch.delete_record_set(old_record)
        change_batch.create()
        while change_batch.status != 'done':
            change_batch.reload()
